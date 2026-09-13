import pandas as pd

from config.settings import RISK_THRESHOLDS

TRAFFIC_BASE_SCORE = {"low": 20, "medium": 50, "high": 80}
INCIDENT_PENALTY = 15


def _incident_lookup(incidents):
    """Build a set of incident-flagged locations and corridors (pairs of
    locations) from the incidents table, e.g. 'Guwahati-Tezpur' -> corridor."""
    locations = set()
    corridors = set()
    if incidents is not None and not incidents.empty and "location" in incidents.columns:
        locations = set(
            incidents["location"].astype(str).str.strip().tolist()
        )
        for name in locations:
            parts = [p.strip() for p in name.replace("–", "-").split("-")]
            if len(parts) == 2:
                corridors.add(frozenset(parts))
    return locations, corridors


def risk_band(score):
    """Map a 0-100 risk score to a band using the configurable thresholds
    in config.settings.RISK_THRESHOLDS. These cut points are placeholders
    until they can be calibrated against real pilot outcomes."""
    if score <= RISK_THRESHOLDS["LOW"]:
        return "LOW"
    if score <= RISK_THRESHOLDS["MODERATE"]:
        return "MODERATE"
    if score <= RISK_THRESHOLDS["HIGH"]:
        return "HIGH"
    return "CRITICAL"


def score_segment(traffic, has_incident):
    """Rule-based 0-100 disruption-risk score for a single road segment.
    This stands in for the trained XGBoost disruption model described in
    the platform PRD until real historical training data is available."""
    score = TRAFFIC_BASE_SCORE.get(str(traffic).strip().lower(), 50)
    if has_incident:
        score = min(100, score + INCIDENT_PENALTY)
    return score


def compute_network_risk(graph, incidents=None):
    """Return a DataFrame with one row per road segment (edge), scored for
    disruption risk. Used by the Risk Map page and by home-page KPIs."""
    incident_locations, incident_corridors = _incident_lookup(incidents)

    rows = []
    for start, end, data in graph.edges(data=True):
        traffic = data.get("traffic", "Medium")
        has_incident = (
            start in incident_locations
            or end in incident_locations
            or frozenset((start, end)) in incident_corridors
        )
        score = score_segment(traffic, has_incident)

        rows.append({
            "source": start,
            "destination": end,
            "distance_km": round(data.get("distance", 0), 2),
            "traffic": traffic,
            "incident_flagged": has_incident,
            "risk_score": score,
            "risk_band": risk_band(score),
        })

    if not rows:
        return pd.DataFrame(
            columns=["source", "destination", "distance_km", "traffic",
                     "incident_flagged", "risk_score", "risk_band"]
        )

    band_order = {"CRITICAL": 0, "HIGH": 1, "MODERATE": 2, "LOW": 3}
    result = pd.DataFrame(rows)
    result["_sort"] = result["risk_band"].map(band_order)
    result = result.sort_values(
        ["_sort", "risk_score"], ascending=[True, False]
    ).drop(columns="_sort").reset_index(drop=True)
    return result


def calculate_route_risk(graph, route, incidents=None):
    if not route or len(route) < 2:
        return {"risk_score": 0, "risk_level": "Unknown"}

    risk_values = {"low": 0.2, "medium": 0.5, "high": 0.8}
    total_risk = 0
    incident_locations = set()
    incident_corridors = set()
    if incidents is not None and not incidents.empty:
        incident_locations = set(
            incidents.get("location", []).astype(str).str.strip().tolist()
        )
        for incident_name in incident_locations:
            parts = [part.strip() for part in incident_name.replace("–", "-").split("-")]
            if len(parts) == 2:
                incident_corridors.add(frozenset(parts))

    for i in range(len(route) - 1):
        start = route[i]
        end = route[i + 1]
        traffic = str(
            graph[start][end].get("traffic", "Medium")
        ).lower()
        edge_risk = risk_values.get(traffic, 0.5)
        if (
            start in incident_locations
            or end in incident_locations
            or frozenset((start, end)) in incident_corridors
        ):
            edge_risk = min(1.0, edge_risk + 0.2)
        total_risk += edge_risk

    score = total_risk / (len(route) - 1)

    if score >= 0.7:
        level = "High"
    elif score >= 0.4:
        level = "Medium"
    else:
        level = "Low"

    return {"risk_score": round(score * 100, 2), "risk_level": level}
