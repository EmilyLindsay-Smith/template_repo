#!/usr/bin/env python3
"""Bootstrap standard GitHub repository settings for a project template.

This script assumes the repository already exists on GitHub and that you are
running it from inside a clone with the GitHub CLI (`gh`) installed and
authenticated.

It standardises:
- repository settings (template repo, issues, merge strategy, etc.)
- common labels
- branch protection for `main`

The branch-protection check names default to the current CI job names in this
template. If you rename jobs, update the defaults or pass your own list with
`--required-status-check`.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from dataclasses import dataclass

DEFAULT_REQUIRED_STATUS_CHECKS = [
    "CI / Python",
    "CI / PR title",
]

DEFAULT_LABELS = [
    ("bug", "D73A4A", "Something is broken"),
    ("enhancement", "A2EEEF", "New feature or improvement"),
    ("documentation", "0075CA", "Documentation changes"),
    ("refactor", "FBCA04", "Internal refactoring"),
    ("dependencies", "BFDADC", "Dependency updates"),
    ("wontfix", "ffffff", "Issue will not be fixed"),
]


@dataclass(frozen=True)
class RepoConfig:
    repo: str
    default_branch: str
    description: str | None
    homepage: str | None
    topics: list[str]
    required_status_checks: list[str]
    apply_branch_protection: bool
    apply_labels: bool


def run(cmd: list[str], *, input_text: str | None = None) -> None:
    """Run a command and raise a helpful error on failure."""
    completed = subprocess.run(  # noqa: S603
        cmd,
        check=False,
        text=True,
        input=input_text,
        capture_output=True,
    )
    if completed.returncode != 0:
        message = ["Command failed:", "  " + " ".join(cmd)]
        if completed.stdout:
            message.append("\nstdout:\n" + completed.stdout)
        if completed.stderr:
            message.append("\nstderr:\n" + completed.stderr)
        raise RuntimeError("\n".join(message))


def infer_repo() -> str:
    """Infer the repository name from the current git remote using gh."""
    completed = subprocess.run(
        ["gh", "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"],  # noqa: S607
        check=False,
        text=True,
        capture_output=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "Could not infer the repository name. Pass --repo OWNER/REPO.\n"
            f"stdout:\n{completed.stdout}\n"
            f"stderr:\n{completed.stderr}"
        )
    repo = completed.stdout.strip()
    if not repo:
        raise RuntimeError("GitHub CLI returned an empty repository name.")
    return repo


def split_csv(values: list[str]) -> list[str]:
    """Split repeated comma-separated args into a flat list."""
    out: list[str] = []
    for value in values:
        out.extend(part.strip() for part in value.split(",") if part.strip())
    return out


def configure_repository(cfg: RepoConfig) -> None:
    """Apply GitHub repository settings via gh repo edit."""
    cmd = [
        "gh",
        "repo",
        "edit",
        cfg.repo,
        "--template",
        "--enable-issues",
        "--enable-discussions=false",
        "--enable-projects=false",
        "--enable-wiki=false",
        "--enable-squash-merge",
        "--squash-merge-commit-message",
        "pr-title",
        "--delete-branch-on-merge",
        "--default-branch",
        cfg.default_branch,
    ]

    if cfg.description:
        cmd.extend(["--description", cfg.description])
    if cfg.homepage:
        cmd.extend(["--homepage", cfg.homepage])
    for topic in cfg.topics:
        cmd.extend(["--add-topic", topic])

    run(cmd)


def configure_labels(repo: str) -> None:
    """Create or update standard labels."""
    for name, color, description in DEFAULT_LABELS:
        run(
            [
                "gh",
                "label",
                "create",
                name,
                "--repo",
                repo,
                "--color",
                color,
                "--description",
                description,
                "--force",
            ]
        )


def configure_branch_protection(cfg: RepoConfig) -> None:
    """Apply branch protection to the default branch."""
    body = {
        "required_status_checks": {
            "strict": True,
            "contexts": cfg.required_status_checks,
        },
        "enforce_admins": True,
        "required_pull_request_reviews": {
            "dismiss_stale_reviews": True,
            "require_code_owner_reviews": True,
            "required_approving_review_count": 1,
        },
        "restrictions": None,
        "required_linear_history": True,
        "allow_force_pushes": False,
        "allow_deletions": False,
        "required_conversation_resolution": True,
    }

    run(
        [
            "gh",
            "api",
            "--method",
            "PUT",
            f"repos/{cfg.repo}/branches/{cfg.default_branch}/protection",
            "--input",
            "-",
            "-H",
            "Accept: application/vnd.github+json",
        ],
        input_text=json.dumps(body),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Standardise GitHub repository settings for a template repo.",
    )
    parser.add_argument(
        "--repo",
        help="GitHub repository in OWNER/REPO format. Defaults to the current repo.",
    )
    parser.add_argument(
        "--default-branch",
        default="main",
        help="Default branch to protect and configure. Default: main",
    )
    parser.add_argument(
        "--description",
        help="Repository description to set via gh repo edit.",
    )
    parser.add_argument(
        "--homepage",
        help="Repository homepage URL to set via gh repo edit.",
    )
    parser.add_argument(
        "--topic",
        action="append",
        default=[],
        help="Repository topic to add. May be supplied multiple times.",
    )
    parser.add_argument(
        "--required-status-check",
        action="append",
        default=[],
        help=(
            "Required GitHub Actions status check name. May be supplied multiple times. "
            "Can also be comma-separated."
        ),
    )
    parser.add_argument(
        "--no-branch-protection",
        action="store_true",
        help="Skip branch protection setup.",
    )
    parser.add_argument(
        "--no-labels",
        action="store_true",
        help="Skip creating labels.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    if shutil.which("gh") is None:
        raise RuntimeError("GitHub CLI ('gh') is required but was not found on PATH.")

    parser = build_parser()
    args = parser.parse_args(argv)

    repo = args.repo or infer_repo()
    required_status_checks = split_csv(args.required_status_check)
    if not required_status_checks:
        required_status_checks = DEFAULT_REQUIRED_STATUS_CHECKS.copy()

    cfg = RepoConfig(
        repo=repo,
        default_branch=args.default_branch,
        description=args.description,
        homepage=args.homepage,
        topics=args.topic,
        required_status_checks=required_status_checks,
        apply_branch_protection=not args.no_branch_protection,
        apply_labels=not args.no_labels,
    )

    # Make sure the user is authenticated before attempting any mutations.
    run(["gh", "auth", "status"])

    configure_repository(cfg)
    if cfg.apply_labels:
        configure_labels(cfg.repo)
    if cfg.apply_branch_protection:
        configure_branch_protection(cfg)

    print(f"Configured GitHub settings for {cfg.repo}")  # noqa: T201
    print(f"Protected branch: {cfg.default_branch}")  # noqa: T201
    print("Required checks: " + ", ".join(cfg.required_status_checks))  # noqa: T201
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
