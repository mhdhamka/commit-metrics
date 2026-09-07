# Commit Metrics

> Automated GitHub Repository Health & Portfolio Auditor

**CommitMetrics** is a developer tool designed to evaluate public GitHub profiles, assess repository health against modern engineering standards, and generate actionable insights to level up portfolio quality.

---

## Tech Stack

* **Backend & Logic:** Python, PyGithub, Pydantic
* **API Layer:** FastAPI (`/audit/{username}`)
* **Frontend Dashboard:** Streamlit (GitHub Dark-mode developer interface)
* **Testing & Quality:** Pytest, Ruff

---

## Core Features

* **Smart Evaluation Engine:** Grades repositories across four key pillars weighted to reflect real-world engineering standards:
  * **Documentation (25%):** README, License, Contributing guidelines.
  * **Automation & CI/CD (30%):** GitHub Actions workflows and pipeline checks.
  * **Maintenance (25%):** Update recency and activity hygiene.
  * **Security & Best Practices (20%):** Proper `.gitignore` usage and repository setup.
* **Instant Grading:** Outputs a weighted portfolio letter grade (A+ to F) alongside a breakdown score.
* **Actionable Recommendations:** Delivers concrete suggestions for every repository lacking baseline standards.

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

### 5. Run the application:

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
│   └── main.py            # FastAPI endpoints
├── src/
│   ├── __init__.py
│   ├── config.py          # Constants & scoring weights
│   ├── github_client.py   # GitHub API integration
│   ├── analyzer.py        # Core grading & health logic
│   └── logging_config.py  # Structured logging setup
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