import pandas as pd
import streamlit as st

from components.nav import page_header
from src.data_manager import get_roads, get_incidents

st.set_page_config(page_title="Analytics — पूर्वपथ", page_icon="📊", layout="wide")

page_header(
    "📊 Logistics Analytics",
    "A readable operational view of network coverage, risk signals, and reported incidents.",
)

roads = get_roads()
incidents = get_incidents()

# ---------------------------------------------------------------------
# Network overview
# ---------------------------------------------------------------------
total_roads = len(roads)
total_incidents = len(incidents)

high_critical_incidents = 0
if not incidents.empty and "severity" in incidents.columns:
    high_critical_incidents = int(
        incidents["severity"]
        .astype(str)
        .str.strip()
        .str.upper()
        .isin({"HIGH", "CRITICAL"})
        .sum()
    )

k1, k2, k3 = st.columns(3)
k1.metric("Road Corridors", total_roads)
k2.metric("Recorded Incidents", total_incidents)
k3.metric("High / Critical Incidents", high_critical_incidents)

st.divider()

# ---------------------------------------------------------------------
# Incident analysis — intentionally narrow and scannable instead of a
# wide raw-data table.
# ---------------------------------------------------------------------
st.subheader("Incident Analysis")

if incidents.empty:
    st.success("No incident data available.")
else:
    incident_view = incidents.copy()
    incident_view.columns = [
        str(c).strip().replace("_", " ").title() for c in incident_view.columns
    ]

    severity_col = next((c for c in incident_view.columns if c.lower() == "severity"), None)
    type_col = next((c for c in incident_view.columns if c.lower() in {"incident type", "type"}), None)
    location_col = next((c for c in incident_view.columns if c.lower() == "location"), None)

    f1, f2 = st.columns(2)
    with f1:
        severity_options = (
            sorted(incident_view[severity_col].dropna().astype(str).unique().tolist())
            if severity_col else []
        )
        selected_severity = st.multiselect(
            "Severity",
            severity_options,
            default=severity_options,
        )
    with f2:
        type_options = (
            sorted(incident_view[type_col].dropna().astype(str).unique().tolist())
            if type_col else []
        )
        selected_types = st.multiselect(
            "Incident type",
            type_options,
            default=type_options,
        )

    filtered = incident_view
    if severity_col and selected_severity:
        filtered = filtered[filtered[severity_col].astype(str).isin(selected_severity)]
    if type_col and selected_types:
        filtered = filtered[filtered[type_col].astype(str).isin(selected_types)]

    # Show the most useful fields first and keep the table compact.
    preferred = [location_col, type_col, severity_col]
    preferred = [c for c in preferred if c and c in filtered.columns]
    remaining = [c for c in filtered.columns if c not in preferred]
    display_cols = preferred + remaining

    st.caption(f"Showing {len(filtered)} of {len(incident_view)} recorded incidents.")
    st.dataframe(
        filtered[display_cols],
        use_container_width=True,
        hide_index=True,
        height=360,
        column_config={
            c: st.column_config.TextColumn(c, width="medium")
            for c in display_cols
        },
    )

st.divider()

# ---------------------------------------------------------------------
# Top 9 accuracy improvements
# ---------------------------------------------------------------------
st.divider()
st.subheader("Top 9 Accuracy Improvements")
st.caption(
    "Recommended upgrades to move पूर्वपथ from a prototype dashboard "
    "toward a reliable, evidence-based operational decision system."
)

accuracy_ideas = [
    ("01", "Live Weather", "Connect verified weather and rainfall feeds so risk reacts to real conditions."),
    ("02", "Road Conditions", "Ingest closures, landslides, flooding, maintenance and road-condition reports."),
    ("03", "GPS Telemetry", "Use real vehicle speed, position and travel-time data instead of assumed movement."),
    ("04", "Geospatial Matching", "Snap every incident to the correct road segment and calculate nearby exposure."),
    ("05", "Historical Learning", "Train and validate risk models using previous incidents and their actual outcomes."),
    ("06", "Time Decay", "Give fresh incidents more weight and gradually reduce the impact of old reports."),
    ("07", "Risk Confidence", "Show a confidence score alongside LOW, MODERATE, HIGH or CRITICAL risk."),
    ("08", "Data Freshness", "Display source, last-updated time and feed health so operators know how current data is."),
    ("09", "Field Validation", "Let field teams confirm, reject or resolve alerts and feed those outcomes back into the model."),
]

for row_start in range(0, len(accuracy_ideas), 3):
    cols = st.columns(3)
    for col, (num, title, desc) in zip(cols, accuracy_ideas[row_start:row_start + 3]):
        with col:
            st.markdown(
                f"""
                <div style="
                    border:1px solid rgba(70,160,190,.25);
                    border-radius:14px;
                    padding:16px;
                    min-height:145px;
                    margin-bottom:14px;
                    background:linear-gradient(135deg, rgba(15,45,62,.72), rgba(8,25,38,.72));
                    box-shadow:0 8px 24px rgba(0,0,0,.12);
                ">
                    <div style="font-size:12px;font-weight:700;letter-spacing:1px;
                                color:#6ee7c8;margin-bottom:8px;">{num}</div>
                    <div style="font-size:17px;font-weight:700;color:#f5fbff;margin-bottom:7px;">
                        {title}
                    </div>
                    <div style="font-size:12px;line-height:1.55;color:#9fb4c2;">
                        {desc}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

st.info(
    "SIH-ready target: combine verified weather + road + incident + GPS + historical "
    "data into one explainable risk score, then validate every alert with field feedback."
)

# ---------------------------------------------------------------------
# Accuracy note
# ---------------------------------------------------------------------
st.subheader("Data Quality")
st.caption(
    "Analytics currently reflect the records available in the project data files. "
    "For production deployment, connect verified live feeds and historical outcomes "
    "before treating risk scores as predictive."
)
