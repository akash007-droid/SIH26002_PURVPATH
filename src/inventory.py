import networkx as nx
import pandas as pd

from config.settings import DEFAULT_SPEED, CRITICAL_STOCK_DAYS, WARNING_STOCK_DAYS

CRITICAL_DAYS = CRITICAL_STOCK_DAYS
WARNING_DAYS = WARNING_STOCK_DAYS


def _estimate_eta_days(graph, source, destination):
    """Shortest-path distance over the existing road graph, converted to
    a travel-time estimate in days using the configured average speed."""
    if source not in graph.nodes or destination not in graph.nodes:
        return None
    try:
        distance = nx.shortest_path_length(
            graph, source=source, target=destination, weight="weight"
        )
    except nx.NetworkXNoPath:
        return None
    hours = distance / DEFAULT_SPEED
    return round(hours / 24, 2)


def _risk_level(days_remaining):
    if days_remaining <= CRITICAL_DAYS:
        return "Critical"
    if days_remaining <= WARNING_DAYS:
        return "Warning"
    return "OK"


def calculate_shortage_alerts(stock, vehicles, graph):
    """Join destination stock levels with any vehicle currently carrying
    that item toward that location, and flag whether the shipment will
    arrive before local stock runs out."""
    if stock is None or stock.empty:
        return pd.DataFrame()

    rows = []
    for _, stock_row in stock.iterrows():
        location = str(stock_row["location"]).strip()
        item = str(stock_row["item"]).strip()
        current_qty = float(stock_row["current_quantity"])
        daily_use = float(stock_row["daily_consumption"]) or 0.0001
        days_remaining = round(current_qty / daily_use, 2)

        matching_vehicle = None
        if vehicles is not None and not vehicles.empty:
            candidates = vehicles[
                (vehicles["destination"].astype(str).str.strip() == location)
                & (vehicles["cargo_item"].astype(str).str.strip() == item)
            ]
            if not candidates.empty:
                matching_vehicle = candidates.iloc[0]

        eta_days = None
        will_arrive_in_time = None
        incoming_vehicle_id = None
        incoming_qty = None

        if matching_vehicle is not None:
            incoming_vehicle_id = matching_vehicle["vehicle_id"]
            incoming_qty = matching_vehicle["quantity"]
            eta_days = _estimate_eta_days(
                graph,
                str(matching_vehicle["current_location"]).strip(),
                location,
            )
            if eta_days is not None:
                will_arrive_in_time = eta_days <= days_remaining

        rows.append({
            "location": location,
            "item": item,
            "category": stock_row.get("category", ""),
            "days_remaining": days_remaining,
            "risk_level": _risk_level(days_remaining),
            "incoming_vehicle": incoming_vehicle_id,
            "incoming_qty": incoming_qty,
            "eta_days": eta_days,
            "will_arrive_in_time": will_arrive_in_time,
        })

    result = pd.DataFrame(rows)
    risk_order = {"Critical": 0, "Warning": 1, "OK": 2}
    result["_sort"] = result["risk_level"].map(risk_order)
    result = result.sort_values("_sort").drop(columns="_sort").reset_index(drop=True)
    return result
