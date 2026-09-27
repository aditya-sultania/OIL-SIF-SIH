"""
mock_data.py
------------
MOCK DATA LAYER — OIL SIF Precursor Intelligence Platform

Everything in this file is synthetic sample data used to make the frontend
fully functional before the real backend (MySQL + NLP/ML pipeline) exists.

Nothing here should be mistaken for real Oil India Limited data.

The data relationships are constructed deliberately (not random) so that
Hazard <-> Activity <-> Life-Saving Rule <-> Barrier <-> Consequence stay
logically consistent, and so that trends/rankings/precursor frequencies
are meaningful across the dashboard.

Replace this module with real database queries once the backend is ready.
See data_api.py for the integration seam.
"""

import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

random.seed(42)
np.random.seed(42)

# ---------------------------------------------------------------------------
# REFERENCE DOMAIN DATA
# ---------------------------------------------------------------------------

SITES = [
    "Duliajan Field Complex", "Moran GGS", "Kumchai EPS", "Naharkatiya Terminal",
    "Digboi Refinery Unit-2", "Jorajan Drilling Site", "Baghjan EPS",
    "Tengakhat GGS", "Barekuri Field Station", "Numaligarh Pipeline Yard",
]

ACTIVITIES = [
    "Maintenance", "Hot Work", "Lifting Operations", "Vessel Entry",
    "Drilling Operations", "Pipeline Work", "Electrical Work",
    "Working at Height", "Excavation", "Vehicle Movement",
]

# Each hazard maps to a canonical Life-Saving Rule, critical barrier,
# a typical barrier-failure mode, and a plausible consequence.
# A report can reference 1-2 hazards -> 1-2 Life-Saving Rules.
HAZARD_PROFILES = {
    "Electrical Energy": {
        "rule": "Energy Isolation",
        "barrier": "Isolation Verification",
        "failure": "Isolation not verified before work start",
        "consequence": "Fatal electrocution",
        "activities": ["Maintenance", "Electrical Work"],
    },
    "Stored / Residual Energy": {
        "rule": "Energy Isolation",
        "barrier": "Lock-Out Tag-Out (LOTO) Compliance",
        "failure": "LOTO device missing or bypassed",
        "consequence": "Crush injury from unexpected equipment start-up",
        "activities": ["Maintenance"],
    },
    "Toxic / Flammable Atmosphere": {
        "rule": "Confined Space",
        "barrier": "Gas Testing Prior to Entry",
        "failure": "Atmosphere not tested / test not repeated",
        "consequence": "Asphyxiation or explosion inside confined space",
        "activities": ["Vessel Entry"],
    },
    "Oxygen Deficiency": {
        "rule": "Confined Space",
        "barrier": "Continuous Atmosphere Monitoring",
        "failure": "Monitoring equipment not used through duration of entry",
        "consequence": "Loss of consciousness / asphyxiation",
        "activities": ["Vessel Entry"],
    },
    "Ignition Source": {
        "rule": "Hot Work",
        "barrier": "Hot Work Permit Compliance",
        "failure": "Work started without valid / site-verified permit",
        "consequence": "Fire or explosion in hydrocarbon atmosphere",
        "activities": ["Hot Work"],
    },
    "Flammable Vapour Presence": {
        "rule": "Hot Work",
        "barrier": "Gas Testing & Fire Watch",
        "failure": "Fire watch not maintained during work",
        "consequence": "Flash fire / explosion",
        "activities": ["Hot Work"],
    },
    "Suspended Load": {
        "rule": "Safe Mechanical Lifting",
        "barrier": "Lift Plan & Rigging Inspection",
        "failure": "Rigging not inspected / lift plan not followed",
        "consequence": "Struck-by injury from dropped or swinging load",
        "activities": ["Lifting Operations"],
    },
    "Line of Fire Exposure": {
        "rule": "Line of Fire",
        "barrier": "Exclusion Zone Control",
        "failure": "Personnel positioned in line of fire during operation",
        "consequence": "Fatal struck-by incident",
        "activities": ["Lifting Operations", "Drilling Operations", "Pipeline Work"],
    },
    "Fall from Height": {
        "rule": "Work at Height",
        "barrier": "Fall Protection System",
        "failure": "Fall arrest not anchored / harness not worn correctly",
        "consequence": "Fatal or serious fall injury",
        "activities": ["Working at Height"],
    },
    "Unauthorised / Unpermitted Work": {
        "rule": "Work Authorisation",
        "barrier": "Permit-to-Work Verification",
        "failure": "Work initiated without valid work authorisation",
        "consequence": "Uncontrolled hazard exposure of unknown severity",
        "activities": ["Maintenance", "Pipeline Work", "Excavation"],
    },
    "Uncontrolled Excavation": {
        "rule": "Line of Fire",
        "barrier": "Underground Utility Verification",
        "failure": "Excavation started without utility clearance",
        "consequence": "Pipeline rupture or buried cable strike",
        "activities": ["Excavation"],
    },
    "Vehicle-Personnel Interface": {
        "rule": "Safe Driving",
        "barrier": "Journey Management / Segregation",
        "failure": "Pedestrian route not segregated from vehicle movement",
        "consequence": "Fatal vehicle-pedestrian collision",
        "activities": ["Vehicle Movement"],
    },
}

REPORT_TYPES = ["Near Miss", "Unsafe Act", "Unsafe Condition", "Incident"]

REVIEW_STATUS = ["Pending", "Confirmed", "Corrected", "Rejected"]

# Narrative fragments used to assemble semi-realistic free text reports
NARRATIVE_TEMPLATES = {
    "Electrical Energy": [
        "During {activity_lc} of the {equip}, the technician started work without verifying electrical isolation. "
        "{intervention}",
    ],
    "Stored / Residual Energy": [
        "While carrying out {activity_lc} on the {equip}, the crew removed guarding before confirming stored energy "
        "had been fully released. {intervention}",
    ],
    "Toxic / Flammable Atmosphere": [
        "A worker entered the {equip} for {activity_lc} before gas testing was completed for the confined space. "
        "{intervention}",
    ],
    "Oxygen Deficiency": [
        "Personnel remained inside the {equip} during {activity_lc} without continuous atmosphere monitoring in place. "
        "{intervention}",
    ],
    "Ignition Source": [
        "Hot work was initiated on the {equip} without a verified hot work permit at the location. {intervention}",
    ],
    "Flammable Vapour Presence": [
        "Welding work proceeded on the {equip} while fire watch coverage was not maintained continuously. "
        "{intervention}",
    ],
    "Suspended Load": [
        "During {activity_lc} of the {equip}, the rigging was not inspected before the lift and the lift plan was "
        "not followed. {intervention}",
    ],
    "Line of Fire Exposure": [
        "A field supervisor observed a worker standing in the line of fire of the {equip} during {activity_lc}. "
        "{intervention}",
    ],
    "Fall from Height": [
        "A technician working at height on the {equip} was found without the fall arrest system properly anchored. "
        "{intervention}",
    ],
    "Unauthorised / Unpermitted Work": [
        "{activity} on the {equip} was found in progress without an approved permit-to-work. {intervention}",
    ],
    "Uncontrolled Excavation": [
        "Excavation near the {equip} began before underground utility clearance was confirmed. {intervention}",
    ],
    "Vehicle-Personnel Interface": [
        "A light vehicle was observed moving through the pedestrian walkway near the {equip} during shift change. "
        "{intervention}",
    ],
}

INTERVENTIONS = [
    "The supervisor stopped the job before contact with the hazard occurred.",
    "A co-worker intervened and the activity was halted immediately.",
    "The condition was self-reported by the crew before any injury occurred.",
    "The issue was identified during a routine HSE walkthrough.",
    "No injury occurred, but the exposure window lasted several minutes.",
]

EQUIPMENT = [
    "main process pump", "separator vessel", "wellhead assembly", "crude oil storage tank",
    "compressor skid", "pipeline tie-in point", "crane and load assembly", "drilling rig floor",
    "electrical switchgear", "flare knockout drum", "scaffold structure", "excavation trench",
]


def _weighted_choice(options, weights):
    return random.choices(options, weights=weights, k=1)[0]


def _build_narrative(hazard, activity):
    template = random.choice(NARRATIVE_TEMPLATES[hazard])
    return template.format(
        activity_lc=activity.lower(),
        activity=activity,
        equip=random.choice(EQUIPMENT),
        intervention=random.choice(INTERVENTIONS),
    )


def _sif_score_for(hazard, report_type):
    """Assigns an internally-consistent SIF score band per hazard severity."""
    high_severity = {
        "Electrical Energy", "Toxic / Flammable Atmosphere", "Oxygen Deficiency",
        "Ignition Source", "Suspended Load", "Line of Fire Exposure",
        "Fall from Height", "Vehicle-Personnel Interface",
    }
    base = random.uniform(68, 97) if hazard in high_severity else random.uniform(35, 75)
    # Actual incidents skew higher than near misses/unsafe acts at same hazard
    if report_type == "Incident":
        base = min(99, base + random.uniform(5, 12))
    elif report_type == "Unsafe Condition":
        base = min(97, base + random.uniform(0, 5))
    return round(base, 1)


def generate_reports(n=420, days_back=180):
    """
    Generates a realistic, internally-consistent set of safety reports.
    Returns a pandas DataFrame — this is the core dataset the whole app reads from.
    """
    rows = []
    today = datetime.now()
    site_weights = np.random.dirichlet(np.ones(len(SITES)) * 1.4) * 100
    # A couple of sites get an artificial upward trend injected for the
    # "Emerging Risk Detection" feature to have something real to show.
    trending_site = "Baghjan EPS"
    trending_hazard = "Electrical Energy"

    for i in range(n):
        hazard = random.choice(list(HAZARD_PROFILES.keys()))
        profile = HAZARD_PROFILES[hazard]
        activity = random.choice(profile["activities"])
        site = _weighted_choice(SITES, site_weights)
        report_type = _weighted_choice(REPORT_TYPES, [38, 27, 22, 13])

        days_ago = int(np.random.beta(1.6, 3.2) * days_back)
        date = today - timedelta(days=days_ago, hours=random.randint(0, 23))

        # inject a rising trend for the emerging-risk narrative
        if site == trending_site and hazard == trending_hazard and days_ago > 90:
            if random.random() < 0.55:
                continue  # thin out older records so recent ones dominate -> rising trend

        sif_score = _sif_score_for(hazard, report_type)
        sif_band = "High" if sif_score >= 75 else ("Medium" if sif_score >= 50 else "Low")

        # secondary hazard sometimes present (multi-rule support)
        secondary_hazard = None
        if random.random() < 0.22:
            candidates = [h for h in HAZARD_PROFILES if h != hazard]
            secondary_hazard = random.choice(candidates)

        review_status = _weighted_choice(REVIEW_STATUS, [46, 34, 12, 8])

        rows.append({
            "report_id": f"OIL-{2025 if date.year == 2025 else date.year}-{i+1:05d}",
            "date": date,
            "site": site,
            "report_type": report_type,
            "activity": activity,
            "hazard": hazard,
            "secondary_hazard": secondary_hazard,
            "life_saving_rule": profile["rule"],
            "secondary_rule": HAZARD_PROFILES[secondary_hazard]["rule"] if secondary_hazard else None,
            "critical_barrier": profile["barrier"],
            "barrier_failure": profile["failure"],
            "potential_consequence": profile["consequence"],
            "sif_score": sif_score,
            "sif_band": sif_band,
            "review_status": review_status,
            "narrative": _build_narrative(hazard, activity),
        })

    df = pd.DataFrame(rows).sort_values("date", ascending=False).reset_index(drop=True)
    return df


# Single shared in-memory dataset for the session (simulates a DB table)
REPORTS_DF = generate_reports()


def get_precursor_pattern_table(df=None):
    """
    Aggregates (activity + hazard + barrier_failure) combinations into
    ranked recurring precursor patterns with a naive period-over-period trend.
    """
    df = REPORTS_DF if df is None else df
    df = df.copy()
    df["pattern"] = df["activity"] + " + " + df["hazard"] + " + " + df["barrier_failure"]

    cutoff = df["date"].max() - timedelta(days=45)
    recent = df[df["date"] >= cutoff]
    older = df[df["date"] < cutoff]

    recent_counts = recent.groupby("pattern").size()
    older_counts = older.groupby("pattern").size()

    all_counts = df.groupby("pattern").agg(
        frequency=("pattern", "size"),
        avg_sif=("sif_score", "mean"),
        rule=("life_saving_rule", lambda x: x.mode()[0] if not x.mode().empty else ""),
        activity=("activity", lambda x: x.mode()[0] if not x.mode().empty else ""),
        hazard=("hazard", lambda x: x.mode()[0] if not x.mode().empty else ""),
    ).reset_index()

    def trend_pct(pattern):
        r = recent_counts.get(pattern, 0)
        o = older_counts.get(pattern, 0)
        if o == 0:
            return 100.0 if r > 0 else 0.0
        return round(((r - o) / o) * 100, 1)

    all_counts["trend_pct"] = all_counts["pattern"].apply(trend_pct)

    def _density(v):
        if v >= 75:
            return "High"
        elif v >= 50:
            return "Medium"
        return "Low/Medium"

    all_counts["risk_density"] = all_counts["avg_sif"].apply(_density)
    all_counts = all_counts.sort_values("frequency", ascending=False).reset_index(drop=True)
    return all_counts
