import streamlit as st
import pandas as pd

from components.nav import page_header
from src.graph import create_graph
from src.simulation import update_traffic
from services.route_service import optimize_route
from components.charts import show_convergence_chart

st.set_page_config(page_title="Route Optimizer — पूर्वपथ", page_icon="🧭", layout="wide")

page_header(
    "🧭 Intelligent Route Optimizer",
    "Compare classical (Dijkstra) and quantum-inspired (QPSO) route search "
    "between any two locations.",
)

graph = create_graph()
locations = list(graph.nodes())

if len(locations) < 2:
    st.error("Not enough locations available in the transportation network.")
    st.stop()

col1, col2, col3 = st.columns(3)

with col1:
    source = st.selectbox("Source Location", locations)

with col2:
    destination = st.selectbox(
        "Destination Location",
        locations,
        index=min(1, len(locations) - 1),
        key="route_destination",
    )

with col3:
    algorithm = st.selectbox("Optimization Algorithm", ["Dijkstra", "Quantum PSO"])

simulate = st.checkbox("Enable Dynamic Traffic Simulation", value=True)
st.caption("Traffic simulation is demo data. Replace it with live feeds before production use.")

if st.button("🚀 Optimize Route", use_container_width=True):
    if source == destination:
        st.warning("Please select different source and destination locations.")
        st.stop()

    if simulate:
        graph = update_traffic(graph)

    with st.spinner("Optimizing route..."):
        result = optimize_route(graph, source, destination, algorithm)

    if result.get("route"):
        st.success(f"Optimal Route Generated using {result['algorithm']}")

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Travel Cost", f"{result['distance']} km-equivalent")
        c2.metric("Risk Score", f"{result['risk']['risk_score']}%")
        c3.metric("Risk Level", result["risk"]["risk_level"])

        st.subheader("Optimized Route")
        st.write(" → ".join(result["route"]))
        st.page_link(
            "pages/1_Risk_Map.py",
            label="View this corridor's live risk levels on the Risk Map",
            icon="🗺️",
        )

        route_data = []
        for i in range(len(result["route"]) - 1):
            start = result["route"][i]
            end = result["route"][i + 1]
            edge = graph[start][end]

            route_data.append({
                "From": start,
                "To": end,
                "Distance (km)": round(edge.get("distance", 0), 2),
                "Traffic": edge.get("traffic", "Unknown"),
            })

        st.subheader("Route Details")
        st.dataframe(pd.DataFrame(route_data), use_container_width=True)

        if algorithm == "Quantum PSO":
            st.subheader("Quantum-Inspired Optimization Convergence")
            show_convergence_chart(result.get("convergence", []))
    else:
        st.error("No route could be generated.")
