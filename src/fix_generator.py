def generate_fix_snippet(issue_type: str, tech_stack: str | list[str] = "Python") -> str:
    issue_lower = issue_type.lower()
    
    # Normalize tech_stack whether it is passed as a string or a list from RepoAnalyzer
    if isinstance(tech_stack, list):
        primary_stack = tech_stack[0] if tech_stack else "Python"
    else:
        primary_stack = tech_stack

    if "readme" in issue_lower:
        return (
            "# Project Name\n\n"
            "> A brief, high-impact description of your project.\n\n"
            "## Features\n"
            "- Core feature 1\n"
            "- Core feature 2\n\n"
            "## Quick Start\n"
            "```bash\n"
            "# Clone and install dependencies\n"
            "git clone [https://github.com/username/repo.git](https://github.com/username/repo.git)\n"
            "pip install -r requirements.txt\n"
            "```"
        )
    elif "ci" in issue_lower or "workflow" in issue_lower or "actions" in issue_lower:
        if "python" in primary_stack.lower():
            return (
                "name: CI Pipeline\n\n"
                "on:\n"
                "  push:\n"
                "    branches: [\"main\"]\n"
                "  pull_request:\n"
                "    branches: [\"main\"]\n\n"
                "jobs:\n"
                "  build-and-test:\n"
                "    runs-on: ubuntu-latest\n"
                "    steps:\n"
                "    - uses: actions/checkout@v4\n"
                "    - name: Set up Python\n"
                "      uses: actions/setup-python@v5\n"
                "      with:\n"
                "        python-version: \"3.11\"\n"
                "    - name: Install Dependencies\n"
                "      run: pip install -r requirements.txt\n"
                "    - name: Run Tests\n"
                "      run: pytest\n"
            )
        elif "node" in primary_stack.lower():
            return (
                "name: CI Pipeline\n\n"
                "on: [push, pull_request]\n\n"
                "jobs:\n"
                "  build:\n"
                "    runs-on: ubuntu-latest\n"
                "    steps:\n"
                "    - uses: actions/checkout@v4\n"
                "    - name: Set up Node.js\n"
                "      uses: actions/setup-node@v4\n"
                "      with:\n"
                "        node-version: \"20\"\n"
                "    - name: Install & Test\n"
                "      run: npm install && npm test\n"
            )
        else:
            return (
                "name: CI Pipeline\n\n"
                "on: [push, pull_request]\n\n"
                "jobs:\n"
                "  build:\n"
                "    runs-on: ubuntu-latest\n"
                "    steps:\n"
                "    - uses: actions/checkout@v4\n"
                "    - name: Run Build/Check\n"
                "      run: echo 'Add build commands here'\n"
            )
    elif "gitignore" in issue_lower:
        return (
            "# Byte-compiled / optimized / DLL files\n"
            "__pycache__/\n"
            "*.py[cod]\n"
            "*$py.class\n\n"
            "# Environments / Virtualenvs\n"
            "venv/\n"
            "env/\n"
            ".env\n\n"
            "# Distribution / packaging\n"
            "build/\n"
            "dist/\n"
            "*.egg-info/\n\n"
            "# IDE & OS specific files\n"
            ".idea/\n"
            ".vscode/\n"
            ".DS_Store"
        )
    elif "license" in issue_lower:
        return (
            "MIT License\n\n"
            "Copyright (c) 2026 Developer\n\n"
            "Permission is hereby granted, free of charge, to any person obtaining a copy\n"
            "of this software and associated documentation files (the \"Software\"), to deal\n"
            "in the Software without restriction..."
        )
    elif "branch" in issue_lower or "stale" in issue_lower or "zombie" in issue_lower:
        return (
            "# Branch Hygiene Instructions\n\n"
            "To prune and clean up stale or zombie branches:\n"
            "```bash\n"
            "# Prune remote-tracking branches no longer on remote\n"
            "git fetch --prune\n\n"
            "# Delete local branch safely\n"
            "git branch -d <branch_name>\n\n"
            "# Delete remote branch\n"
            "git push origin --delete <branch_name>\n"
            "```"
        )
        
    return "# Review repository guidelines for standard structure, documentation, and automated testing."