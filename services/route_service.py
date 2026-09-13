from src.routing import get_shortest_route
from src.qpso import qpso_route_optimizer
from src.risk import calculate_route_risk
from src.data_manager import get_incidents


def optimize_route(graph, source, destination, algorithm="Dijkstra"):
    if algorithm == "Quantum PSO":
        result = qpso_route_optimizer(graph, source, destination)
        result["algorithm"] = "Quantum-Inspired PSO"
    else:
        result = get_shortest_route(graph, source, destination)
        result["algorithm"] = "Dijkstra"

    result["risk"] = calculate_route_risk(
        graph, result.get("route", []), get_incidents()
    )
    return result
