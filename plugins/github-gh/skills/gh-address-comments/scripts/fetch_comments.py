#!/usr/bin/env python3
"""
Fetch all PR conversation comments + reviews + review threads (inline threads)
for the PR associated with the current git branch, by shelling out to:

  gh api graphql

Requires:
  - GitHub CLI `gh`
  - `gh auth login` already set up
  - current branch has an associated (open) PR

If `gh` is missing on Windows, install it with:
  winget install --id GitHub.cli

Usage:
  python fetch_comments.py > pr_comments.json
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from shutil import which
from typing import Any

GH_INSTALL_HINT = "gh is not installed. Install GitHub CLI with `winget install --id GitHub.cli`."
GH_LOGIN_HINT = "gh is not authenticated. Run `gh auth login` and retry."
GH_GODEBUG_VALUE = "http2client=0"
GRAPHQL_FALLBACK_HINT = (
    "gh GraphQL transport failed. Falling back to REST review comments without thread "
    "resolution state."
)
GH_RETRY_ATTEMPTS = 4
GH_RETRY_DELAY_SECONDS = 1.0

QUERY = """\
query(
  $owner: String!,
  $repo: String!,
  $number: Int!,
  $commentsCursor: String,
  $reviewsCursor: String,
  $threadsCursor: String
) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      number
      url
      title
      state

      # Top-level "Conversation" comments (issue comments on the PR)
      comments(first: 100, after: $commentsCursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          body
          createdAt
          updatedAt
          author { login }
        }
      }

      # Review submissions (Approve / Request changes / Comment), with body if present
      reviews(first: 100, after: $reviewsCursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          state
          body
          submittedAt
          author { login }
        }
      }

      # Inline review threads (grouped), includes resolved state
      reviewThreads(first: 100, after: $threadsCursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          isResolved
          isOutdated
          path
          line
          diffSide
          startLine
          startDiffSide
          originalLine
          originalStartLine
          resolvedBy { login }
          comments(first: 100) {
            nodes {
              id
              body
              createdAt
              updatedAt
              author { login }
            }
          }
        }
      }
    }
  }
}
"""


def _resolve_gh() -> str | None:
    found = which("gh")
    if found:
        return found

    candidates = [
        Path(os.environ.get("ProgramW6432", r"C:\Program Files")) / "GitHub CLI" / "gh.exe",
        Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "GitHub CLI" / "gh.exe",
        Path(os.environ.get("LocalAppData", "")) / "Programs" / "GitHub CLI" / "gh.exe",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)
    return None


GH_EXE = _resolve_gh()


def _gh_env() -> dict[str, str]:
    env = os.environ.copy()
    env["GODEBUG"] = GH_GODEBUG_VALUE
    return env


def _is_retryable_gh_error(detail: str) -> bool:
    lowered = detail.lower()
    return (
        "eof" in lowered
        or "timeout" in lowered
        or "connection reset" in lowered
        or "tls handshake timeout" in lowered
    )


def _run(cmd: list[str], stdin: str | None = None) -> str:
    if cmd and cmd[0] == "gh":
        if GH_EXE is None:
            raise RuntimeError(GH_INSTALL_HINT)
        cmd = [GH_EXE, *cmd[1:]]

    attempts = GH_RETRY_ATTEMPTS if GH_EXE and cmd and cmd[0] == GH_EXE else 1
    last_detail = ""
    for attempt in range(1, attempts + 1):
        try:
            p = subprocess.run(cmd, input=stdin, capture_output=True, text=True, env=_gh_env())
        except FileNotFoundError as exc:
            raise RuntimeError(GH_INSTALL_HINT) from exc

        if p.returncode == 0:
            return p.stdout

        stderr = (p.stderr or "").strip()
        stdout = (p.stdout or "").strip()
        last_detail = stderr or stdout
        if attempt < attempts and _is_retryable_gh_error(last_detail):
            time.sleep(GH_RETRY_DELAY_SECONDS)
            continue
        break

    raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{last_detail}")


def _run_json(cmd: list[str], stdin: str | None = None) -> dict[str, Any]:
    out = _run(cmd, stdin=stdin)
    try:
        return json.loads(out)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse JSON from command output: {e}\nRaw:\n{out}") from e


def _run_json_any(cmd: list[str], stdin: str | None = None) -> Any:
    out = _run(cmd, stdin=stdin)
    try:
        return json.loads(out)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse JSON from command output: {e}\nRaw:\n{out}") from e


def _ensure_gh_authenticated() -> None:
    if GH_EXE is None:
        raise RuntimeError(GH_INSTALL_HINT)

    try:
        _run(["gh", "--version"])
        _run(["gh", "auth", "status"])
    except RuntimeError:
        raise RuntimeError(GH_LOGIN_HINT) from None


def gh_pr_view_json(fields: str) -> dict[str, Any]:
    # fields is a comma-separated list like: "number,headRepositoryOwner,headRepository"
    return _run_json(["gh", "pr", "view", "--json", fields])


def get_current_pr_ref() -> tuple[str, str, int]:
    """
    Resolve the PR for the current branch (whatever gh considers associated).
    Works for cross-repo PRs too, by reading head repository owner/name.
    """
    pr = gh_pr_view_json("number,headRepositoryOwner,headRepository")
    owner = pr["headRepositoryOwner"]["login"]
    repo = pr["headRepository"]["name"]
    number = int(pr["number"])
    return owner, repo, number


def gh_api_graphql(
    owner: str,
    repo: str,
    number: int,
    comments_cursor: str | None = None,
    reviews_cursor: str | None = None,
    threads_cursor: str | None = None,
) -> dict[str, Any]:
    """
    Call `gh api graphql` using -F variables, avoiding JSON blobs with nulls.
    Query is passed via stdin using query=@- to avoid shell newline/quoting issues.
    """
    cmd = [
        "gh",
        "api",
        "graphql",
        "-F",
        "query=@-",
        "-F",
        f"owner={owner}",
        "-F",
        f"repo={repo}",
        "-F",
        f"number={number}",
    ]
    if comments_cursor:
        cmd += ["-F", f"commentsCursor={comments_cursor}"]
    if reviews_cursor:
        cmd += ["-F", f"reviewsCursor={reviews_cursor}"]
    if threads_cursor:
        cmd += ["-F", f"threadsCursor={threads_cursor}"]

    return _run_json(cmd, stdin=QUERY)


def _gh_api_get_json(path: str) -> Any:
    return _run_json_any(["gh", "api", path])


def _fetch_paginated_array(path_template: str) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    page = 1
    while True:
        path = path_template.format(page=page)
        payload = _gh_api_get_json(path)
        if not isinstance(payload, list):
            raise RuntimeError(f"Expected list payload from gh api for {path}")
        items.extend(payload)
        if len(payload) < 100:
            break
        page += 1
    return items


def _pr_meta_from_rest(owner: str, repo: str, number: int) -> dict[str, Any]:
    pr = _gh_api_get_json(f"repos/{owner}/{repo}/pulls/{number}")
    if not isinstance(pr, dict):
        raise RuntimeError("Unexpected pull request metadata shape from REST API.")
    return {
        "number": pr.get("number"),
        "url": pr.get("html_url"),
        "title": pr.get("title"),
        "state": pr.get("state"),
        "owner": owner,
        "repo": repo,
    }


def fetch_all_graphql(owner: str, repo: str, number: int) -> dict[str, Any]:
    conversation_comments: list[dict[str, Any]] = []
    reviews: list[dict[str, Any]] = []
    review_threads: list[dict[str, Any]] = []

    comments_cursor: str | None = None
    reviews_cursor: str | None = None
    threads_cursor: str | None = None

    pr_meta: dict[str, Any] | None = None

    while True:
        payload = gh_api_graphql(
            owner=owner,
            repo=repo,
            number=number,
            comments_cursor=comments_cursor,
            reviews_cursor=reviews_cursor,
            threads_cursor=threads_cursor,
        )

        if "errors" in payload and payload["errors"]:
            raise RuntimeError(f"GitHub GraphQL errors:\n{json.dumps(payload['errors'], indent=2)}")

        pr = payload["data"]["repository"]["pullRequest"]
        if pr_meta is None:
            pr_meta = {
                "number": pr["number"],
                "url": pr["url"],
                "title": pr["title"],
                "state": pr["state"],
                "owner": owner,
                "repo": repo,
            }

        c = pr["comments"]
        r = pr["reviews"]
        t = pr["reviewThreads"]

        conversation_comments.extend(c.get("nodes") or [])
        reviews.extend(r.get("nodes") or [])
        review_threads.extend(t.get("nodes") or [])

        comments_cursor = c["pageInfo"]["endCursor"] if c["pageInfo"]["hasNextPage"] else None
        reviews_cursor = r["pageInfo"]["endCursor"] if r["pageInfo"]["hasNextPage"] else None
        threads_cursor = t["pageInfo"]["endCursor"] if t["pageInfo"]["hasNextPage"] else None

        if not (comments_cursor or reviews_cursor or threads_cursor):
            break

    assert pr_meta is not None
    return {
        "pull_request": pr_meta,
        "conversation_comments": conversation_comments,
        "reviews": reviews,
        "review_threads": review_threads,
    }


def fetch_all_rest(owner: str, repo: str, number: int, reason: str) -> dict[str, Any]:
    conversation_comments = _fetch_paginated_array(
        f"repos/{owner}/{repo}/issues/{number}/comments?per_page=100&page={{page}}"
    )
    reviews = _fetch_paginated_array(
        f"repos/{owner}/{repo}/pulls/{number}/reviews?per_page=100&page={{page}}"
    )
    review_comments = _fetch_paginated_array(
        f"repos/{owner}/{repo}/pulls/{number}/comments?per_page=100&page={{page}}"
    )
    return {
        "pull_request": _pr_meta_from_rest(owner, repo, number),
        "conversation_comments": conversation_comments,
        "reviews": reviews,
        "review_threads": [],
        "review_comments": review_comments,
        "fallback": {
            "mode": "rest_no_threads",
            "reason": reason,
            "note": GRAPHQL_FALLBACK_HINT,
        },
    }


def _should_fallback_to_rest(message: str) -> bool:
    lowered = message.lower()
    return "graphql" in lowered or "api.github.com/graphql" in lowered or "eof" in lowered


def fetch_all(owner: str, repo: str, number: int) -> dict[str, Any]:
    try:
        return fetch_all_graphql(owner, repo, number)
    except RuntimeError as exc:
        message = str(exc)
        if _should_fallback_to_rest(message):
            return fetch_all_rest(owner, repo, number, reason=message)
        raise


def main() -> int:
    try:
        _ensure_gh_authenticated()
        owner, repo, number = get_current_pr_ref()
        result = fetch_all(owner, repo, number)
        print(json.dumps(result, indent=2))
        return 0
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
