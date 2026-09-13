import networkx as nx
from src.data_manager import get_locations, get_roads


def create_graph():
    locations = get_locations()
    roads = get_roads()
    graph = nx.Graph()

    if locations.empty:
        return graph

    required = {"location", "latitude", "longitude"}
    if not required.issubset(locations.columns):
        return graph

    for _, row in locations.iterrows():
        try:
            graph.add_node(
                str(row["location"]).strip(),
                latitude=float(row["latitude"]),
                longitude=float(row["longitude"]),
                state=str(row.get("state", "Unknown")),
            )
        except (TypeError, ValueError):
            continue

    if not roads.empty:
        source_col = next((c for c in ["source", "from", "origin"] if c in roads.columns), None)
        target_col = next((c for c in ["destination", "to", "target"] if c in roads.columns), None)
        distance_col = next((c for c in ["distance", "weight", "travel_distance"] if c in roads.columns), None)

        if source_col and target_col:
            for _, row in roads.iterrows():
                source = str(row[source_col])
                target = str(row[target_col])

                if source not in graph.nodes or target not in graph.nodes:
                    continue

                try:
                    distance = float(row[distance_col]) if distance_col else 100.0
                except (TypeError, ValueError):
                    continue
                if distance <= 0:
                    continue
                traffic = str(row.get("traffic", "Medium"))

                graph.add_edge(
                    source,
                    target,
                    distance=distance,
                    traffic=traffic,
                    weight=distance
                )

    return graph


def get_graph_summary(graph):
    return {
        "locations": graph.number_of_nodes(),
        "roads": graph.number_of_edges()
    }
