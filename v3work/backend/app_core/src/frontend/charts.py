"""
charts.py
---------
Plotly chart builders for the OIL SIF Precursor Intelligence Platform.
All charts share a common dark, industrial theme and use risk-semantic
colors consistently (see styles.COLORS).
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from src.frontend.styles import COLORS

FONT = dict(family="Inter, sans-serif", color=COLORS["text_secondary"], size=12)

BASE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=FONT,
    margin=dict(l=10, r=10, t=40, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    xaxis=dict(gridcolor=COLORS["border_soft"], zeroline=False),
    yaxis=dict(gridcolor=COLORS["border_soft"], zeroline=False),
)


def _apply_layout(fig, title=None, height=340, **overrides):
    layout = dict(BASE_LAYOUT)
    layout.update(overrides)
    fig.update_layout(**layout, height=height)
    if title:
        fig.update_layout(title=dict(text=title, font=dict(size=14, color=COLORS["text_primary"]), x=0))
    return fig


def sif_trend_chart(df):
    """Stacked area / line chart of High/Medium/Low SIF potential over time."""
    d = df.copy()
    d["week"] = d["date"].dt.to_period("W").apply(lambda p: p.start_time)
    grouped = d.groupby(["week", "sif_band"]).size().reset_index(name="count")
    pivot = grouped.pivot(index="week", columns="sif_band", values="count").fillna(0)
    for band in ["Low", "Medium", "High"]:
        if band not in pivot.columns:
            pivot[band] = 0
    pivot = pivot[["Low", "Medium", "High"]].sort_index()

    fig = go.Figure()
    color_map = {"High": COLORS["critical"], "Medium": COLORS["elevated"], "Low": COLORS["controlled"]}
    for band in ["Low", "Medium", "High"]:
        fig.add_trace(go.Scatter(
            x=pivot.index, y=pivot[band], name=band, mode="lines",
            stackgroup="one", line=dict(width=0.5, color=color_map[band]),
            fillcolor=color_map[band],
            hovertemplate="%{y} reports<extra>" + band + "</extra>",
        ))
    return _apply_layout(fig, height=320)


def sif_distribution_donut(df):
    counts = df["sif_band"].value_counts()
    order = ["High", "Medium", "Low"]
    values = [counts.get(b, 0) for b in order]
    colors = [COLORS["critical"], COLORS["elevated"], COLORS["controlled"]]
    fig = go.Figure(go.Pie(
        labels=order, values=values, hole=0.62,
        marker=dict(colors=colors, line=dict(color=COLORS["bg"], width=2)),
        textinfo="percent", textfont=dict(color=COLORS["text_primary"], size=12),
    ))
    return _apply_layout(fig, height=300, showlegend=True)


def risk_by_category_bar(df, category_col, top_n=8, horizontal=True):
    grp = df.groupby(category_col)["sif_score"].mean().sort_values(ascending=True).tail(top_n)
    colors = [COLORS["critical"] if v >= 75 else COLORS["elevated"] if v >= 50 else COLORS["controlled"]
              for v in grp.values]
    fig = go.Figure(go.Bar(
        x=grp.values if horizontal else grp.index,
        y=grp.index if horizontal else grp.values,
        orientation="h" if horizontal else "v",
        marker=dict(color=colors),
        text=[f"{v:.0f}" for v in grp.values],
        textposition="outside",
        textfont=dict(color=COLORS["text_secondary"]),
    ))
    return _apply_layout(fig, height=max(280, 34 * len(grp)))


def report_volume_by_type(df):
    grp = df["report_type"].value_counts()
    fig = go.Figure(go.Bar(
        x=grp.index, y=grp.values,
        marker=dict(color=COLORS["accent"]),
        text=grp.values, textposition="outside",
        textfont=dict(color=COLORS["text_secondary"]),
    ))
    return _apply_layout(fig, height=300)


def precursor_trend_chart(df, site=None, hazard=None):
    """Time series for the emerging-risk narrative on a given site/hazard."""
    d = df.copy()
    if site:
        d = d[d["site"] == site]
    if hazard:
        d = d[d["hazard"] == hazard]
    d["week"] = d["date"].dt.to_period("W").apply(lambda p: p.start_time)
    grouped = d.groupby("week").size().reset_index(name="count")
    fig = go.Figure(go.Scatter(
        x=grouped["week"], y=grouped["count"], mode="lines+markers",
        line=dict(color=COLORS["critical"], width=2.5),
        marker=dict(size=6, color=COLORS["critical"]),
        fill="tozeroy", fillcolor=f"{COLORS['critical']}22",
    ))
    return _apply_layout(fig, height=280)


def barrier_failure_bar(df):
    grp = df.sort_values("occurrences", ascending=True)
    colors = [COLORS["critical"] if v >= 75 else COLORS["elevated"] if v >= 50 else COLORS["controlled"]
              for v in grp["avg_sif"]]
    fig = go.Figure(go.Bar(
        x=grp["occurrences"], y=grp["critical_barrier"], orientation="h",
        marker=dict(color=colors),
        text=grp["occurrences"], textposition="outside",
        textfont=dict(color=COLORS["text_secondary"]),
        customdata=grp["avg_sif"].round(0),
        hovertemplate="%{y}<br>%{x} occurrences<br>Avg SIF score: %{customdata}<extra></extra>",
    ))
    return _apply_layout(fig, height=max(260, 40 * len(grp)))


def site_risk_scatter(site_df):
    fig = go.Figure(go.Scatter(
        x=site_df["total_reports"], y=site_df["risk_score"],
        mode="markers+text",
        marker=dict(
            size=site_df["high_sif"].clip(lower=6) * 1.6,
            color=site_df["risk_score"],
            colorscale=[[0, COLORS["controlled"]], [0.55, COLORS["elevated"]], [1, COLORS["critical"]]],
            cmin=0, cmax=100,
            line=dict(width=1, color=COLORS["bg"]),
            showscale=False,
        ),
        text=site_df["site"].str.replace(" ", "\n", n=1),
        textposition="top center",
        textfont=dict(size=9, color=COLORS["text_secondary"]),
        hovertext=site_df["site"],
        hovertemplate="%{hovertext}<br>Reports: %{x}<br>Risk score: %{y:.0f}<extra></extra>",
    ))
    fig.update_layout(
        xaxis_title="Total Reports", yaxis_title="Avg SIF Risk Score",
    )
    return _apply_layout(fig, height=380)


def lsr_bar(lsr_df):
    grp = lsr_df.sort_values("reports", ascending=True)
    colors = [COLORS["critical"] if v >= 75 else COLORS["elevated"] if v >= 50 else COLORS["controlled"]
              for v in grp["avg_sif"]]
    fig = go.Figure(go.Bar(
        x=grp["reports"], y=grp["rule"], orientation="h",
        marker=dict(color=colors),
        text=grp["reports"], textposition="outside",
        textfont=dict(color=COLORS["text_secondary"]),
    ))
    return _apply_layout(fig, height=max(280, 42 * len(grp)))


def site_sif_trend(site_df):
    d = site_df.copy()
    d["week"] = d["date"].dt.to_period("W").apply(lambda p: p.start_time)
    grouped = d.groupby("week")["sif_score"].mean().reset_index()
    fig = go.Figure(go.Scatter(
        x=grouped["week"], y=grouped["sif_score"], mode="lines+markers",
        line=dict(color=COLORS["accent"], width=2.5),
        marker=dict(size=5, color=COLORS["accent"]),
        fill="tozeroy", fillcolor=f"{COLORS['accent']}1A",
    ))
    return _apply_layout(fig, height=260)


def activity_ranking_bar(df):
    grp = df["activity"].value_counts().sort_values(ascending=True)
    fig = go.Figure(go.Bar(
        x=grp.values, y=grp.index, orientation="h",
        marker=dict(color=COLORS["accent"]),
        text=grp.values, textposition="outside",
        textfont=dict(color=COLORS["text_secondary"]),
    ))
    return _apply_layout(fig, height=max(260, 34 * len(grp)))
