import streamlit as st
import base64
from pathlib import Path

from config.settings import APP_NAME, APP_ICON

# Supplied Purv Path logo
_logo_path = Path(__file__).parent / "assets" / "purv_path_logo.jpeg"
try:
    _logo_b64 = base64.b64encode(_logo_path.read_bytes()).decode("ascii")
    LOGO_HTML = f'<img src="data:image/jpeg;base64,{_logo_b64}" alt="Purv Path logo" />'
except Exception:
    LOGO_HTML = '<span>✦</span>'

from components.nav import inject_theme
from src.graph import create_graph, get_graph_summary
from src.data_manager import get_incidents, get_vehicles, get_stock
from src.inventory import calculate_shortage_alerts
from src.risk import compute_network_risk
from components.map_view import show_risk_map

st.set_page_config(
    page_title=f"{APP_NAME} Dashboard",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_theme()

# ---------------------------------------------------------------------
# Dashboard data
# ---------------------------------------------------------------------
graph = create_graph()
summary = get_graph_summary(graph)
incidents = get_incidents()
vehicles = get_vehicles()
stock = get_stock()
risk_df = compute_network_risk(graph, incidents)

critical_corridors = (
    len(risk_df[risk_df["risk_band"] == "CRITICAL"]) if not risk_df.empty else 0
)
critical_stock = 0
if not stock.empty:
    alerts = calculate_shortage_alerts(stock, vehicles, graph)
    if not alerts.empty:
        critical_stock = len(alerts[alerts["risk_level"] == "Critical"])

# ---------------------------------------------------------------------
# Header — compact, aligned like the reference dashboard
# ---------------------------------------------------------------------
st.markdown(
    f"""
    <div class="pp-dashboard-header">
      <div class="pp-dashboard-brand">
        <div class="pp-brand-mark">{LOGO_HTML}</div>
        <div>
          <div class="pp-dashboard-name">{APP_NAME}</div>
          <div class="pp-dashboard-tagline">Safer Roads&nbsp;&nbsp; Stronger Communities</div>
        </div>
      </div>
      <div class="pp-top-navigation">
        <span class="pp-top-nav active">⌂&nbsp;&nbsp; Dashboard</span>
        <span class="pp-top-nav">♧&nbsp;&nbsp; Map</span>
        <span class="pp-top-nav">▤&nbsp;&nbsp; Field Reports</span>
        <span class="pp-top-nav">♟&nbsp;&nbsp; Alerts</span>
        <span class="pp-top-nav">▥&nbsp;&nbsp; Analytics</span>
      </div>
      <div class="pp-header-actions">
        <span class="pp-bell">♧<i>{len(incidents)}</i></span>
        <a class="pp-help" href="tel:+919321127701">☎ <span>North East Helpline<br><b>+91 93211 27701</b></span></a>
        <span class="pp-avatar">●</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------
# Main two-panel dashboard
# ---------------------------------------------------------------------
left, right = st.columns([1, 1], gap="medium")

with left:
    st.markdown(
        """
        <div class="pp-panel pp-input-panel">
          <div class="pp-panel-heading">
            <div class="pp-panel-icon">⌖</div>
            <div><div class="pp-panel-title">Location Input</div>
            <div class="pp-panel-sub">Enter a location or use your current location</div></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    input_col, loc_col = st.columns([1.72, .72], gap="small")
    with input_col:
        location = st.text_input(
            "Location",
            value="Guwahati, Assam",
            label_visibility="collapsed",
            placeholder="Enter location name (e.g., Guwahati, Assam)",
            key="dashboard_location",
        )
    with loc_col:
        st.button("⌖  Use Current Location", use_container_width=True, key="current_location")

    detected = location.strip() or "Guwahati, Assam"
    default_lat, default_lon = 26.1445, 91.7362

    st.markdown(
        f"""
        <div class="pp-location-stats">
          <div class="pp-location-stat"><span>⌾</span><small>Latitude</small><b>{default_lat:.4f}° N</b></div>
          <div class="pp-location-stat"><span>⌖</span><small>Longitude</small><b>{default_lon:.4f}° E</b></div>
          <div class="pp-location-stat detected"><span>♧</span><small>Location Detected</small><b>{detected}</b></div>
        </div>

        <div class="pp-query-heading">
          <div class="pp-query-icon">☁</div>
          <div><div class="pp-panel-title">What U What to explore?</div>
          <div class="pp-panel-sub">Choose a query or ask anything about the region</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    items = [
        ("☁", "Weather & Climate", "Get current weather, forecast and alerts", "pages/6_Analytics.py"),
        ("⚠", "Road Conditions", "Check road status, closures and hazards", "pages/1_Risk_Map.py"),
        ("▣", "Recent Incidents", "View latest incidents and risk areas", "pages/5_Alerts.py"),
        ("⌘", "Network Health", "Check connectivity and service status", "pages/6_Analytics.py"),
        ("⌗", "Route Planning", "Get safer and optimized routes", "pages/2_Route_Optimizer.py"),
        ("▤", "Field Reports", "Submit or view field updates", "pages/4_Field_Reports.py"),
    ]

    for idx, (icon, title, desc, page) in enumerate(items):
        a, b = st.columns([.95, .05], gap="small")
        with a:
            st.markdown(
                f"""
                <div class="pp-query-row">
                  <div class="pp-query-icon-small">{icon}</div>
                  <div><div class="pp-query-title">{title}</div><div class="pp-query-desc">{desc}</div></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with b:
            st.page_link(page, label="›")

with right:
    st.markdown(
        """
        <div class="pp-panel pp-output-panel">
          <div class="pp-output-heading">
            <div class="pp-panel-heading">
              <div class="pp-panel-icon">♟</div>
              <div><div class="pp-panel-title">What would you like to explore?</div>
              <div class="pp-panel-sub">AI-powered insights for your location</div></div>
            </div>
            <a class="pp-contact" href="tel:+919321127701">☎&nbsp; Tap to Contact</a>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    w, r, i, n = st.columns(4, gap="small")
    with w:
        st.markdown('<div class="pp-output-card blue"><small>☁&nbsp; Weather</small><strong>24°C</strong><span>☁ Light Rain</span></div>', unsafe_allow_html=True)
    with r:
        road_state = "Moderate" if critical_corridors or not risk_df.empty else "Good"
        st.markdown(f'<div class="pp-output-card amber"><small>⚠&nbsp; Road Condition</small><strong>{road_state}</strong><span>Some blockages</span></div>', unsafe_allow_html=True)
    with i:
        st.markdown(f'<div class="pp-output-card red"><small>⚠&nbsp; Incidents</small><strong>{len(incidents)}</strong><span>Active</span></div>', unsafe_allow_html=True)
    with n:
        st.markdown('<div class="pp-output-card green"><small>▥&nbsp; Network Health</small><strong>Good</strong><span>All services active</span></div>', unsafe_allow_html=True)

    # Map is intentionally contained inside the same visual output area.
    st.markdown('<div class="pp-map-wrap">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="pp-map-overlay"><b>{detected}</b><span>{default_lat:.4f}° N, {default_lon:.4f}° E</span></div>',
        unsafe_allow_html=True,
    )
    show_risk_map(graph, risk_df, height=345)
    st.markdown('</div>', unsafe_allow_html=True)

    risk_label = "Moderate" if critical_corridors or not risk_df.empty else "Low"
    blockage_text = "including one road blockage near Basistha" if len(incidents) else "with no reported road blockage"
    st.markdown(
        f"""
        <div class="pp-ai-result">
          <div class="pp-ai-badge">AI</div>
          <div><b>AI Analysis Result</b>
          <p>The area around <strong>{detected}</strong> is experiencing light to moderate rainfall. There are <strong>{len(incidents)}</strong> active incidents, {blockage_text}. The overall risk level is <mark>{risk_label}</mark>. It is advisable to avoid affected routes and follow official updates.</p></div>
        </div>
        </div>
""",
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------
# Prompt bar
# ---------------------------------------------------------------------
prompt_info, prompt_input, prompt_action = st.columns([.40, .55, .05], gap="small")
with prompt_info:
    st.markdown(
        """
        <div class="pp-prompt-label pp-prompt-label-inline">
          <div class="pp-prompt-icon">ϟ</div>
          <div><b>Prompt</b><small>Ask about the region, weather, roads, or incidents.</small></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with prompt_input:
    st.text_input(
        "Prompt",
        value="What is the weather forecast for Guwahati in the next 3 days?",
        label_visibility="collapsed",
        key="dashboard_prompt",
    )
with prompt_action:
    st.button("→", use_container_width=True, key="prompt_submit")
