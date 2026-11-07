#!/usr/bin/env python3
"""Generate the self-hosted SVG cards used by the GitHub profile README.

No token is required. Data comes from public sources only:

* the public contribution calendar  (https://github.com/users/<user>/contributions)
* blob-filtered clones of the user's public non-fork repositories
  (commit dates for the project timeline, file sizes for language share)

Usage:
    python scripts/update_profile_stats.py --clones /tmp/repos --repos 18 --new-repos 5

Missing clones are created automatically with ``git clone --filter=blob:none``.
"""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import html
import json
import math
import os
import re
import subprocess
from pathlib import Path
from urllib.request import Request, urlopen

from svgkit import THEMES, open_svg

USER = "PWJCSqiushan"
TZ_ENV = {**os.environ, "TZ": "Asia/Shanghai"}

# Timeline lanes: (display name, "repo|repo|...") — public, non-fork repositories only.
TIMELINE = [
    ("Higgs", "Higgs"),
    ("Qiushan Workspace", "qiushan-workspace"),
    ("AudioDock", "audiodock"),
    ("TongChuangQS", "TongChuangQS-Public"),
    ("PIEZO1 Screening", "piezo1-virtual-screening"),
    ("Watermark Studio", "offline-watermark-studio"),
    ("Mirage Mane", "Mirage-Mane|Mirage-Mane-V2|mirage-scalp-grid-viewer"),
    ("FurColor Studio", "FurColor-Studio"),
    ("Starflare Pet", "starflare-codex-pet"),
    ("Earlier tools", "JKS|chaoxing-quiz-pdf|chaoxing-fanya|hospital-management-system|stockhub|cloudflare-edgetunnel-v2rayn-guide"),
]

EXT = {
    ".py": "Python", ".ts": "TypeScript", ".tsx": "TypeScript", ".js": "JavaScript",
    ".jsx": "JavaScript", ".mjs": "JavaScript", ".cpp": "C++", ".cc": "C++", ".h": "C++",
    ".hpp": "C++", ".html": "HTML", ".css": "CSS", ".ps1": "PowerShell", ".sh": "Shell",
}
# Vendored, bundled or third-party paths are excluded from the language share.
SKIP = ("dist/", "node_modules/", "vendor/", "third_party/", "build/", "public/", "PaddleOCR/", "skills/", "/assets/", ".min.")
LANG_COLORS = {
    "Python": "#AF85B9", "TypeScript": "#7FB8D8", "C++": "#D4909F", "JavaScript": "#E3C58E",
    "CSS": "#8FB9A8", "Other": "#7D8590",
}

def style(t: dict) -> str:
    h = t["heat"]
    return ("<style>"
            f".t{{fill:{t['text']};}} .m{{fill:{t['muted']};}} .grid{{stroke:{t['faint']};fill:none;}}"
            + "".join(f".l{i}{{fill:{c};}}" for i, c in enumerate(h))
            + f".lane{{fill:{t['lane']};}} .ring{{stroke:{t['lane']};}}"
            "</style>")


# ---------------------------------------------------------------- data

def fetch_calendar(user: str) -> list[tuple[str, int]]:
    req = Request(f"https://github.com/users/{user}/contributions", headers={"User-Agent": "profile-cards"})
    page = urlopen(req, timeout=30).read().decode("utf-8")
    ids = {m.group(2): m.group(1) for m in re.finditer(r'data-date="([\d-]+)" id="(contribution-day-component-[\d-]+)"', page)}
    counts = {}
    for m in re.finditer(r'for="(contribution-day-component-[\d-]+)"[^>]*>([^<]*)', page):
        n = re.match(r"(\d+) contribution", m.group(2))
        if m.group(1) in ids:
            counts[ids[m.group(1)]] = int(n.group(1)) if n else 0
    return sorted(counts.items())


def ensure_clone(root: Path, repo: str) -> Path:
    path = root / repo
    if not path.exists():
        subprocess.run(["git", "clone", "-q", "--filter=blob:none", f"https://github.com/{USER}/{repo}.git", str(path)], check=True)
    return path


def commit_dates(path: Path) -> list[str]:
    out = subprocess.run(["git", "-C", str(path), "log", "--format=%ad", "--date=format-local:%Y-%m-%d"],
                         capture_output=True, text=True, env=TZ_ENV, check=True).stdout
    return out.split()


def language_bytes(path: Path) -> collections.Counter:
    files = subprocess.run(["git", "-C", str(path), "ls-files"], capture_output=True, text=True, check=True).stdout.splitlines()
    c: collections.Counter = collections.Counter()
    for f in files:
        if any(s in "/" + f for s in SKIP):
            continue
        lang = EXT.get(os.path.splitext(f)[1].lower())
        p = path / f
        if lang and p.is_file() and p.stat().st_size < 400_000:
            c[lang] += p.stat().st_size
    return c


# ---------------------------------------------------------------- helpers

def level(n: int) -> int:
    return 0 if n == 0 else 1 if n < 4 else 2 if n < 10 else 3 if n < 20 else 4


def streak_and_active(days: list[tuple[str, int]]) -> tuple[int, int]:
    best = cur = 0
    for _, n in days:
        cur = cur + 1 if n else 0
        best = max(best, cur)
    return best, sum(1 for _, n in days if n)


def svg_open(w: int, h: int, title: str, desc: str, t: dict) -> list[str]:
    return open_svg(w, h, title, desc, t) + [style(t)]


def header(parts: list[str], title: str, sub: str, accent: str) -> None:
    parts += [
        f'<rect x="20" y="20" width="4" height="28" rx="2" fill="{accent}"/>',
        f'<text class="t" x="36" y="38" font-size="18" font-weight="700">{html.escape(title)}</text>',
        f'<text class="m" x="36" y="55" font-size="11">{html.escape(sub)}</text>',
    ]


def next_month(m: dt.date) -> dt.date:
    return dt.date(m.year + (m.month == 12), m.month % 12 + 1, 1)


# ---------------------------------------------------------------- cards

def activity_card(days: list[tuple[str, int]], since: dt.date, repos: int, new_repos: int, t: dict) -> str:
    total_year = sum(n for _, n in days)
    window = [(d, n) for d, n in days if dt.date.fromisoformat(d) >= since]
    best, active = streak_and_active(window)
    end = dt.date.fromisoformat(days[-1][0])
    W, H = 880, 232
    p = svg_open(W, H, f"{USER} contribution rhythm",
                 f"{total_year} contributions in the last year, {active} active days and a {best}-day longest streak since {since}.", t)
    header(p, "Contribution Rhythm", f"Public contribution calendar · {since:%Y-%m-%d} → {end:%Y-%m-%d}", "#AF85B9")

    kpis = [(f"{total_year}", "contributions / year"), (f"{active}", "active days"),
            (f"{best}", "day longest streak"), (f"{repos}", f"public repos · {new_repos} new")]
    for i, (v, label) in enumerate(kpis):
        x, y = 36 + (i % 2) * 124, 112 + (i // 2) * 64
        p.append(f'<text class="t" x="{x}" y="{y}" font-size="26" font-weight="700">{v}</text>')
        p.append(f'<text class="m" x="{x}" y="{y + 18}" font-size="10.5">{html.escape(label)}</text>')
    p.append('<path class="grid" d="M276 78V206"/>')

    # heatmap, Sunday-start weeks like GitHub
    start = since - dt.timedelta(days=(since.weekday() + 1) % 7)
    counts = dict(days)
    cell, gap, x0, y0 = 12, 3, 322, 90
    weeks = (end - start).days // 7 + 1
    for wk in range(weeks):
        first = start + dt.timedelta(days=wk * 7)
        for wd in range(7):
            d = first + dt.timedelta(days=wd)
            if since <= d <= end:
                n = counts.get(d.isoformat(), 0)
                p.append(f'<rect class="l{level(n)}" x="{x0 + wk * (cell + gap)}" y="{y0 + wd * (cell + gap)}" '
                         f'width="{cell}" height="{cell}" rx="2.5"><title>{d}: {n} contributions</title></rect>')
        last = first + dt.timedelta(days=6)
        if wk == 0 or last.month != (last - dt.timedelta(days=7)).month:
            p.append(f'<text class="m" x="{x0 + wk * (cell + gap)}" y="{y0 - 8}" font-size="10">{last:%b}</text>')
    for wd, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        p.append(f'<text class="m" x="{x0 - 7}" y="{y0 + wd * (cell + gap) + 10}" font-size="9" text-anchor="end">{name}</text>')
    right = x0 + weeks * (cell + gap) - gap
    ly = y0 + 7 * (cell + gap) + 12
    p.append(f'<text class="m" x="{right - 106}" y="{ly}" font-size="9" text-anchor="end">Less</text>')
    for i in range(5):
        p.append(f'<rect class="l{i}" x="{right - 101 + i * 15}" y="{ly - 9}" width="10" height="10" rx="2"/>')
    p.append(f'<text class="m" x="{right}" y="{ly}" font-size="9" text-anchor="end">More</text>')

    # monthly totals
    months: collections.Counter = collections.Counter()
    for d, n in window:
        months[d[:7]] += n
    keys = sorted(months)
    bx = right + 40
    p.append(f'<path class="grid" d="M{bx - 20} 78V206"/>')
    p.append(f'<text class="m" x="{bx}" y="{y0 - 8}" font-size="10">Monthly</text>')
    peak = max(months.values()) or 1
    base, maxh = 190, 84
    bw = min(24, (W - 20 - bx) // max(1, len(keys)) - 7)
    for i, k in enumerate(keys):
        v = months[k]
        h = max(2.0, maxh * v / peak)
        x = bx + i * (bw + 7)
        op = "1" if v == peak else "0.62"
        p.append(f'<rect x="{x}" y="{base - h:.1f}" width="{bw}" height="{h:.1f}" rx="3" fill="#AF85B9" fill-opacity="{op}"/>')
        p.append(f'<text class="t" x="{x + bw / 2}" y="{base - h - 5:.1f}" font-size="9.5" text-anchor="middle">{v}</text>')
        p.append(f'<text class="m" x="{x + bw / 2}" y="{base + 13}" font-size="9.5" text-anchor="middle">{dt.date.fromisoformat(k + "-01"):%b}</text>')
    p.append("</svg>")
    return "\n".join(p)


def timeline_card(lanes: list[tuple[str, list[str]]], since: dt.date, end: dt.date, t: dict) -> str:
    W, row = 495, 19
    y0 = 84
    H = y0 + row * len(lanes) + 10
    p = svg_open(W, H, f"{USER} project timeline", "Weekly commits per public project since " + since.isoformat(), t)
    header(p, "Project Timeline", f"Weekly commits per public repo · Σ = commits since {since:%b %Y}", "#A2E0F2")
    x0, x1 = 132, 424
    span = (end - since).days or 1

    def xpos(d: dt.date) -> float:
        return x0 + (x1 - x0) * (d - since).days / span

    m = dt.date(since.year, since.month, 1)
    while m <= end:
        if m >= since:
            x = xpos(m)
            p.append(f'<path class="grid" d="M{x:.1f} {y0 - 4}V{y0 + row * len(lanes) - 4}" stroke-dasharray="2 3"/>')
            p.append(f'<text class="m" x="{x + 3:.1f}" y="{y0 - 8}" font-size="9.5">{m:%b}</text>')
        m = next_month(m)
    p.append(f'<text class="m" x="{W - 20}" y="{y0 - 8}" font-size="9.5" text-anchor="end">Σ</text>')
    colors = ["#AF85B9", "#7FB8D8", "#D4909F", "#E3C58E", "#8FB9A8"]
    for i, (name, dates) in enumerate(lanes):
        y = y0 + i * row + 6
        p.append(f'<rect class="lane" x="{x0 - 6}" y="{y - 7.5}" width="{x1 - x0 + 12}" height="15" rx="7.5"/>')
        p.append(f'<text class="t" x="{x0 - 14}" y="{y + 4}" font-size="11" text-anchor="end">{html.escape(name)}</text>')
        weeks: collections.Counter = collections.Counter()
        for d in dates:
            day = dt.date.fromisoformat(d)
            if since <= day <= end:
                weeks[day - dt.timedelta(days=day.weekday())] += 1
        c = colors[i % len(colors)]
        for wk, n in sorted(weeks.items()):
            r = min(7.0, 2.3 + 1.1 * math.sqrt(n))
            cx = min(x1, max(x0, xpos(wk + dt.timedelta(days=3))))
            p.append(f'<circle cx="{cx:.1f}" cy="{y}" r="{r:.1f}" fill="{c}" fill-opacity="0.82"><title>{html.escape(name)} · week of {wk}: {n} commits</title></circle>')
        p.append(f'<text class="m" x="{W - 20}" y="{y + 4}" font-size="10.5" text-anchor="end">{sum(weeks.values())}</text>')
    p.append("</svg>")
    return "\n".join(p)


def languages_card(totals: collections.Counter, height: int, t: dict) -> str:
    W, H = 495, height
    p = svg_open(W, H, f"{USER} languages", "Language share by own source size across public non-fork repositories.", t)
    header(p, "Languages", "Own source files in public repos · vendored code excluded", "#D4909F")
    top = totals.most_common(5)
    other = sum(totals.values()) - sum(v for _, v in top)
    items = top + ([("Other", other)] if other else [])
    total = sum(v for _, v in items) or 1
    cx, cy, r, sw = 112, 72 + (H - 72) / 2, 56, 18
    circ = 2 * math.pi * r
    off = 0.0
    p.append(f'<circle class="ring" cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke-width="{sw}"/>')
    for name, v in items:
        frac = v / total
        dash = max(0.6, frac * circ - 2.5)
        p.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{LANG_COLORS.get(name, "#7D8590")}" stroke-width="{sw}" '
                 f'stroke-dasharray="{dash:.2f} {circ:.2f}" stroke-dashoffset="{-off:.2f}" transform="rotate(-90 {cx} {cy})"/>')
        off += frac * circ
    p.append(f'<text class="t" x="{cx}" y="{cy + 3}" font-size="22" font-weight="700" text-anchor="middle">{len(totals)}</text>')
    p.append(f'<text class="m" x="{cx}" y="{cy + 18}" font-size="9.5" text-anchor="middle">languages</text>')
    lx = 222
    ly = cy - (len(items) - 1) * 13 + 4
    for i, (name, v) in enumerate(items):
        y = ly + i * 26
        pct = v / total * 100
        color = LANG_COLORS.get(name, "#7D8590")
        p.append(f'<circle cx="{lx}" cy="{y - 4}" r="5" fill="{color}"/>')
        p.append(f'<text class="t" x="{lx + 14}" y="{y}" font-size="12">{html.escape(name)}</text>')
        p.append(f'<rect class="lane" x="{lx + 102}" y="{y - 8.5}" width="96" height="8" rx="4"/>')
        p.append(f'<rect x="{lx + 102}" y="{y - 8.5}" width="{max(3.0, 96 * pct / 100):.1f}" height="8" rx="4" fill="{color}"/>')
        p.append(f'<text class="m" x="{W - 20}" y="{y}" font-size="11" text-anchor="end">{pct:.1f}%</text>')
    p.append("</svg>")
    return "\n".join(p)


# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--clones", type=Path, default=Path("profile-data/repos"))
    ap.add_argument("--since", default="2026-06-01", help="start of heatmap / timeline window")
    ap.add_argument("--repos", type=int, required=True, help="number of public non-fork repositories")
    ap.add_argument("--new-repos", type=int, required=True, help="repositories created since the previous refresh")
    ap.add_argument("--output", type=Path, default=Path("assets"))
    a = ap.parse_args()
    since = dt.date.fromisoformat(a.since)

    days = fetch_calendar(USER)
    end = dt.date.fromisoformat(days[-1][0])
    a.clones.mkdir(parents=True, exist_ok=True)

    lanes, langs = [], collections.Counter()
    for name, spec in TIMELINE:
        dates: list[str] = []
        for repo in spec.split("|"):
            path = ensure_clone(a.clones, repo)
            dates += commit_dates(path)
            langs += language_bytes(path)
        lanes.append((name, dates))

    a.output.mkdir(parents=True, exist_ok=True)
    for theme, t in THEMES.items():
        timeline = timeline_card(lanes, since, end, t)
        height = int(re.search(r'height="(\d+)"', timeline).group(1))
        (a.output / f"activity-overview-{theme}.svg").write_text(activity_card(days, since, a.repos, a.new_repos, t), encoding="utf-8", newline="\n")
        (a.output / f"project-timeline-{theme}.svg").write_text(timeline, encoding="utf-8", newline="\n")
        (a.output / f"top-languages-{theme}.svg").write_text(languages_card(langs, height, t), encoding="utf-8", newline="\n")
    best, active = streak_and_active([(d, n) for d, n in days if dt.date.fromisoformat(d) >= since])
    snapshot = {
        "generated": dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).isoformat(timespec="minutes"),
        "calendar_end": end.isoformat(),
        "contributions_last_year": sum(n for _, n in days),
        "window_since": a.since,
        "active_days": active,
        "longest_streak": best,
        "public_repos": a.repos,
        "new_repos": a.new_repos,
        "commits_per_lane": {n: len(d) for n, d in lanes},
        "language_bytes": langs.most_common(),
    }
    (a.output / "profile-snapshot.json").write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(snapshot, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
