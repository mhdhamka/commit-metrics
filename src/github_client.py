from github import Github, GithubException
from src.config import settings
import logging

logger = logging.getLogger(__name__)


class GitHubClient:
    def __init__(self, token: str | None = None):
        # Use token from settings if not explicitly passed (avoids low rate limits)
        auth_token = token or settings.github_token
        self.client = Github(auth_token) if auth_token else Github()

    def get_user_repos(self, username: str) -> list[dict]:
        """Fetches all public repositories for a given GitHub username."""
        try:
            user = self.client.get_user(username)
            repos = []
            
            for repo in user.get_repos(type="public"):
                if repo.fork:
                    continue  # Skip forked repos to focus on original work
                
                # Basic metadata extraction
                repo_data = {
                    "name": repo.name,
                    "full_name": repo.full_name,
                    "html_url": repo.html_url,
                    "description": repo.description,
                    "stargazers_count": repo.stargazers_count,
                    "forks_count": repo.forks_count,
                    "open_issues_count": repo.open_issues_count,
                    "updated_at": repo.updated_at,
                    "has_issues": repo.has_issues,
                    "language": repo.language,
                }
                
                # Check critical health files and structures
                repo_data["has_readme"] = self._check_file_exists(repo, "README.md")
                repo_data["has_license"] = self._check_file_exists(repo, "LICENSE")
                repo_data["has_gitignore"] = self._check_file_exists(repo, ".gitignore")
                repo_data["has_workflows"] = self._check_folder_exists(repo, ".github/workflows")
                
                # Get branch info (to check for staleness)
                repo_data["branches_count"] = self._get_branches_count(repo)
                
                repos.append(repo_data)
                
            return repos

        except GithubException as e:
            logger.error(f"GitHub API Error for user {username}: {e.data.get('message', str(e))}")
            raise ValueError(f"Could not fetch data for username '{username}'. Check if user exists or token is valid.")
        except Exception as e:
            logger.error(f"Unexpected error fetching repos for {username}: {str(e)}")
            raise

    def _check_file_exists(self, repo, path: str) -> bool:
        """Checks if a specific file exists in the repository root."""
        try:
            repo.get_contents(path)
            return True
        except Exception:
            return False

    def _check_folder_exists(self, repo, path: str) -> bool:
        """Checks if a specific folder exists in the repository."""
        try:
            contents = repo.get_contents(path)
            return isinstance(contents, list) and len(contents) > 0
        except Exception:
            return False

    def _get_branches_count(self, repo) -> int:
        """Safely retrieves the number of branches."""
        try:
            return len(list(repo.get_branches()))
        except Exception:
            return 0