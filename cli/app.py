import typer

from src.analyzer import RepoAnalyzer
from src.github_client import GitHubClient

app = typer.Typer(help="CommitMetrics Terminal Auditor")


@app.command()
def check(user: str, token: str | None = None):
    """Run a quick repository health check for a given GitHub username."""
    typer.echo(f"Analyzing public repositories for @{user}...")

    try:
        # Initialize client and analyzer
        client = GitHubClient(token=token)
        repos = client.get_user_repos(user)

        analyzer = RepoAnalyzer()
        result = analyzer.analyze_portfolio(repos)

        # Print neat terminal output
        typer.echo("\n--- Portfolio Audit Summary ---")
        typer.echo(f"Total Repositories: {result['total_repos']}")
        typer.echo(f"Overall Score: {result['overall_score']}%")
        typer.echo(f"Portfolio Grade: {result['grade']}")

        typer.echo("\nTop Recommendations:")
        for rec in result["recommendations"]:
            typer.echo(f" - {rec}")

    except Exception as e:
        typer.echo(f"[Error] Could not complete audit for {user}: {e!s}", err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()