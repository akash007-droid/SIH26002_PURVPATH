from datetime import datetime

import pandas as pd
import streamlit as st

from components.nav import page_header
from src.data_manager import get_locations

try:
    from streamlit_geolocation import streamlit_geolocation
except ImportError:
    streamlit_geolocation = None

st.set_page_config(page_title="Field Reports — पूर्वपथ", page_icon="📝", layout="wide")

page_header(
    "📝 Field Reports",
    "Capture geo-tagged incident reports from the field — road damage, "
    "landslides, floods, blockages and other disruptions.",
)

st.info(
    "Demo prototype: reports are stored only for this browser session. "
    "Use the location control to attach your device's current GPS coordinates "
    "to a report. Production deployment should add offline-first encrypted "
    "queueing and background sync."
)

# ---------------------------------------------------------------------
# Current location
# ---------------------------------------------------------------------
st.subheader("Report location")
if streamlit_geolocation is None:
    st.warning(
        "GPS location support is not installed. Run "
        "`python -m pip install streamlit-geolocation` and restart Streamlit."
    )
    gps = None
else:
    gps = streamlit_geolocation()

gps_lat = gps.get("latitude") if isinstance(gps, dict) else None
gps_lon = gps.get("longitude") if isinstance(gps, dict) else None
gps_accuracy = gps.get("accuracy") if isinstance(gps, dict) else None

if gps_lat is not None and gps_lon is not None:
    st.success(
        f"Current location captured: {float(gps_lat):.6f}, {float(gps_lon):.6f}"
        + (f" · accuracy ±{float(gps_accuracy):.0f} m" if gps_accuracy else "")
    )
else:
    st.caption(
        "Allow browser location access when prompted. You can still choose a "
        "known location manually if GPS is unavailable."
    )

locations = get_locations()
location_names = locations["location"].tolist() if not locations.empty else []

with st.form("field_report_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        location = st.selectbox(
            "Nearest / known location",
            ["— Select known location —"] + location_names,
            help="Used as a reference; the device GPS coordinates are stored with the report.",
        )
        incident_type = st.selectbox(
            "Incident Type",
            [
                "Landslide", "Flood", "Road Damage", "Bridge Damage",
                "Debris/Obstruction", "Traffic Congestion", "Other",
            ],
        )
    with col2:
        severity = st.select_slider(
            "Severity",
            options=["Low", "Medium", "High", "Critical"],
            value="Medium",
        )
        st.caption("Reporter identity is not collected. The report is geo-tagged from the device location.")

    description = st.text_area(
        "Description",
        placeholder="What did you observe?",
    )
    photo = st.file_uploader(
        "Attach photo (optional)",
        type=["jpg", "jpeg", "png"],
    )

    submitted = st.form_submit_button("📤 Submit Report", use_container_width=True)

    if submitted:
        known_location = "" if location == "— Select known location —" else location
        if gps_lat is None or gps_lon is None:
            st.warning(
                "Reporter location is required. Allow browser GPS access so पूर्वपथ "
                "can geo-tag this report."
            )
        elif not description.strip():
            st.warning("Please provide a description.")
        else:
            # Match the GPS point to the nearest known network location when possible.
            nearest_location = known_location
            nearest_distance_km = None
            try:
                import math
                if not nearest_location and not locations.empty:
                    lat1, lon1 = float(gps_lat), float(gps_lon)
                    best = None
                    for _, loc_row in locations.iterrows():
                        lat2 = float(loc_row.get("latitude"))
                        lon2 = float(loc_row.get("longitude"))
                        dlat = math.radians(lat2 - lat1)
                        dlon = math.radians(lon2 - lon1)
                        a = (
                            math.sin(dlat / 2) ** 2
                            + math.cos(math.radians(lat1))
                            * math.cos(math.radians(lat2))
                            * math.sin(dlon / 2) ** 2
                        )
                        distance_km = 6371.0 * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                        if best is None or distance_km < best[0]:
                            best = (distance_km, str(loc_row.get("location")))
                    if best:
                        nearest_distance_km, nearest_location = best
            except (TypeError, ValueError, KeyError):
                pass

            report = {
                "Submitted At": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Reporter Location": nearest_location or "GPS location",
                "Latitude": round(float(gps_lat), 6),
                "Longitude": round(float(gps_lon), 6),
                "GPS Accuracy (m)": round(float(gps_accuracy), 1) if gps_accuracy else None,
                "Nearest Network Location (km)": round(nearest_distance_km, 2) if nearest_distance_km is not None else None,
                "Type": incident_type,
                "Severity": severity,
                "Description": description.strip(),
                "Photo Attached": "Yes" if photo is not None else "No",
                "Status": "Submitted",
            }
            st.session_state.setdefault("field_reports", []).insert(0, report)
            st.success("Report submitted with location data.")

st.divider()
st.subheader("Recent Field Reports")

reports = st.session_state.get("field_reports", [])
if not reports:
    st.write("No field reports submitted yet in this session.")
else:
    report_df = pd.DataFrame(reports)
    st.dataframe(
        report_df,
        use_container_width=True,
        hide_index=True,
        height=380,
        column_config={
            "Latitude": st.column_config.NumberColumn(format="%.6f"),
            "Longitude": st.column_config.NumberColumn(format="%.6f"),
            "GPS Accuracy (m)": st.column_config.NumberColumn(format="%.1f"),
            "Description": st.column_config.TextColumn(width="large"),
        },
    )
