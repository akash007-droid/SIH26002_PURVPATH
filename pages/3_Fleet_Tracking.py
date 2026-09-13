import pandas as pd
import streamlit as st

from components.nav import page_header
from src.data_manager import get_vehicles, get_stock
from src.graph import create_graph
from src.inventory import calculate_shortage_alerts

st.set_page_config(page_title="Fleet & Supply Tracking — पूर्वपथ", page_icon="🚛", layout="wide")

page_header(
    "🚛 Fleet & Essential Goods Tracking",
    "Monitor vehicles carrying essential commodities and get shortage alerts "
    "at destinations before local stock runs out.",
)

vehicles = get_vehicles()

if vehicles.empty:
    st.warning("No vehicle data available.")
    st.stop()

total_vehicles = len(vehicles)
col1, col2, col3 = st.columns(3)
col1.metric("Total Vehicles", total_vehicles)

if "status" in vehicles.columns:
    active = len(vehicles[vehicles["status"].astype(str).str.lower() == "active"])
    col2.metric("Active Vehicles", active)
    col3.metric("Inactive Vehicles", total_vehicles - active)

st.divider()
st.subheader("🚚 Vehicles & Cargo In Transit")
display_cols = [
    c for c in [
        "vehicle_id", "type", "status", "current_location",
        "destination", "cargo_category", "cargo_item", "quantity", "unit",
    ]
    if c in vehicles.columns
]
st.dataframe(vehicles[display_cols], use_container_width=True, hide_index=True)

st.divider()
st.subheader("💊 Essential Goods Shortage Alerts")

stock = get_stock()
if stock.empty:
    st.info("No destination stock data available. Add data/stock.csv.")
    st.stop()

graph = create_graph()
alerts = calculate_shortage_alerts(stock, vehicles, graph)

if alerts.empty:
    st.success("No shortage data to display.")
    st.stop()

critical = alerts[alerts["risk_level"] == "Critical"]
warning = alerts[alerts["risk_level"] == "Warning"]

m1, m2, m3 = st.columns(3)
m1.metric("Critical Shortages", len(critical))
m2.metric("Warning Level", len(warning))
m3.metric("Locations Tracked", alerts["location"].nunique())

for _, row in alerts.iterrows():
    label = f"{row['location']} — {row['item']} ({row['days_remaining']} days of stock left)"

    if row["risk_level"] == "Critical":
        box = st.error
    elif row["risk_level"] == "Warning":
        box = st.warning
    else:
        box = st.success

    if pd.notna(row["incoming_vehicle"]):
        eta_text = (
            f"Incoming: {row['incoming_qty']} units via {row['incoming_vehicle']}, "
            f"ETA {row['eta_days']} days — "
            + (
                "will arrive in time."
                if row["will_arrive_in_time"]
                else "⚠ will NOT arrive before stock runs out."
            )
        )
    else:
        eta_text = "No shipment currently assigned to this shortage."

    box(f"**{label}**\n\n{eta_text}")

st.divider()
st.subheader("📋 Full Shortage Table")
st.dataframe(alerts, use_container_width=True, hide_index=True)
