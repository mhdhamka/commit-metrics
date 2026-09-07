from datetime import datetime, timezone
from src.config import SCORE_WEIGHTS
import logging

logger = logging.getLogger(__name__)


class RepoAnalyzer:
    def __init__(self):
        self.weights = SCORE_WEIGHTS

    def analyze_portfolio(self, repos: list[dict]) -> dict:
        """Analyzes a list of repositories and returns aggregate portfolio health metrics."""
        if not repos:
            return {
                "total_repos": 0,
                "overall_score": 0.0,
                "grade": "N/A",
                "repositories": [],
                "recommendations": ["No public repositories found to analyze."],
            }

        analyzed_repos = []
        total_score_sum = 0.0

        for repo in repos:
            repo_analysis = self._analyze_single_repo(repo)
            analyzed_repos.append(repo_analysis)
            total_score_sum += repo_analysis["health_score"]

        # Calculate average portfolio score
        overall_score = round(total_score_sum / len(repos), 2)
        overall_grade = self._score_to_grade(overall_score)

        # Aggregate top recommendations across the portfolio
        portfolio_recommendations = self._generate_portfolio_recommendations(analyzed_repos)

        return {
            "total_repos": len(repos),
            "overall_score": overall_score,
            "grade": overall_grade,
            "repositories": analyzed_repos,
            "recommendations": portfolio_recommendations,
        }

    def _analyze_single_repo(self, repo: dict) -> dict:
        """Evaluates an individual repository across core health dimensions."""
        
        # 1. Documentation Score (README, License)
        doc_score = 0.0
        if repo.get("has_readme"):
            doc_score += 0.6
        if repo.get("has_license"):
            doc_score += 0.4

        # 2. CI/CD Score (Workflows presence)
        ci_cd_score = 1.0 if repo.get("has_workflows") else 0.0

        # 3. Maintenance Score (Recency of updates & branch hygiene)
        maintenance_score = self._calculate_maintenance_score(repo.get("updated_at"))

        # 4. Security & Best Practices (.gitignore presence)
        security_score = 1.0 if repo.get("has_gitignore") else 0.0

        # Weighted calculation
        final_score = (
            (doc_score * self.weights["documentation"]) +
            (ci_cd_score * self.weights["ci_cd"]) +
            (maintenance_score * self.weights["maintenance"]) +
            (security_score * self.weights["security"])
        ) * 100  # Scale to 0-100

        final_score = round(final_score, 2)
        grade = self._score_to_grade(final_score)

        # Generate repository-specific recommendations
        suggestions = []
        if not repo.get("has_readme"):
            suggestions.append("Add a detailed `README.md` explaining setup and usage.")
        if not repo.get("has_license"):
            suggestions.append("Add an open-source `LICENSE` file.")
        if not repo.get("has_workflows"):
            suggestions.append("Set up GitHub Actions workflow in `.github/workflows/` for automated testing/linting.")
        if not repo.get("has_gitignore"):
            suggestions.append("Add a proper `.gitignore` file to prevent tracking build artifacts or secrets.")

        return {
            "name": repo["name"],
            "html_url": repo["html_url"],
            "language": repo.get("language") or "Unknown",
            "health_score": final_score,
            "grade": grade,
            "breakdown": {
                "documentation": round(doc_score * 100, 1),
                "ci_cd": round(ci_cd_score * 100, 1),
                "maintenance": round(maintenance_score * 100, 1),
                "security": round(security_score * 100, 1),
            },
            "suggestions": suggestions,
        }

    def _calculate_maintenance_score(self, updated_at) -> float:
        """Scores maintenance based on how recently the repository was updated."""
        if not updated_at:
            return 0.0
        
        # Ensure timezone-aware comparison
        if updated_at.tzinfo is None:
            updated_at = updated_at.replace(tzinfo=timezone.utc)
            
        now = datetime.now(timezone.utc)
        age_days = (now - updated_at).days

        if age_days <= 30:
            return 1.0
        elif age_days <= 90:
            return 0.75
        elif age_days <= 180:
            return 0.5
        elif age_days <= 365:
            return 0.25
        return 0.1  # Stale repository (> 1 year)

    def _score_to_grade(self, score: float) -> str:
        """Converts a numerical score (0-100) into a letter grade."""
        if score >= 90:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B"
        elif score >= 60:
            return "C"
        elif score >= 50:
            return "D"
        return "F"

    def _generate_portfolio_recommendations(self, analyzed_repos: list[dict]) -> list[str]:
        """Synthesizes high-level actionable feedback for the entire portfolio."""
        missing_readmes = sum(1 for r in analyzed_repos if any("README" in s for s in r["suggestions"]))
        missing_workflows = sum(1 for r in analyzed_repos if any("GitHub Actions" in s for s in r["suggestions"]))
        
        recs = []
        if missing_readmes > 0:
            recs.append(f"{missing_readmes} of your repositories are missing a `README.md`. Strong documentation drives portfolio views.")
        if missing_workflows > 0:
            recs.append(f"{missing_workflows} repositories lack CI/CD pipelines. Add automated testing via GitHub Actions.")
            
        if not recs:
            recs.append("Amazing job! Your portfolio repositories meet elite standards across documentation, CI/CD, and hygiene.")
            
        return recs