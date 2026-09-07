import logging

from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware

from src.analyzer import RepoAnalyzer
from src.database import get_audit_history, save_audit_log
from src.github_client import GitHubClient

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CommitMetrics API",
    description="Automated GitHub Repository Health & Portfolio Auditor",
    version="2.0.0",
)

# Enable CORS for frontend integration (Streamlit, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """Root health check endpoint."""
    return {
        "status": "online",
        "service": "CommitMetrics API",
        "docs_url": "/docs"
    }


@app.get("/audit/{username}")
def audit_user_repositories(
    username: str,
    token: str | None = Query(None, description="Optional custom GitHub Token to override rate limits")
):
    """
    Scans all public repositories for a given GitHub username,
    evaluates health metrics, returns a comprehensive grading report,
    and logs the audit history to SQLite.
    """
    try:
        logger.info(f"Starting audit for GitHub user: {username}")
        
        # 1. Initialize client and fetch repos
        client = GitHubClient(token=token)
        raw_repos = client.get_user_repos(username)
        
        if not raw_repos:
            raise HTTPException(
                status_code=404,
                detail=f"No public repositories found for user '{username}', or user does not exist."
            )

        # 2. Run analysis and scoring
        analyzer = RepoAnalyzer()
        report = analyzer.analyze_portfolio(raw_repos)

        # Extract grading details to save into the database
        overall_grade = report.get("overall_grade", "N/A")
        overall_score = report.get("overall_score", 0.0)

        # 3. Save audit record to SQLite database
        save_audit_log(username=username, grade=overall_grade, score=overall_score)

        return {
            "username": username,
            "audit_summary": report,
            "history": get_audit_history(username)
        }

    except ValueError as ve:
        logger.warning(f"Validation error for {username}: {ve!s}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Unexpected error during audit for {username}: {e!s}")
        raise HTTPException(status_code=500, detail="An internal server error occurred while processing the repository audit.")


@app.get("/badge/{username}")
def get_badge(username: str):
    """
    Generates a dynamic SVG badge reflecting the user's latest portfolio health grade
    for embedding directly into GitHub profile READMEs.
    """
    history = get_audit_history(username)
    grade = history[-1]["grade"] if history else "N/A"
    
    # Choose color based on grade tier
    color = "#28a745" if grade in ["A+", "A", "B"] else "#d73a49"
    
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="130" height="20">
      <linearGradient id="b" x2="0" y2="100%"><stop offset="0" stop-color="#bbb" stop-opacity=".1"/><stop offset="1" stop-opacity=".1"/></linearGradient>
      <mask id="a"><rect width="130" height="20" rx="3" fill="#fff"/></mask>
      <g mask="url(#a)">
        <path fill="#555" d="M0 0h65v20H0z"/>
        <path fill="{color}" d="M65 0h65v20H65z"/>
        <path fill="url(#b)" d="M0 0h130v20H0z"/>
      </g>
      <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
        <text x="32.5" y="15" fill="#010101" fill-opacity=".3">repo health</text>
        <text x="32.5" y="14">repo health</text>
        <text x="97.5" y="15" fill="#010101" fill-opacity=".3">{grade}</text>
        <text x="97.5" y="14">{grade}</text>
      </g>
    </svg>"""
    return Response(content=svg_content, media_type="image/svg+xml")