import streamlit as st

from components.nav import page_header
from components.map_view import show_risk_map
from src.graph import create_graph
from src.simulation import update_traffic
from src.data_manager import get_incidents
from src.risk import compute_network_risk
from config.settings import RISK_BAND_COLORS, RISK_THRESHOLDS

st.set_page_config(page_title="Risk Map — पूर्वपथ", page_icon="🗺️", layout="wide")

page_header(
    "🗺️ Risk Map",
    "Live disruption-risk view of every road corridor in the network. "
    "This is the only map in पूर्वपथ — all other features link back here "
    "for spatial context instead of duplicating separate maps.",
)

# Keep a simulated-traffic graph in session state so the map doesn't
# re-randomize on every unrelated interaction/rerun.
if "risk_map_graph" not in st.session_state:
    st.session_state["risk_map_graph"] = create_graph()

col_a, col_b = st.columns([1, 3])
with col_a:
    if st.button("🔄 Simulate Live Conditions", use_container_width=True):
        st.session_state["risk_map_graph"] = update_traffic(create_graph())

graph = st.session_state["risk_map_graph"]
incidents = get_incidents()
risk_df = compute_network_risk(graph, incidents)

if risk_df.empty:
    st.error("Not enough road network data available to compute risk.")
    st.stop()

critical = risk_df[risk_df["risk_band"] == "CRITICAL"]
high = risk_df[risk_df["risk_band"] == "HIGH"]

m1, m2, m3, m4 = st.columns(4)
m1.metric("Corridors Monitored", len(risk_df))
m2.metric("Critical", len(critical))
m3.metric("High", len(high))
m4.metric("Avg Risk Score", round(risk_df["risk_score"].mean(), 1))

st.caption(
    f"Risk bands — LOW: 0–{RISK_THRESHOLDS['LOW']} · "
    f"MODERATE: {RISK_THRESHOLDS['LOW']+1}–{RISK_THRESHOLDS['MODERATE']} · "
    f"HIGH: {RISK_THRESHOLDS['MODERATE']+1}–{RISK_THRESHOLDS['HIGH']} · "
    f"CRITICAL: {RISK_THRESHOLDS['HIGH']+1}–100. "
    "Thresholds are placeholder/configurable (see config/settings.py) until "
    "calibrated against real pilot outcomes."
)

legend_cols = st.columns(4)
for col, band in zip(legend_cols, ["LOW", "MODERATE", "HIGH", "CRITICAL"]):
    color = RISK_BAND_COLORS[band]
    col.markdown(
        f"<span style='display:inline-block;width:12px;height:12px;"
        f"border-radius:50%;background:{color};margin-right:6px;'></span>{band}",
        unsafe_allow_html=True,
    )

show_risk_map(graph, risk_df)

if not critical.empty:
    st.error(f"⚠ {len(critical)} corridor(s) currently at CRITICAL disruption risk.")

st.subheader("Corridor Risk Table")
band_filter = st.multiselect(
    "Filter by risk band",
    ["CRITICAL", "HIGH", "MODERATE", "LOW"],
    default=["CRITICAL", "HIGH", "MODERATE", "LOW"],
)
filtered = risk_df[risk_df["risk_band"].isin(band_filter)]
st.dataframe(filtered, use_container_width=True, hide_index=True)
