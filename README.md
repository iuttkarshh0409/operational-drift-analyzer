# Operational Drift Analyzer

A lightweight, explainable CLI tool to analyze **operational drift** in event-based systems.

This project focuses on **behavioral signals**, not ML magic:
- Retry pressure trends
- Dead event ratios
- Confidence-aware assessments
- Transparent snapshot persistence

Built to answer one question honestly:
> “Is the system drifting, or are we just paranoid?”

---

## 🚦 Signals Implemented

### 1. Retry Pressure (Primary Signal)
Compares retry behavior across two time windows:
- **Baseline window**
- **Recent window**

Outputs:
- Baseline average
- Recent average
- Delta
- Confidence
- Risk classification

Handled states:
- `OK`
- `WARMUP`
- `UNKNOWN`

---

### 2. Dead Event Ratio (Secondary Signal)
Measures how many events ended in a terminal `DEAD` state.

Rules:
- Uses a rolling time window
- Requires a minimum number of total events
- `None` = not enough data  
- `0.0` = valid, computed result

Outputs:
- Dead event ratio
- Dead event confidence

---

## 🧠 Design Philosophy

- Data over vibes
- None ≠ zero
- Confidence is explicit
- No silent assumptions
- Explainability > cleverness

---

## 🗄️ Architecture Overview

.
├── app.py
├── cli.py
├── services/
│   ├── drift_metrics_service.py
│   ├── risk_classifier.py
│   └── explanation_service.py
├── db/
│   ├── schema.py
│   └── repositories/
│       ├── event_repo.py
│       └── drift_repo.py
└── operational_drift.db

---

## ▶️ Usage

Run drift analysis:
```
python cli.py --drift
```

Show latest snapshot:
```
python cli.py --latest
```

---

## 🧊 Project Status

Frozen. Stable. Verified with real data.

---

## 🧾 License

Internal / personal use.
