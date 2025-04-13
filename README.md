# MTV – Multi Test Viewer

**Multi Test Viewer** is an MVP version of a test execution analysis dashboard.  
It provides interactive visualizations of time-series (`Trace`) and aggregated (`Metric`) test data from CSV files, allowing users to explore results "efficiently".

This project was created as a prototype to demonstrate key features of a robust testing analytics platform using Dash and FastAPI.

---
## 📚 Table of Contents

- [MTV – Multi Test Viewer](#mtv--multi-test-viewer)
  - [📚 Table of Contents](#-table-of-contents)
  - [✨ Key Features](#-key-features)
  - [🔧 Technologies](#-technologies)
  - [🚀 Getting Started](#-getting-started)
    - [🐍 Option 1: Using Python `venv` + `pip`](#-option-1-using-python-venv--pip)
      - [▶️ Linux / macOS](#️-linux--macos)
      - [▶️ Windows](#️-windows)
    - [⚡ Option 2: Using UV Package Manager](#-option-2-using-uv-package-manager)
  - [🛠️ TODO](#️-todo)

---

## ✨ Key Features

- 📊 **Three dedicated dashboard pages** for different types of analysis:
  - Time-series `Trace` visualizations with stats (avg, std, min, max)
  - Comparative `Metric` analysis with difference visualization (e.g., +50%, -30%)
  - Interactive summary table with selectable test details
- 🧠 **Dynamic charts** – add/remove metrics and traces on the fly
- 🔍 **Test parameter filtering**
- 🔗 **Sharable URLs** with full dashboard state (filters, selections, views)
- 🔁 **Real-time synchronization** with file-based data changes
- 🧩 Modular architecture: Dash frontend + FastAPI backend
- 🌐 **REST API** support for fetching data
- 🔌 **WebSocket connection** for real-time interactivity

---

## 🔧 Technologies

- Python 3
- [Dash by Plotly](https://dash.plotly.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- Pandas
- Plotly
- Uvicorn

---

## 🚀 Getting Started

You can run the project using one of the following options:
- **Standard Python** (with `venv` + `pip`)
- **UV Package Manager** (fast alternative to pip + venv)

---

### 🐍 Option 1: Using Python `venv` + `pip`

#### ▶️ Linux / macOS

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run backend
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

# 4. In a new terminal: run frontend
source venv/bin/activate
python -m mtv_dashboard.main
```

#### ▶️ Windows

``` bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run backend
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

# 4. In a new terminal: run frontend
venv\Scripts\activate
python -m mtv_dashboard.main
```

---
### ⚡ Option 2: Using UV Package Manager
> [UV ](https://github.com/astral-sh/uv)is a fast and modern Python package manager that replaces both `pip` and `venv`.

```bash
# 1. Create virtual environment using UV and install dependencies

uv sync
```

---

## 🛠️ TODO

- [ ] Connect WebSocket **only** on the home page to reduce overhead.
- [ ] Adjust chart dimensions – current layout renders them too small.
- [ ] Improve sharable link mechanism:
  - [x] **Current:** Populate charts using route path parameters.
  - [ ] **Planned:** Store chart state in a database and generate a short sharable link that maps to saved data.
