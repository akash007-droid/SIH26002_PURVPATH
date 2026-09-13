import streamlit as st

from components.nav import page_header
from src.graph import create_graph
from src.data_manager import get_incidents, get_vehicles, get_stock
from src.inventory import calculate_shortage_alerts
from src.risk import compute_network_risk

st.set_page_config(page_title="Alerts Center — पूर्वपथ", page_icon="🔔", layout="wide")

page_header(
    "🔔 Alerts Center",
    "A single feed of everything that needs attention right now — high-risk "
    "corridors, active field incidents and critical stock shortages.",
)

if "acknowledged_alerts" not in st.session_state:
    st.session_state["acknowledged_alerts"] = set()

graph = create_graph()
incidents = get_incidents()
vehicles = get_vehicles()
stock = get_stock()

risk_df = compute_network_risk(graph, incidents)
shortage_df = calculate_shortage_alerts(stock, vehicles, graph) if not stock.empty else None

alerts = []

for _, row in risk_df[risk_df["risk_band"].isin(["CRITICAL", "HIGH"])].iterrows():
    alerts.append({
        "id": f"risk::{row['source']}-{row['destination']}",
        "severity": row["risk_band"],
        "category": "Corridor Risk",
        "title": f"{row['source']} → {row['destination']} at {row['risk_band']} risk ({row['risk_score']})",
        "detail": f"Traffic: {row['traffic']} · Incident flagged: {'Yes' if row['incident_flagged'] else 'No'}",
    })

for _, row in incidents.iterrows():
    severity = str(row.get("severity", "Medium")).upper()
    alerts.append({
        "id": f"incident::{row.get('incident_id', row.get('location'))}",
        "severity": severity if severity in ("LOW", "MEDIUM", "HIGH", "CRITICAL") else "MEDIUM",
        "category": "Field Incident",
        "title": f"{row.get('incident_type', 'Incident')} at {row.get('location', 'Unknown')}",
        "detail": f"Incident ID: {row.get('incident_id', 'N/A')}",
    })

if shortage_df is not None and not shortage_df.empty:
    for _, row in shortage_df[shortage_df["risk_level"].isin(["Critical", "Warning"])].iterrows():
        alerts.append({
            "id": f"stock::{row['location']}-{row['item']}",
            "severity": "CRITICAL" if row["risk_level"] == "Critical" else "HIGH",
            "category": "Stock Shortage",
            "title": f"{row['item']} at {row['location']} — {row['days_remaining']} days remaining",
            "detail": "Incoming shipment assigned" if row["incoming_vehicle"] else "No shipment currently assigned",
        })

severity_rank = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
alerts.sort(key=lambda a: severity_rank.get(a["severity"], 4))

active_alerts = [a for a in alerts if a["id"] not in st.session_state["acknowledged_alerts"]]
ack_count = len(alerts) - len(active_alerts)

m1, m2, m3 = st.columns(3)
m1.metric("Total Alerts", len(alerts))
m2.metric("Active", len(active_alerts))
m3.metric("Acknowledged", ack_count)

st.divider()

if not active_alerts:
    st.success("No active alerts. Everything acknowledged or nothing critical right now.")
else:
    for alert in active_alerts:
        box = {
            "CRITICAL": st.error,
            "HIGH": st.warning,
            "MEDIUM": st.info,
            "LOW": st.info,
        }.get(alert["severity"], st.info)

        with st.container(border=True):
            col1, col2 = st.columns([5, 1])
            with col1:
                box(f"**[{alert['category']}] {alert['title']}**\n\n{alert['detail']}")
            with col2:
                if st.button("Acknowledge", key=alert["id"]):
                    st.session_state["acknowledged_alerts"].add(alert["id"])
                    st.rerun()
