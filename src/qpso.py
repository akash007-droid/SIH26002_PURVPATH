import random
import networkx as nx


def qpso_route_optimizer(graph, source, destination, particles=30, iterations=50):
    """
    Quantum-inspired probabilistic route search.
    This implementation perturbs route costs and repeatedly searches
    candidate paths, retaining the best solution found.
    """
    if source not in graph.nodes or destination not in graph.nodes:
        return {"route": [], "distance": 0, "convergence": []}

    best_route = None
    best_cost = float("inf")
    convergence_history = []

    original_weights = {}
    for u, v, data in graph.edges(data=True):
        original_weights[(u, v)] = data.get(
            "base_distance", data.get("distance", data.get("weight", 1))
        )

    for _ in range(iterations):
        for _ in range(particles):
            for u, v in graph.edges():
                base_weight = original_weights[(u, v)]
                beta = random.uniform(0.75, 1.25)
                graph[u][v]["temp_weight"] = base_weight * beta

            try:
                route = nx.shortest_path(
                    graph, source=source, target=destination, weight="temp_weight"
                )

                cost = sum(
                    graph[route[i]][route[i + 1]].get(
                        "temp_weight",
                        graph[route[i]][route[i + 1]].get("weight", 0),
                    )
                    for i in range(len(route) - 1)
                )

                if cost < best_cost:
                    best_cost = cost
                    best_route = route
            except nx.NetworkXNoPath:
                continue

        convergence_history.append(round(best_cost, 2) if best_route else None)

    reported_distance = 0
    if best_route:
        reported_distance = sum(
            graph[best_route[i]][best_route[i + 1]].get(
                "weight", graph[best_route[i]][best_route[i + 1]].get("distance", 0)
            )
            for i in range(len(best_route) - 1)
        )

    return {
        "route": best_route or [],
        "distance": round(reported_distance, 2),
        "convergence": convergence_history,
        "iterations": iterations,
        "particles": particles
    }
