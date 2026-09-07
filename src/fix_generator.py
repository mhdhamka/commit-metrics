def generate_fix_snippet(issue_type: str, tech_stack: str = "Python") -> str:
    if issue_type == "missing_readme":
        return "# Project Name\n\n> Short description of your project.\n\n## Quick Start\n```bash\n# Add your run commands here\n```"
    elif issue_type == "missing_ci" and tech_stack == "Python":
        return "name: CI\non: [push]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - name: Run Tests\n        run: pip install -r requirements.txt && pytest"
    return "# Review repository guidelines for standard structure."