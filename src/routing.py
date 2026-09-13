import networkx as nx


def get_shortest_route(graph, source, destination):
    try:
        route = nx.shortest_path(graph, source, destination, weight="weight")
        distance = nx.shortest_path_length(graph, source, destination, weight="weight")

        return {
            "success": True,
            "route": route,
            "distance": round(distance, 2)
        }
    except Exception as error:
        return {
            "success": False,
            "route": [],
            "distance": 0,
            "error": str(error)
        }
