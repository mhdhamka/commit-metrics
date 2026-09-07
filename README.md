<div align="center">

# Commit Metrics

> Automated GitHub Repository Health & Portfolio Auditor

**CommitMetrics** is a developer tool designed to evaluate public GitHub profiles, assess repository health against modern engineering standards, and generate actionable insights to level up portfolio quality.

[Live Demo](https://commit-metrics.streamlit.app/) · [Report Bug](https://github.com/mhdhamka/commit-metrics/issues) · [Request Feature](https://github.com/mhdhamka/commit-metrics/issues)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.11%2B-3776ab?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B?logo=streamlit&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-2.6%2B-E92063?logo=pydantic&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-8.0%2B-0A9EDC?logo=pytest&logoColor=white)
![Ruff](https://img.shields.io/badge/Ruff-0.3%2B-261230?logo=ruff&logoColor=white)

</div>

---

## Tech Stack

* **Backend & Logic:** Python, PyGithub, Pydantic
* **Database & Persistence:** SQLite (historical audit logs and tracking)
* **API Layer:** FastAPI (`/audit/{username}`, `/badge/{username}`)
* **Frontend Dashboard:** (Streamlit GitHub Dark-mode developer interface)
* **Terminal Automation:** Typer (CLI-based health audits)
* **Testing & Quality:** Pytest, Ruff

---

## Core Features

* **Smart Evaluation Engine:** Grades repositories across four key pillars weighted to reflect real-world engineering standards:
  * **Documentation (25%):** README, License, and structural clarity.
  * **Automation & CI/CD (30%):** GitHub Actions workflows and pipeline checks.
  * **Maintenance (25%):** Update recency, commit frequency, and branch hygiene.
  * **Security & Best Practices (20%):** Proper `.gitignore` usage and repository setup.

* **Advanced Tech Intelligence & Hygiene:** 
  * **Smart Tech Stack Detection:** Automatically parses project structures (`requirements.txt`, `package.json`, `Dockerfile`) to identify underlying frameworks (Python, Node.js, Docker).
  * **Zombie Branch Detection:** Flags stale branches left untouched for over 60 days to prevent codebase clutter.

* **Historical Tracking & Persistence:** 
  * **SQLite Audit Logs:** Automatically records portfolio health scores and timestamps over time, allowing developers to track how their engineering standards improve.

* **Terminal Automation (CLI):** 
  * **Typer-Based CLI Tool:** Execute quick portfolio health checks straight from your command line using simple commands like `python -m cli.app check <username>`.

* **Actionable Remediation & Dynamic Badges:**
  * **One-Click Fix Generators:** Provides copy-pasteable configuration templates (boilerplate READMEs, CI/CD YAML pipelines, and `.gitignore` files) directly inside the Streamlit dashboard for underperforming repos.
  * **Dynamic Profile Badges:** Exposes a `/badge/{username}` SVG endpoint to embed live, real-time repository health grades directly into personal GitHub profile READMEs.

* **Instant Grading & Dashboard:** 
  * **Multi-Format Output:** Delivers a weighted portfolio letter grade (A+ to F) alongside a GitHub Primer dark-mode UI with dimension breakdown scores and aggregate insights.

---

## Quick Start & Local Setup

### 1. Clone the repository:
```Bash
git clone https://github.com/mhdhamka/commit-metrics.git
cd commit-metrics
```

### 2. Create and activate a virtual environment:
```Bash
python -m venv venv
# On Windows:
venv\Scripts\activate
```

### 3. Install dependencies:
```Bash
pip install -r requirements.txt
```

### 4. Configure environment variables:
Copy .env.example to .env and add your GitHub Personal Access Token to avoid API rate limits.

### 5. Run tests:
Verify that your environment and code pass all unit tests:
```Bash
python -m pytest
```

### 6. Run the application:

#### Start FastAPI Backend:
```Bash
uvicorn api.main:app --reload
```

#### Start Streamlit UI (in a separate terminal):
```Bash
streamlit run ui/app.py
```

---


## Project Architecture

```text
commit-metrics/
│
├── .github/
│   └── workflows/         # CI/CD pipeline (linting, tests)
├── api/
│   ├── __init__.py
│   └── main.py            # FastAPI endpoints (/audit, /badge)
├── src/
│   ├── __init__.py
│   ├── config.py          # Constants, scoring weights, paths
│   ├── database.py        # SQLite storage for historical audit logs
│   ├── github_client.py   # PyGithub / async API integration
│   ├── analyzer.py        # Core grading, tech stack & hygiene logic
│   ├── fix_generator.py   # "Fix It" snippet generator
│   └── logging_config.py  # Structured logging setup
├── cli/
│   ├── __init__.py
│   └── app.py             # Typer CLI implementation
├── ui/
│   └── app.py             # Streamlit dashboard interface
├── tests/
│   └── test_analyzer.py   # Pytest unit tests
├── .env.example           # Environment variable template
├── .gitignore
├── README.md
├── pyproject.toml         # Dependencies & linter rules
└── requirements.txt       # Pinned dependencies
```

---

## Contributing

Issues and pull requests are welcome. If you're picking up one of the Roadmap items above, please open an issue first so effort isn't duplicated.

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/repo-integration`)
3. Commit your changes
4. Open a pull request describing what changed and why

---

## License

Distributed under the MIT License.

---

<div align="center">

If you found this project interesting, consider giving it a star ⭐

Crafted by **[@mhdhamka](https://github.com/mhdhamka)**

</div>