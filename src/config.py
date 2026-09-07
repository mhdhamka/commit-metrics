from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    github_token: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Initialize settings instance
settings = Settings()

# Portfolio health scoring weights (must total 1.0)
SCORE_WEIGHTS = {
    "documentation": 0.25,  # README, License, Contributing
    "ci_cd": 0.30,  # GitHub Actions, workflows, linters
    "maintenance": 0.25,  # Stale branches, commit frequency
    "security": 0.20,  # .gitignore, basic best practices
}