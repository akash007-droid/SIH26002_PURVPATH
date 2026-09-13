from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FOLDER = PROJECT_ROOT / "data"

REQUIRED_COLUMNS = {
    "locations.csv": {"location", "latitude", "longitude"},
    "roads.csv": {"source", "destination", "distance"},
    "vehicles.csv": {"vehicle_id", "status", "current_location"},
    "incidents.csv": {"incident_id", "location", "incident_type", "severity"},
    "stock.csv": {"location", "item", "current_quantity", "daily_consumption"},
}


def load_csv(filename):
    path = DATA_FOLDER / filename
    if not path.exists():
        return pd.DataFrame()

    try:
        dataframe = pd.read_csv(path)
        dataframe.columns = (
            dataframe.columns.astype(str).str.strip().str.lower()
        )
        missing = REQUIRED_COLUMNS.get(filename, set()) - set(dataframe.columns)
        if missing:
            raise ValueError(
                f"{filename} is missing required columns: {', '.join(sorted(missing))}"
            )
        return dataframe
    except (OSError, pd.errors.ParserError, ValueError) as error:
        print(f"Could not load {filename}: {error}")
        return pd.DataFrame()


def get_locations():
    return load_csv("locations.csv")


def get_roads():
    return load_csv("roads.csv")


def get_vehicles():
    return load_csv("vehicles.csv")


def get_incidents():
    return load_csv("incidents.csv")


def get_stock():
    return load_csv("stock.csv")


def get_all_data():
    return {
        "locations": get_locations(),
        "roads": get_roads(),
        "vehicles": get_vehicles(),
        "incidents": get_incidents(),
        "stock": get_stock()
    }
