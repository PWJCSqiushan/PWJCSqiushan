#!/usr/bin/env python3
"""Generate self-hosted SVG cards for the GitHub profile README.

The script uses only Python's standard library. It reads public account data
through GitHub's GraphQL API and writes deterministic SVG assets into the
profile repository, avoiding runtime dependencies on public stats-card hosts.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen


GRAPHQL_URL = "https://api.github.com/graphql"
PALETTE = ["#AF85B9", "#A2E0F2", "#D4909F", "#668099", "#CFA2B0"]


def github_graphql(token: str, query: str, variables: dict[str, Any]) -> dict[str, Any]:
    body = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    request = Request(
        GRAPHQL_URL,
        data=body,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "PWJCSqiushan-profile-stats",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        method="POST",
    )
    with urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if payload.get("errors"):
        messages = "; ".join(item.get("message", "Unknown GraphQL error") for item in payload["errors"])
        raise RuntimeError(messages)
    return payload["data"]


def fetch_profile(token: str, username: str) -> tuple[dict[str, int], list[tuple[str, int, str]]]:
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    start = now - dt.timedelta(days=365)
    query = """
    query ProfileStats($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) {
        repositories(
          first: 100
          ownerAffiliations: OWNER
          privacy: PUBLIC
          isFork: false
          orderBy: {field: UPDATED_AT, direction: DESC}
        ) {
          totalCount
          nodes {
            stargazerCount
            forkCount
            languages(first: 20, orderBy: {field: SIZE, direction: DESC}) {
              edges {
                size
                node { name color }
              }
            }
          }
        }
        contributionsCollection(from: $from, to: $to) {
          contributionCalendar { totalContributions }
          totalCommitContributions
          totalPullRequestContributions
          totalIssueContributions
          totalPullRequestReviewContributions
        }
      }
    }
    """
    data = github_graphql(
        token,
        query,
        {"login": username, "from": start.isoformat(), "to": now.isoformat()},
    )
    user = data.get("user")
    if not user:
        raise RuntimeError(f"GitHub user not found: {username}")

    repositories = user["repositories"]
    contributions = user["contributionsCollection"]
    stats = {
        "repositories": repositories["totalCount"],
        "contributions": contributions["contributionCalendar"]["totalContributions"],
        "commits": contributions["totalCommitContributions"],
        "pull_requests": contributions["totalPullRequestContributions"],
        "stars": sum(repo["stargazerCount"] for repo in repositories["nodes"]),
    }

    totals: dict[str, dict[str, Any]] = {}
    for repository in repositories["nodes"]:
        for edge in repository["languages"]["edges"]:
            name = edge["node"]["name"]
            entry = totals.setdefault(name, {"size": 0, "color": edge["node"].get("color")})
            entry["size"] += edge["size"]
            if not entry["color"] and edge["node"].get("color"):
                entry["color"] = edge["node"]["color"]

    languages = [
        (name, values["size"], values["color"] or PALETTE[index % len(PALETTE)])
        for index, (name, values) in enumerate(
            sorted(totals.items(), key=lambda item: item[1]["size"], reverse=True)[:5]
        )
    ]
    return stats, languages


def svg_style() -> str:
    return """
    <style>
      text { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; }
      .card { fill: #0d1117; stroke: #30363d; }
      .title { fill: #f0f6fc; font-size: 20px; font-weight: 700; }
      .subtitle, .label, .footnote { fill: #8b949e; }
      .value { fill: #f0f6fc; font-size: 24px; font-weight: 700; }
      .label { font-size: 11px; }
      .subtitle, .footnote { font-size: 11px; }
      .track { fill: #21262d; }
      @media (prefers-color-scheme: light) {
        .card { fill: #ffffff; stroke: #d0d7de; }
        .title, .value { fill: #24292f; }
        .subtitle, .label, .footnote { fill: #57606a; }
        .track { fill: #eaeef2; }
      }
    </style>
    """.strip()


def compact_number(value: int) -> str:
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}m"
    if value >= 1_000:
        return f"{value / 1_000:.1f}k"
    return str(value)


def overview_svg(username: str, stats: dict[str, int]) -> str:
    metrics = [
        ("PUBLIC REPOS", stats["repositories"]),
        ("CONTRIBUTIONS", stats["contributions"]),
        ("COMMITS", stats["commits"]),
        ("PULL REQUESTS", stats["pull_requests"]),
        ("STARS", stats["stars"]),
    ]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="495" height="190" viewBox="0 0 495 190" role="img" aria-labelledby="title desc">',
        f'<title id="title">{html.escape(username)} GitHub overview</title>',
        '<desc id="desc">Public repository and contribution statistics for the past twelve months.</desc>',
        svg_style(),
        '<rect class="card" x="0.75" y="0.75" width="493.5" height="188.5" rx="12"/>',
        '<rect x="20" y="20" width="4" height="28" rx="2" fill="#AF85B9"/>',
        '<text class="title" x="36" y="38">GitHub Overview</text>',
        '<text class="subtitle" x="36" y="55">Public activity · rolling 12 months</text>',
        '<path d="M20 70H475" stroke="#30363d" stroke-opacity="0.75"/>',
    ]
    for index, (label, value) in enumerate(metrics):
        x = 49.5 + index * 99
        parts.append(f'<text class="value" x="{x}" y="116" text-anchor="middle">{compact_number(value)}</text>')
        parts.append(f'<text class="label" x="{x}" y="139" text-anchor="middle">{label}</text>')
        if index < len(metrics) - 1:
            divider_x = 99 + index * 99
            parts.append(f'<path d="M{divider_x} 88V146" stroke="#30363d" stroke-opacity="0.7"/>')
    parts.extend(
        [
            '<circle cx="22" cy="169" r="3" fill="#A2E0F2"/>',
            '<text class="footnote" x="32" y="173">Generated from GitHub public data</text>',
            "</svg>",
        ]
    )
    return "\n".join(parts)


def languages_svg(username: str, languages: list[tuple[str, int, str]]) -> str:
    total = sum(size for _, size, _ in languages) or 1
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="495" height="190" viewBox="0 0 495 190" role="img" aria-labelledby="title desc">',
        f'<title id="title">{html.escape(username)} most used repository languages</title>',
        '<desc id="desc">Language distribution by code size across non-fork public repositories.</desc>',
        svg_style(),
        '<rect class="card" x="0.75" y="0.75" width="493.5" height="188.5" rx="12"/>',
        '<rect x="20" y="20" width="4" height="28" rx="2" fill="#A2E0F2"/>',
        '<text class="title" x="36" y="38">Most Used Languages</text>',
        '<text class="subtitle" x="36" y="55">Non-fork public repositories · code size</text>',
    ]
    if not languages:
        parts.append('<text class="subtitle" x="247.5" y="112" text-anchor="middle">No public language data yet</text>')
    else:
        for index, (name, size, color) in enumerate(languages):
            y = 79 + index * 21
            percent = size / total * 100
            width = max(3.0, 270 * percent / 100)
            safe_name = html.escape(name)
            parts.append(f'<circle cx="25" cy="{y - 3}" r="4" fill="{color}"/>')
            parts.append(f'<text class="label" x="36" y="{y}">{safe_name}</text>')
            parts.append(f'<rect class="track" x="133" y="{y - 10}" width="270" height="9" rx="4.5"/>')
            parts.append(f'<rect x="133" y="{y - 10}" width="{width:.1f}" height="9" rx="4.5" fill="{color}"/>')
            parts.append(f'<text class="label" x="467" y="{y}" text-anchor="end">{percent:.1f}%</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", default=os.environ.get("GITHUB_REPOSITORY_OWNER", "PWJCSqiushan"))
    parser.add_argument("--output", type=Path, default=Path("assets"))
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN or GH_TOKEN is required")

    stats, languages = fetch_profile(token, args.username)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "github-overview.svg").write_text(overview_svg(args.username, stats), encoding="utf-8", newline="\n")
    (args.output / "top-languages.svg").write_text(languages_svg(args.username, languages), encoding="utf-8", newline="\n")
    print(f"Generated profile cards for {args.username}: {stats}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
