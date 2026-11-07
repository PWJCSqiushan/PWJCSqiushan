"""Shared theme tokens and tiny SVG helpers for the profile README cards.

Every card is rendered twice (dark / light) and switched in the README with
``<picture><source media="(prefers-color-scheme: dark)">`` so that it follows
the reader's GitHub theme instead of the operating-system setting.
"""

from __future__ import annotations

import html
import unicodedata

FONT = ("-apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', "
        "'Noto Sans CJK SC', 'Noto Sans SC', 'Noto Sans Mono CJK SC', Arial, sans-serif")
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"

# Brand accents (shared with banner.svg)
PURPLE, CYAN, ROSE, GOLD, SAGE = "#AF85B9", "#7FB8D8", "#D4909F", "#E3C58E", "#8FB9A8"

THEMES = {
    "dark": {
        "bg0": "#0f1520", "bg1": "#161d2b", "stroke": "#30363d",
        "text": "#e6edf3", "muted": "#8b949e", "faint": "#30363d",
        "panel": "#121a27", "panel_grid": "#e8eae7", "panel_grid_op": "0.05",
        "lane": "#1c2330", "ink": "#0f1520",
        "heat": ["#1c2330", "#3d3150", "#634a7c", "#8d6a9f", "#c9a3d6"],
        "chip_op": "0.16",
        "accent_text": {PURPLE: "#d2b6dc", CYAN: "#a9d4ec", ROSE: "#e7b4bf", GOLD: "#eed7aa", SAGE: "#b5d4c7"},
    },
    "light": {
        "bg0": "#ffffff", "bg1": "#f8f5fb", "stroke": "#d0d7de",
        "text": "#1f2328", "muted": "#59636e", "faint": "#d8dee4",
        "panel": "#f4f0f8", "panel_grid": "#5b4a6b", "panel_grid_op": "0.06",
        "lane": "#eef1f4", "ink": "#ffffff",
        "heat": ["#eef1f4", "#e9dcef", "#cfb2dc", "#af85b9", "#7a5590"],
        "chip_op": "0.14",
        "accent_text": {PURPLE: "#7a5590", CYAN: "#2f6f93", ROSE: "#a4536a", GOLD: "#8a6a24", SAGE: "#3f7564"},
    },
}


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def text_width(s: str, size: float) -> float:
    """Rough rendered width; CJK glyphs are ~1em, Latin ~0.58em."""
    w = 0.0
    for ch in s:
        if unicodedata.east_asian_width(ch) in "WF":
            w += 1.0
        elif ch in "il.,:;|!'·":
            w += 0.3
        elif ch.isupper() or ch in "mwMW@":
            w += 0.68
        else:
            w += 0.56
    return w * size


def open_svg(w: int, h: int, title: str, desc: str, t: dict, extra_defs: str = "") -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{esc(title)}</title><desc id="desc">{esc(desc)}</desc>',
        "<defs>",
        f'<linearGradient id="cardbg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{t["bg0"]}"/><stop offset="1" stop-color="{t["bg1"]}"/></linearGradient>',
        f'<pattern id="grid" width="22" height="22" patternUnits="userSpaceOnUse"><path d="M22 0H0V22" fill="none" stroke="{t["panel_grid"]}" stroke-opacity="{t["panel_grid_op"]}"/></pattern>',
        extra_defs,
        "</defs>",
        f'<style>text{{font-family:{FONT};}} .mono{{font-family:{MONO};}}</style>',
        f'<rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="14" fill="url(#cardbg)" stroke="{t["stroke"]}" stroke-width="1.5"/>',
    ]


def chip(x: float, y: float, label: str, color: str, t: dict, size: float = 11) -> tuple[str, float]:
    w = text_width(label, size) + 18
    s = (f'<rect x="{x:.1f}" y="{y - 14:.1f}" width="{w:.1f}" height="21" rx="10.5" fill="{color}" fill-opacity="{t["chip_op"]}"/>'
         f'<text x="{x + w / 2:.1f}" y="{y:.1f}" font-size="{size}" font-weight="600" text-anchor="middle" fill="{t["accent_text"][color]}">{esc(label)}</text>')
    return s, w


def chips(x: float, y: float, labels: list[str], color: str, t: dict, gap: float = 7) -> str:
    out = []
    for lab in labels:
        s, w = chip(x, y, lab, color, t)
        out.append(s)
        x += w + gap
    return "".join(out)
