"""
data_api.py
-----------
BACKEND INTEGRATION SEAM.

Every function in this file is the contract the frontend depends on.
Right now each one returns data derived from mock_data.py. When the real
pipeline is ready, replace the *body* of each function with a real call
(MySQL query, NLP extraction pipeline, trained SIF classifier, etc.)
WITHOUT changing the function signature — the frontend will not need to
change.

    Current:  Streamlit UI -> data_api.py -> mock_data.py (synthetic)
    Future:   Streamlit UI -> data_api.py -> MySQL + NLP/ML pipeline

Look for the "BACKEND INTEGRATION POINT" comments.
"""

from datetime import timedelta
import random
import pandas as pd

from src.frontend.mock_data import (
    REPORTS_DF,
    HAZARD_PROFILES,
    get_precursor_pattern_table,
)

SAMPLE_REPORTS = [
    {
        "label": "Electrical isolation not verified (Near Miss)",
        "text": (
            "During maintenance of the pump, the technician started work without verifying "
            "electrical isolation. The supervisor stopped the job before contact with the "
            "energized equipment."
        ),
    },
    {
        "label": "Confined space entry without gas testing",
        "text": (
            "A worker entered the separator vessel to carry out internal inspection before "
            "gas testing was completed for the confined space. The entry was halted by a "
            "co-worker after atmospheric monitoring equipment was found unused."
        ),
    },
    {
        "label": "Line-of-fire exposure during lifting",
        "text": (
            "While a crane was lifting a compressor skid into position, a field supervisor "
            "observed a rigger standing directly beneath the suspended load. The lift was "
            "paused and the rigger was repositioned outside the exclusion zone."
        ),
    },
    {
        "label": "Hot work permit not verified",
        "text": (
            "Welding work began on a pipeline tie-in point without a hot work permit visibly "
            "displayed at the location. Fire watch personnel were not present at the time "
            "work commenced."
        ),
    },
]


def get_reports():
    """
    Returns the full reports dataset as a DataFrame.
    BACKEND INTEGRATION POINT: replace with `SELECT * FROM safety_reports ...`
    """
    return REPORTS_DF.copy()


def get_pending_reviews(limit=25):
    """
    Returns reports awaiting HSE validation.
    BACKEND INTEGRATION POINT: replace with a query filtered on review_status='Pending'
    ordered by SIF score / recency, from the live reports table.
    """
    df = REPORTS_DF[REPORTS_DF["review_status"] == "Pending"].copy()
    df = df.sort_values(["sif_score", "date"], ascending=[False, False])
    return df.head(limit)


def get_site_risk():
    """
    Aggregates site-level SIF risk, high-risk report counts and a naive
    emerging-trend flag.
    BACKEND INTEGRATION POINT: replace with a materialized view / scheduled
    aggregation job over the reports table.
    """
    df = REPORTS_DF.copy()
    cutoff = df["date"].max() - timedelta(days=45)
    recent = df[df["date"] >= cutoff]
    older = df[df["date"] < cutoff]

    agg = df.groupby("site").agg(
        total_reports=("report_id", "count"),
        high_sif=("sif_band", lambda x: (x == "High").sum()),
        risk_score=("sif_score", "mean"),
    ).reset_index()

    recent_avg = recent.groupby("site")["sif_score"].mean()
    older_avg = older.groupby("site")["sif_score"].mean()

    def emerging(site):
        r, o = recent_avg.get(site), older_avg.get(site)
        if r is None or o is None or o == 0:
            return 0.0
        return round(((r - o) / o) * 100, 1)

    agg["emerging_trend_pct"] = agg["site"].apply(emerging)
    agg["risk_score"] = agg["risk_score"].round(1)

    def priority(row):
        if row["risk_score"] >= 75 or row["emerging_trend_pct"] >= 25:
            return "Critical"
        elif row["risk_score"] >= 55 or row["emerging_trend_pct"] >= 10:
            return "Elevated"
        return "Monitor"

    agg["priority"] = agg.apply(priority, axis=1)
    return agg.sort_values("risk_score", ascending=False).reset_index(drop=True)


def get_precursor_patterns():
    """
    Returns ranked recurring precursor patterns (activity+hazard+failure mode).
    BACKEND INTEGRATION POINT: replace with output of the precursor-mining /
    sequence-pattern model run against historical + incoming reports.
    """
    return get_precursor_pattern_table()


def get_barrier_failures():
    """
    Aggregates barrier failure occurrences across the dataset.
    BACKEND INTEGRATION POINT: replace with output of the barrier-classification
    model / structured extraction pipeline.
    """
    df = REPORTS_DF.copy()
    total = len(df)
    cutoff = df["date"].max() - timedelta(days=45)

    agg = df.groupby("critical_barrier").agg(
        occurrences=("report_id", "count"),
        avg_sif=("sif_score", "mean"),
        top_activity=("activity", lambda x: x.mode()[0] if not x.mode().empty else ""),
        top_site=("site", lambda x: x.mode()[0] if not x.mode().empty else ""),
    ).reset_index()
    agg["pct_of_high_risk"] = round(agg["occurrences"] / total * 100, 1)

    recent_counts = df[df["date"] >= cutoff].groupby("critical_barrier").size()
    older_counts = df[df["date"] < cutoff].groupby("critical_barrier").size()

    def trend(barrier):
        r, o = recent_counts.get(barrier, 0), older_counts.get(barrier, 0)
        if o == 0:
            return 100.0 if r > 0 else 0.0
        return round(((r - o) / o) * 100, 1)

    agg["trend_pct"] = agg["critical_barrier"].apply(trend)
    return agg.sort_values("occurrences", ascending=False).reset_index(drop=True)


def get_lsr_statistics():
    """
    Aggregates statistics per IOGP Life-Saving Rule, accounting for reports
    that reference a rule either as primary or secondary.
    BACKEND INTEGRATION POINT: replace with a query joining reports to a
    normalized report_rules table (many-to-many).
    """
    df = REPORTS_DF.copy()
    primary = df[["life_saving_rule", "sif_score", "critical_barrier", "sif_band"]].rename(
        columns={"life_saving_rule": "rule"}
    )
    secondary = df[df["secondary_rule"].notna()][
        ["secondary_rule", "sif_score", "critical_barrier", "sif_band"]
    ].rename(columns={"secondary_rule": "rule"})
    combined = pd.concat([primary, secondary], ignore_index=True)

    agg = combined.groupby("rule").agg(
        reports=("rule", "size"),
        avg_sif=("sif_score", "mean"),
        high_sif_count=("sif_band", lambda x: (x == "High").sum()),
    ).reset_index()
    agg["avg_sif"] = agg["avg_sif"].round(1)

    failed_barriers = combined.groupby("rule")["critical_barrier"].agg(
        lambda x: x.mode()[0] if not x.mode().empty else ""
    )
    agg["top_failed_barrier"] = agg["rule"].map(failed_barriers)
    return agg.sort_values("reports", ascending=False).reset_index(drop=True)


def get_rule_detail(rule_name):
    """Drill-down detail for a single Life-Saving Rule."""
    df = REPORTS_DF.copy()
    mask = (df["life_saving_rule"] == rule_name) | (df["secondary_rule"] == rule_name)
    subset = df[mask]
    return {
        "hazards": subset["hazard"].value_counts().head(5),
        "activities": subset["activity"].value_counts().head(5),
        "barrier_failures": subset["barrier_failure"].value_counts().head(5),
        "sites": subset["site"].value_counts().head(5),
        "consequences": subset["potential_consequence"].value_counts().head(5),
        "count": len(subset),
    }


def get_site_detail(site_name):
    """Drill-down detail for a single site."""
    df = REPORTS_DF[REPORTS_DF["site"] == site_name].copy()
    return {
        "df": df,
        "top_activities": df["activity"].value_counts().head(5),
        "top_hazards": df["hazard"].value_counts().head(5),
        "top_rules": df["life_saving_rule"].value_counts().head(5),
        "top_failures": df["barrier_failure"].value_counts().head(5),
    }


def analyze_report(text: str):
    """
    AI ANALYSIS ENTRY POINT — currently a MOCK IMPLEMENTATION.

    ================================================================
    BACKEND INTEGRATION POINT
    ================================================================
    This function must be replaced with a real call to:
        1. The NLP extraction pipeline (hazard / activity / location NER)
        2. The trained SIF classifier (SIF potential % + risk band)
        3. Life-Saving Rule mapping logic (rule-based or learned)
        4. Barrier / barrier-failure / consequence inference model

    It currently performs simple keyword matching against known hazard
    profiles purely so the frontend has something realistic to render.
    THIS IS NOT A REAL MODEL PREDICTION. Do not present its output as
    ground truth in production — the UI already labels it as an
    "AI-assessed" / "suggested" result pending HSE validation, and that
    framing must be preserved when the real model is connected.
    ================================================================
    """
    text_lc = text.lower()

    keyword_map = {
        "Electrical Energy": ["electrical", "isolation", "energized", "energised", "voltage", "switchgear"],
        "Stored / Residual Energy": ["stored energy", "residual energy", "loto", "lock-out", "lockout"],
        "Toxic / Flammable Atmosphere": ["gas test", "confined space", "vessel entry", "toxic", "vapour", "vapor"],
        "Oxygen Deficiency": ["oxygen", "asphyxiat", "atmosphere monitoring"],
        "Ignition Source": ["hot work permit", "welding", "ignition", "spark"],
        "Flammable Vapour Presence": ["fire watch", "flammable", "flash fire"],
        "Suspended Load": ["crane", "rigging", "lift plan", "suspended load", "lifting"],
        "Line of Fire Exposure": ["line of fire", "struck by", "swinging load", "exclusion zone"],
        "Fall from Height": ["height", "fall arrest", "harness", "scaffold"],
        "Unauthorised / Unpermitted Work": ["permit-to-work", "unauthorised", "unauthorized", "without permit"],
        "Uncontrolled Excavation": ["excavation", "trench", "underground utility", "buried cable"],
        "Vehicle-Personnel Interface": ["vehicle", "pedestrian", "walkway", "collision"],
    }

    matched_hazard = None
    best_score = 0
    for hazard, keywords in keyword_map.items():
        score = sum(1 for kw in keywords if kw in text_lc)
        if score > best_score:
            best_score = score
            matched_hazard = hazard

    if matched_hazard is None:
        matched_hazard = random.choice(list(HAZARD_PROFILES.keys()))

    profile = HAZARD_PROFILES[matched_hazard]

    # crude activity guess
    activity = profile["activities"][0]
    for act in profile["activities"]:
        if act.lower().split()[0] in text_lc:
            activity = act
            break

    # crude report-type guess
    if "stopped" in text_lc or "halted" in text_lc or "paused" in text_lc or "before contact" in text_lc:
        report_type = "Near Miss"
    elif "injury" in text_lc or "injured" in text_lc:
        report_type = "Incident"
    elif "observed" in text_lc or "found" in text_lc:
        report_type = "Unsafe Condition"
    else:
        report_type = "Unsafe Act"

    base_conf = 0.6 + min(best_score, 4) * 0.09
    sif_potential = round(min(97, base_conf * 100 + random.uniform(-3, 6)), 1)
    sif_band = "High" if sif_potential >= 75 else ("Medium" if sif_potential >= 50 else "Low")
    model_confidence = round(min(0.98, base_conf + random.uniform(0.0, 0.08)) * 100, 1)

    location = random.choice(
        ["Duliajan Field Complex", "Baghjan EPS", "Moran GGS", "Digboi Refinery Unit-2"]
    )

    return {
        "sif_potential": sif_potential,
        "sif_band": sif_band,
        "model_confidence": model_confidence,
        "report_type": report_type,
        "activity": activity,
        "location": location,
        "hazard": matched_hazard,
        "life_saving_rule": profile["rule"],
        "critical_barrier": profile["barrier"],
        "barrier_failure": profile["failure"],
        "potential_consequence": profile["consequence"],
        "why_high_risk": _why_high_risk(matched_hazard, profile),
        "raw_text": text,
    }


def _why_high_risk(hazard, profile):
    """Generates a short human-readable justification string for the AI flag."""
    return (
        f"Report describes exposure to {hazard.lower()} where the required control "
        f"({profile['barrier'].lower()}) was reported as ineffective or absent. "
        f"This combination is a recognised precursor to: {profile['consequence'].lower()}."
    )


def submit_review_decision(report_id, decision, corrected_fields=None):
    """
    Records an HSE officer's Confirm / Reject / Correct decision.
    BACKEND INTEGRATION POINT: replace with a write to the review_decisions
    table, and (for Correct) a feedback record used for model retraining.
    Currently updates the in-memory session dataframe only (demo purposes).
    """
    idx = REPORTS_DF.index[REPORTS_DF["report_id"] == report_id]
    if len(idx) == 0:
        return False
    i = idx[0]
    if decision == "Confirm":
        REPORTS_DF.loc[i, "review_status"] = "Confirmed"
    elif decision == "Reject":
        REPORTS_DF.loc[i, "review_status"] = "Rejected"
    elif decision == "Correct" and corrected_fields:
        REPORTS_DF.loc[i, "review_status"] = "Corrected"
        for k, v in corrected_fields.items():
            if k in REPORTS_DF.columns and v is not None:
                REPORTS_DF.loc[i, k] = v
    return True
