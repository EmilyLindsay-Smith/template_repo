# Contributing

Thank you for contributing to **my-project**.

## Project workflow

Development happens on feature branches. `main` should remain clean and releasable.

Recommended flow:

1. Create a branch from `main`.
2. Make your changes.
3. Run the local checks.
4. Open a pull request.
5. Merge only after CI passes and the PR title matches Conventional Commits.

## Local setup

Install the development dependencies and hooks:

```bash
uv sync
uv run pre-commit install --hook-type pre-commit --hook-type commit-msg --hook-type pre-push
uv run pre-commit run --all-files
```

If hooks are not yet installed for this clone, run:

```bash
uv run pre-commit install --install-hooks
```

## Commit messages

This repository uses Conventional Commits.

Use messages like:

```text
feat(parser): add support for X
fix(io): handle empty input
docs: update setup instructions
chore: refresh dependencies
```

Use the present tense and keep the summary line short and specific.

The commit-msg hook validates commit messages automatically. If a commit fails validation, fix the message and recommit.

## Pull requests

PR titles should also follow Conventional Commits, because the CI workflow validates them.

Examples:

```text
feat(parser): add support for X
fix(cli): handle missing argument
docs: improve setup instructions
```

## Checks to run before opening a PR

Run the same checks CI runs:

```bash
uv run pre-commit run --all-files
uv run pytest
```

If you are working on code that uses type checking or packaging metadata, also run:

```bash
uv run mypy
```

## Releases

Automated releases are not enabled yet.

When the project is ready for release, semantic-release will be enabled from CI. Until then, do not add release automation or tags unless explicitly asked for.

## Style

* Prefer small, focused changes.
* Add tests for new behavior.
* Keep functions and modules simple.
* Update documentation when behavior changes.
* Avoid unrelated formatting changes in feature PRs.

## If something fails

Common causes:

* a stale virtual environment or lockfile,
* missing pre-commit hooks,
* a commit message that does not match Conventional Commits,
* a PR title that does not match Conventional Commits.

When in doubt, re-run:

```bash
uv sync
uv run pre-commit run --all-files
```
