"""
Central configuration for Purva Path.

Purva Path ("Eastern Path") is an AI-assisted logistics accessibility
intelligence prototype for the North Eastern Region, built against the
scope described in the project's PRD / TDR / TRD documents. This MVP uses
demo/synthetic data and rule-based scoring in place of live government
data feeds and a trained ML model -- both are called out explicitly in
the UI wherever a real deployment would need real data.
"""

APP_NAME = "पूर्वपथ"
APP_TAGLINE = "AI-Powered Logistics Accessibility Intelligence — North Eastern Region"
APP_ICON = "🛣️"
DATA_FOLDER = "data"

# --- Route optimization -----------------------------------------------
DEFAULT_SPEED = 50  # km/h, used for ETA estimates
HIGH_TRAFFIC_MULTIPLIER = 1.5
MEDIUM_TRAFFIC_MULTIPLIER = 1.2
LOW_TRAFFIC_MULTIPLIER = 1.0
MAX_ROUTE_ALTERNATIVES = 10

# --- Disruption risk scoring -------------------------------------------
# Rule-based placeholder thresholds (0-100 risk score -> band).
# These are NOT scientifically validated. Keep them configurable here
# and recalibrate once real historical incident/weather data is
# available to train the disruption-risk model described in the PRD.
RISK_THRESHOLDS = {
    "LOW": 30,       # 0-30
    "MODERATE": 60,  # 31-60
    "HIGH": 80,      # 61-80
    # anything above HIGH -> CRITICAL (81-100)
}

RISK_BAND_COLORS = {
    "LOW": "#2ecc71",
    "MODERATE": "#f1c40f",
    "HIGH": "#e67e22",
    "CRITICAL": "#e74c3c",
    "UNKNOWN": "#95a5a6",
}

RISK_BAND_ORDER = ["CRITICAL", "HIGH", "MODERATE", "LOW"]

# --- Inventory / shortage alerts ---------------------------------------
CRITICAL_STOCK_DAYS = 1.0
WARNING_STOCK_DAYS = 3.0
