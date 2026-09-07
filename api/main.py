from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from src.github_client import GitHubClient
from src.analyzer import RepoAnalyzer
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CommitMetrics API",
    description="Automated GitHub Repository Health & Portfolio Auditor",
    version="1.0.0",
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
    evaluates health metrics, and returns a comprehensive grading report.
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

        return {
            "username": username,
            "audit_summary": report
        }

    except ValueError as ve:
        logger.warning(f"Validation error for {username}: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Unexpected error during audit for {username}: {str(e)}")
        raise HTTPException(status_code=500, detail="An internal server error occurred while processing the repository audit.")