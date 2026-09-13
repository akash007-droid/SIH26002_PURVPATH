import pandas as pd


def calculate_kpis(locations, roads, vehicles, incidents):
    return {
        "locations": len(locations),
        "roads": len(roads),
        "vehicles": len(vehicles),
        "incidents": len(incidents)
    }


def traffic_distribution(roads):
    if roads.empty:
        return pd.DataFrame()

    data = roads.copy()
    if "traffic" not in data.columns:
        return pd.DataFrame()

    return (
        data["traffic"]
        .astype(str)
        .str.strip()
        .str.title()
        .value_counts()
        .rename_axis("traffic_level")
        .reset_index(name="road_count")
    )
