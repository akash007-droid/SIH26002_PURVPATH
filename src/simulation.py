import random

TRAFFIC_LEVELS = ["Low", "Medium", "High"]


def update_traffic(graph):
    for u, v, data in graph.edges(data=True):
        traffic = random.choices(
            TRAFFIC_LEVELS,
            weights=[0.45, 0.35, 0.20]
        )[0]

        data["traffic"] = traffic
        base_distance = data.get("base_distance", data.get("distance", 1))
        data["base_distance"] = base_distance

        multiplier = {
            "Low": 1.0,
            "Medium": 1.2,
            "High": 1.5
        }[traffic]

        data["weight"] = base_distance * multiplier

    return graph
