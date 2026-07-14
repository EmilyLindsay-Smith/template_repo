# SETUP

This repository is intended to be used as a **GitHub template** for new Python projects.

Follow this checklist after creating a new repository from the template and before beginning development.

---
## Prerequisites

Install:

- Python 3.13+
- uv
- Git
- GitHub CLI (`gh`)

Authenticate GitHub CLI once:

```bash
gh auth login
```

Verify:

```bash
gh auth status
```

---

# 1. Local project setup

## Rename the project

Search the repository for `my-project` and replace it with your project name in docs and metadata. However, keep the Python package name as underscore separated: `my_project`

Typical places to update:

* `README.md`
* `CONTRIBUTING.md`
* `CITATION.cff`
* `CHANGELOG.md`
* `pyproject.toml`
* `CODEOWNERS`
* package names under `src/`
* any documentation

Also replace any placeholders such as:

* `<organisation>`
* `<your-github-name>`
* `<your-name>`
* `<your-email@example.com>`

---

## Create the development environment

Follow the instructions below OR run
```bash
make bootstrap
```
Or manually do this:

Synchronise the virtual environment:

```bash
uv sync
```

Install the Git hooks:

```bash
uv run pre-commit install --hook-type pre-commit --hook-type commit-msg --hook-type pre-push
```

Run all checks once:

```bash
uv run pre-commit run --all-files
uv run pytest --cov=src --cov-report=term-missing
uv run mypy
```

If no lockfile exists yet:

```bash
uv lock
```

---

## Check Python

Confirm your interpreter matches the project requirement:

```bash
python --version
uv --version
```

---

## Create your first development branch

```bash
git checkout -b feat/initial-development
```

Development should happen on feature branches rather than directly on `main`.

---

# 2. GitHub repository setup

Run the repository bootstrap script:

```bash
uv run python scripts/bootstrap_github_repo.py
```

This configures the standard GitHub repository settings used by this template.

It will:

* configure repository settings
* create the standard labels
* configure merge strategy
* apply branch protection
* require CI checks
* require PR title validation

---

## Verify repository settings

After the bootstrap script completes, check the following in GitHub.

### General

* Repository name is correct
* Repository description is correct
* Default branch is `main`

### Pull Requests

Recommended:

* Squash merge enabled
* Merge commits disabled
* Rebase merge disabled (optional)
* Automatically delete head branches

### Branch protection

Protect `main` with:

* Require pull requests
* Require status checks

  * CI
  * PR title
* Require branch to be up to date
* Dismiss stale approvals
* Block force pushes
* Block branch deletion

### Actions

Verify that GitHub Actions are enabled.

### Dependabot

Confirm Dependabot is enabled and scheduled correctly.

### Releases

The semantic-release workflow is intentionally disabled.

Do **not** enable it until you are ready for the first public release.

---

# 3. Verify the template

Before writing code, confirm:

* `uv sync` succeeds
* all pre-commit hooks pass
* tests pass
* mypy passes
* CI succeeds on a test pull request
* branch protection is working
* commit message validation is working
* PR title validation is working

---

# 4. Start developing

From this point onwards, the normal workflow is:

1. Create a feature branch.
2. Make changes.
3. Commit using Conventional Commits.
4. Open a pull request.
5. Merge after CI passes.
6. Keep the release workflow disabled until the project is ready for its first public release.
