# पूर्वपथ Purv path 🛣️

**पूर्वपथ Purv path** ("Eastern Path") is a Streamlit prototype MVP for the
**AI-Powered Smart Logistics & Accessibility Intelligence Platform** for the
North Eastern Region of India, scoped against the project's PRD, TDR and TRD
documents. It demonstrates the core feature set end-to-end using synthetic
demo data and rule-based scoring in place of live government data feeds and
a trained ML model.

## Structure — one landing page, every feature on its own page

```
Home.py                     <- landing page: KPIs + a button/card for every feature
pages/
  1_Risk_Map.py              <- the ONLY map in the app: network colored by disruption risk
  2_Route_Optimizer.py       <- Dijkstra vs. Quantum-inspired (QPSO) route search
  3_Fleet_Tracking.py        <- vehicle tracking + essential-goods shortage alerts
  4_Field_Reports.py         <- geo-tagged incident report submission (session demo)
  5_Alerts.py                <- unified alert feed (risk + incidents + shortages)
  6_Analytics.py             <- traffic distribution + incident trends
components/                 <- shared UI (nav header, risk map, charts)
config/settings.py          <- app name, risk-band thresholds/colors, etc.
src/, services/             <- graph, routing, QPSO, risk scoring, inventory, data loading
data/                       <- demo CSVs (locations, roads, vehicles, incidents, stock)
```

Streamlit auto-detects the `pages/` folder next to `Home.py` and builds the
sidebar navigation from it, so every feature is reachable from the sidebar
**and** from a card/button on the Home page — and every feature page links
back to Home at the top.

**Only one map exists in the whole app — the Risk Map.** Every other page
that needs spatial context (e.g. the Route Optimizer) links to it instead of
rendering its own separate map.

## 1. Install

```bash
cd purva_path
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 2. Run

```bash
streamlit run Home.py
```

Streamlit prints a local address, normally `http://localhost:8501`. Always
run the command from the `purva_path` folder, since `Home.py` is the entry
point Streamlit uses to auto-discover `pages/`.

## 3. What each page does

### Home
Landing page. Shows headline KPIs (locations, corridors, vehicles, active
incidents, critical-risk corridors, critical stock shortages) and a card for
every feature, each linking straight to its page.

### 🗺️ Risk Map
The single map in the platform. Every road corridor is colored by a 0–100
disruption-risk score, bucketed into LOW / MODERATE / HIGH / CRITICAL bands
(thresholds configurable in `config/settings.py`). Score = base traffic-level
score + a penalty if the corridor has an active reported incident. This is a
rule-based placeholder for the trained XGBoost disruption model described in
the PRD — swap it in once real historical incident/weather data exists (see
`src/risk.py: score_segment`). A "Simulate Live Conditions" button randomizes
traffic to demo how the map updates.

### 🧭 Route Optimizer
Pick a source, destination and algorithm (Dijkstra or Quantum-inspired PSO),
optionally simulate live traffic, and get the optimized route, travel cost,
risk score, and a hop-by-hop table. Links to the Risk Map for the spatial
view instead of duplicating a map here.

### 🚛 Fleet & Supply Tracking
Vehicle roster with cargo, plus shortage alerts per destination: days of
local stock remaining, whether a vehicle is currently assigned to resupply
it, that vehicle's live ETA over the road graph, and whether it will arrive
before stock runs out.

### 📝 Field Reports
A form to submit a geo-tagged incident report (location, type, severity,
description, optional photo). Stored in the browser session only — this is
a demo of the PRD's offline-first field-reporting feature, not a persisted
backend. A production build needs local encrypted queueing and background
sync per the TDR.

### 🔔 Alerts Center
Aggregates CRITICAL/HIGH risk corridors, active field incidents, and
CRITICAL/WARNING stock shortages into one feed, sorted by severity, with a
per-alert Acknowledge action (session-based).

### 📊 Analytics
Traffic-level distribution across the network and the recorded incident
table — the first layer for spotting bottlenecks.

## 4. Edit the sample data

Files live in `data/`:

- `locations.csv` — `location`, `latitude`, `longitude` (`state` optional)
- `roads.csv` — `source`, `destination`, `distance` (`traffic` recommended)
- `vehicles.csv` — `vehicle_id`, `status`, `current_location` (+ cargo columns)
- `incidents.csv` — `incident_id`, `location`, `incident_type`, `severity`
- `stock.csv` — `location`, `item`, `current_quantity`, `daily_consumption`

Location names must match exactly across files (a road `Guwahati → Shillong`
needs both names present in `locations.csv`).

## 5. Production roadmap (from the PRD/TDR/TRD)

This prototype intentionally simplifies things that a production pilot
needs real infrastructure for:

1. **Trained disruption-risk model** — replace `src/risk.py`'s rule-based
   scoring with an XGBoost (or similar) model trained on real historical
   incident/weather/terrain data, per the PRD's AI/ML section.
2. **Live data feeds** — weather/rainfall, GPS/telematics, and government
   road-status integrations instead of static CSVs.
3. **Real persistence** — PostgreSQL/PostGIS backend (see the Backend
   Schema doc) instead of CSVs and in-session state; this also makes Field
   Reports and Alerts durable across restarts and users.
4. **Offline-first mobile app** — encrypted local queue + background sync
   for field reporting in low-connectivity areas.
5. **Auth, RBAC, audit trail** — role-scoped access by geography per the
   TDR's security requirements.
6. **Notifications** — SMS/push/email/multilingual alert delivery instead
   of in-app acknowledgement only.

## 6. Troubleshooting

- If `streamlit` isn't recognized, activate `.venv` and run
  `python -m streamlit run Home.py`.
- If the Risk Map is blank, check that every location has valid numeric
  latitude/longitude and that road endpoints exactly match location names.
- If a route can't be found, the source and destination sit in disconnected
  parts of the road graph — add a connecting road or report the corridor as
  unavailable.


## Frontend refresh
The UI has been refreshed into an SIH-ready command-center style:
- Dark navy glassmorphism theme with cyan/green operational accents.
- Emergency Alert Center banner with live counts from the demo data.
- Climate Conditions card matching the provided wireframe (clearly marked demo feed).
- Mission Control feature rail matching the sketch.
- Animated network-map preview with risk nodes and hover-ready visual treatment.
- Responsive KPI cards and polished navigation shared across all pages.
- Plotly charts use the same dark visual system.


## Accuracy roadmap for SIH demo → pilot

The current risk engine is a transparent rule-based prototype. For a more accurate and defensible deployment:

1. **Use verified live feeds** — IMD weather alerts, road-closure/maintenance feeds, state PWD/NHAI updates, and GPS/telematics where available.
2. **Add time + location to every incident** — exact coordinates, start/end time, closure status, affected corridor, and source agency.
3. **Separate observed vs predicted values** — never mix synthetic/demo values with live observations; show source and timestamp beside each signal.
4. **Calibrate risk with historical outcomes** — train on past closures, delays, landslides, flooding, and travel-time disruption rather than fixed traffic penalties.
5. **Use a weighted, explainable risk model** — weather severity, incident recency, road condition, elevation/slope, historical failure frequency, and route exposure can each contribute a documented weight.
6. **Validate predictions** — track precision/recall for disruption alerts and MAE/RMSE for ETA; report false alarms and missed incidents.
7. **Add confidence scores** — show `Risk: High · 82% confidence` and lower confidence when feeds are stale or incomplete.
8. **Add freshness/health indicators** — display the last update time and feed status so judges can distinguish a current signal from stale data.
9. **Use geospatial matching** — match an incident/weather cell to road segments by coordinates and distance instead of relying only on corridor-name text.
10. **Create a feedback loop** — field teams can confirm, reject, or resolve alerts; feed those verified outcomes back into model evaluation.

## Top 9 Accuracy Improvements

1. **Live weather** — verified weather/rainfall feeds.
2. **Road conditions** — closures, landslides, flooding and maintenance.
3. **GPS telemetry** — real vehicle position, speed and travel time.
4. **Geospatial matching** — map incidents to exact road segments.
5. **Historical learning** — train/validate against real past outcomes.
6. **Time decay** — prioritize recent incidents.
7. **Risk confidence** — expose confidence alongside risk severity.
8. **Data freshness** — show source, timestamp and feed health.
9. **Field validation** — capture confirmation/resolution from field teams.

These upgrades are recommended before treating the dashboard's risk score as a production predictive model.


## Latest UI / Field Report Changes

- Dark theme is forced by default through `.streamlit/config.toml`.
- Reporter Name / ID is no longer collected.
- Field reports require device GPS and store reporter coordinates plus the nearest known network location.
- A compact 🚨 emergency control reveals the North East helpline: +91 93211 27701.
- Navigation remains page-based; the emergency control is intentionally compact so it does not alter the main dashboard layout.
#   S I H 2 6 0 0 2 _ P U R V P A T H  
 #   S I H 2 6 0 0 2 _ P U R V P A T H  
 