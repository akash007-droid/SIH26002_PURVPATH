from src.data_manager import get_all_data
from src.analytics import calculate_kpis


def get_dashboard_data():
    data = get_all_data()
    kpis = calculate_kpis(
        data["locations"],
        data["roads"],
        data["vehicles"],
        data["incidents"]
    )
    return data, kpis
