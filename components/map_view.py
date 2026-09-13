import folium
import streamlit as st
from folium.plugins import Fullscreen, MousePosition
from streamlit_folium import st_folium

from config.settings import RISK_BAND_COLORS
from src.data_manager import get_incidents


def show_risk_map(graph, risk_df, highlight_route=None, height=620):
    """Render पूर्वपथ's single operational map.

    The map is intentionally used only on the Risk Map page. It includes
    risk-colored corridors, location markers, incident markers, popups,
    layer controls, fullscreen, and automatic bounds fitting.
    """
    if graph.number_of_nodes() == 0:
        st.warning("No network locations are available.")
        return

    valid_nodes = []
    for node, data in graph.nodes(data=True):
        try:
            lat = float(data.get("latitude"))
            lon = float(data.get("longitude"))
            if -90 <= lat <= 90 and -180 <= lon <= 180:
                valid_nodes.append((node, lat, lon, data))
        except (TypeError, ValueError):
            continue

    if not valid_nodes:
        st.error("The network has no valid latitude/longitude coordinates.")
        return

    center_lat = sum(x[1] for x in valid_nodes) / len(valid_nodes)
    center_lon = sum(x[2] for x in valid_nodes) / len(valid_nodes)

    risk_map = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=7,
        tiles=None,
        control_scale=True,
        prefer_canvas=True,
    )

    # Base layers make the map usable for both operational and geographic context.
    folium.TileLayer(
        "OpenStreetMap",
        name="Street map",
        control=True,
        show=True,
    ).add_to(risk_map)
    folium.TileLayer(
        "CartoDB positron",
        name="Light map",
        control=True,
        show=False,
    ).add_to(risk_map)

    risk_lookup = {}
    if risk_df is not None and not risk_df.empty:
        for _, row in risk_df.iterrows():
            risk_lookup[frozenset((str(row["source"]), str(row["destination"])))] = row

    node_worst_band = {}
    band_rank = {"CRITICAL": 0, "HIGH": 1, "MODERATE": 2, "LOW": 3, "UNKNOWN": 4}

    road_layer = folium.FeatureGroup(name="Risk corridors", show=True)
    location_layer = folium.FeatureGroup(name="Locations", show=True)
    incident_layer = folium.FeatureGroup(name="Field incidents", show=True)

    for start, end, data in graph.edges(data=True):
        if start not in graph.nodes or end not in graph.nodes:
            continue
        try:
            start_xy = [float(graph.nodes[start]["latitude"]), float(graph.nodes[start]["longitude"])]
            end_xy = [float(graph.nodes[end]["latitude"]), float(graph.nodes[end]["longitude"])]
        except (KeyError, TypeError, ValueError):
            continue

        row = risk_lookup.get(frozenset((str(start), str(end))))
        band = str(row["risk_band"]) if row is not None else "UNKNOWN"
        score = row["risk_score"] if row is not None else "N/A"
        color = RISK_BAND_COLORS.get(band, RISK_BAND_COLORS["UNKNOWN"])

        for node in (start, end):
            current = node_worst_band.get(node, "UNKNOWN")
            if band_rank.get(band, 9) < band_rank.get(current, 9):
                node_worst_band[node] = band

        traffic = data.get("traffic", "Unknown")
        popup = (
            f"<b>{start} → {end}</b><br>"
            f"Risk score: <b>{score}</b><br>"
            f"Risk band: <b>{band}</b><br>"
            f"Traffic: {traffic}<br>"
            f"Distance: {data.get('distance', 'N/A')} km"
        )
        folium.PolyLine(
            [start_xy, end_xy],
            color=color,
            weight=7 if band in {"CRITICAL", "HIGH"} else 5,
            opacity=0.9,
            tooltip=f"{start} → {end} · {band} · {score}",
            popup=folium.Popup(popup, max_width=320),
        ).add_to(road_layer)

    for node, lat, lon, data in valid_nodes:
        band = node_worst_band.get(node, "UNKNOWN")
        color = RISK_BAND_COLORS.get(band, RISK_BAND_COLORS["UNKNOWN"])
        folium.CircleMarker(
            location=[lat, lon],
            radius=8,
            color="#ffffff",
            weight=2,
            fill=True,
            fill_color=color,
            fill_opacity=0.95,
            tooltip=node,
            popup=folium.Popup(
                f"<b>{node}</b><br>{data.get('state', 'Unknown')}<br>"
                f"Worst connected risk: <b>{band}</b>",
                max_width=260,
            ),
        ).add_to(location_layer)

    # Plot known demo incidents at their matching locations.
    incidents = get_incidents()
    location_lookup = {str(node).strip(): (lat, lon) for node, lat, lon, _ in valid_nodes}
    for _, incident in incidents.iterrows():
        name = str(incident.get("location", "")).strip()
        coords = location_lookup.get(name)
        if not coords:
            continue
        severity = str(incident.get("severity", "Unknown"))
        incident_type = str(incident.get("incident_type", "Incident"))
        folium.Marker(
            location=list(coords),
            tooltip=f"Incident · {name}",
            popup=folium.Popup(
                f"<b>{incident_type}</b><br>Location: {name}<br>"
                f"Severity: <b>{severity}</b>",
                max_width=280,
            ),
            icon=folium.Icon(color="red", icon="warning-sign"),
        ).add_to(incident_layer)

    road_layer.add_to(risk_map)
    location_layer.add_to(risk_map)
    incident_layer.add_to(risk_map)

    if highlight_route and len(highlight_route) > 1:
        route_coordinates = []
        for loc in highlight_route:
            if loc in graph.nodes:
                try:
                    route_coordinates.append([
                        float(graph.nodes[loc]["latitude"]),
                        float(graph.nodes[loc]["longitude"]),
                    ])
                except (KeyError, TypeError, ValueError):
                    pass
        if len(route_coordinates) > 1:
            folium.PolyLine(
                route_coordinates,
                color="#1f77b4",
                weight=8,
                opacity=0.9,
                tooltip="Selected route",
            ).add_to(risk_map)

    bounds = [[lat, lon] for _, lat, lon, _ in valid_nodes]
    risk_map.fit_bounds(bounds, padding=(30, 30))
    Fullscreen(position="topleft", title="Full screen", title_cancel="Exit full screen").add_to(risk_map)
    MousePosition(position="bottomleft", separator=" | ", prefix="Coordinates:").add_to(risk_map)
    folium.LayerControl(collapsed=False, position="topright").add_to(risk_map)

    st_folium(
        risk_map,
        width="100%",
        height=height,
        returned_objects=[],
        key="purva_path_risk_map",
    )
