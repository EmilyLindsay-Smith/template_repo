# my-project

Generates input files for Splice to run behavioural experiments in Xmod.

## Status

This project is under active development. Automated releases are not enabled yet.

## Requirements

* Python 3.13 or later
* `uv`

## Getting started

Install dependencies:

```bash
uv sync
```

Install local hooks:

```bash
uv run pre-commit install --hook-type pre-commit --hook-type commit-msg --hook-type pre-push
```

Run the checks:

```bash
uv run pre-commit run --all-files
uv run pytest
```

## Development workflow

Work on feature branches and open pull requests into `main`.

## Commit messages

This repository uses the **Conventional Commits** specification.

Commit messages should have the form:

```text
<type>(<optional-scope>): <short description>
```

Examples:

```text
feat(parser): add support for CSV input
fix(io): handle empty configuration files
docs: update installation instructions
refactor(model): simplify validation logic
test(parser): add regression tests for empty files
```

Pull request titles should also follow Conventional Commits.

### Commit types

| Type       | When to use                                                       |      Triggers a release?*      |
| ---------- | ----------------------------------------------------------------- | :----------------------------: |
| `feat`     | A new feature or user-visible capability                          |              Minor             |
| `fix`      | A bug fix                                                         |              Patch             |
| `perf`     | A performance improvement                                         |              Patch             |
| `docs`     | Documentation only                                                |               No               |
| `refactor` | Code restructuring without changing behaviour                     |               No               |
| `test`     | Adding or modifying tests                                         |               No               |
| `style`    | Formatting, whitespace, imports, comments (no behavioural change) |               No               |
| `build`    | Build system or packaging changes                                 |               No               |
| `ci`       | Continuous integration or GitHub Actions                          |               No               |
| `chore`    | Maintenance, tooling, dependencies, housekeeping                  |               No               |
| `revert`   | Reverting a previous commit                                       | Depends on the reverted commit |

* Once automated releases are enabled.

### Scopes

A scope is optional but encouraged where it makes the change clearer.

Examples:

```text
feat(parser): add support for JSON files
fix(cli): handle missing arguments
docs(api): document configuration options
test(io): add regression tests
refactor(model): simplify validation logic
```

Use scopes that correspond to logical parts of the project rather than filenames.

### Breaking changes

Breaking API or behavioural changes should either:

```text
feat(api)!: redesign configuration format
```

or include a footer:

```text
BREAKING CHANGE: configuration files now use TOML instead of YAML.
```

### Good examples

```text
feat(parser): support zipped input files

fix(io): handle empty configuration directory

perf(parser): cache compiled regular expressions

docs: add migration guide

refactor(model): split validation into smaller functions

test(parser): add regression test for malformed CSV

ci: cache uv dependencies

build: update setuptools configuration

style: apply Ruff formatting

chore: update development dependencies

revert: revert "feat(parser): support zipped input files"
```

### Examples to avoid

```text
fixed stuff
updates
misc changes
WIP
more work
asdf
bugfix
changes
```

These messages do not describe the change clearly and will fail validation.

### Tips

* Keep the summary line under approximately 72 characters.
* Use the imperative mood ("add", "fix", "remove", not "added" or "fixed").
* Make each commit represent one logical change where practical.
* Put the motivation or implementation details in the commit body if more explanation is needed.
* Prefer `refactor` over `feat` if behaviour has not changed.
* Prefer `chore` for dependency updates and repository maintenance.
* Prefer `docs` for documentation-only changes.

Note: Although only feat, fix, and perf currently result in version bumps once release automation is enabled, all commit types are encouraged.

## Repository layout

* `src/` — package source code
* `tests/` — test suite
* `.github/workflows/` — CI configuration
* `.pre-commit-config.yaml` — local hygiene and validation hooks

## Release policy

Release automation is intentionally disabled for now.

When the project is ready for its first release, semantic-release can be enabled in CI without changing the commit convention already in use.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md).
