#!/usr/bin/env python3
"""Render the illustrated "Featured Work" cards (zh / en × dark / light).

    python scripts/build_project_cards.py --output assets/cards

The illustrations are hand-written vector art that share the banner palette,
so every card stays consistent with the rest of the profile.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from svgkit import CYAN, GOLD, PURPLE, ROSE, SAGE, THEMES, chips, esc, open_svg, text_width

W, H = 880, 300
PANEL_W, PANEL_H = 336, 252

PROJECTS = {
    "higgs": {
        "accent": PURPLE, "art": "higgs", "side": "right",
        "zh": {
            "index": "01", "status": "持续开发 · 256 次提交",
            "title": "Higgs", "tagline": "有记忆、也有边界的自托管 QQ 智能体",
            "points": ["NapCat / OneBot + 官方 QQ Bot 双通道接入",
                       "Persona 2.2 上线，人格核心不被聊天改写",
                       "观察 → 候选 → 审核 → 激活的可治理长期记忆",
                       "3.0：群聊理解、工具调用、QQ 空间与多模态"],
        },
        "en": {
            "index": "01", "status": "ACTIVE · 256 COMMITS",
            "title": "Higgs", "tagline": "A self-hosted QQ agent with memory — and boundaries",
            "points": ["Dual channel: NapCat / OneBot + official QQ Bot",
                       "Persona 2.2 live; chats cannot rewrite its core",
                       "Governed memory: observe → candidate → review → active",
                       "3.0: group context, tool calls, QZone, multimodal"],
        },
        "tags": ["Python", "SQLite", "OneBot", "Docker", "AI Agent"],
    },
    "workspace": {
        "accent": CYAN, "art": "workspace", "side": "left",
        "zh": {
            "index": "02", "status": "每日在用",
            "title": "丘山流调", "tagline": "让每件事有归属，让下一步有顺序",
            "points": ["九条工作流管理学习、科研、开发与学生工作",
                       "跨流唯一的连续协调编号，完成后自动补位",
                       "多设备同步、离线草稿与冲突确认",
                       "统计总览、每日例行与备份恢复"],
        },
        "en": {
            "index": "02", "status": "DAILY DRIVER",
            "title": "Qiushan Workspace", "tagline": "Every task has a home; every next step has an order",
            "points": ["Nine workflows for study, research, dev, and duties",
                       "One continuous coordination number across flows",
                       "Multi-device sync, offline drafts, conflict review",
                       "Analytics overview, daily routines, backup & restore"],
        },
        "tags": ["TypeScript", "React", "Cloudflare Workers", "D1"],
    },
    "mirage": {
        "accent": ROSE, "art": "mirage", "side": "right",
        "zh": {
            "index": "03", "status": "已上线 · 2026-10",
            "title": "Mirage 三维美发教学", "tagline": "把剪发教学的点、线、分区放进三维空间",
            "points": ["1.0 验证抓发、梳理、剪切与造型的实时发丝交互",
                       "V2 以真实头模组织点线、分区与发片图层",
                       "五款头模统一编号的头皮经纬网格",
                       "商业版通过甲方验收，已正式上线"],
        },
        "en": {
            "index": "03", "status": "SHIPPED · 2026-10",
            "title": "Mirage 3D Hair Teaching", "tagline": "Haircut lessons as points, lines, and sections in 3D",
            "points": ["1.0: real-time strands to grab, comb, cut, and style",
                       "V2: teaching layers on real head models",
                       "A numbered scalp grid shared by five head models",
                       "Commercial edition accepted and live since Oct"],
        },
        "tags": ["React", "Three.js", "WebGL", "Nginx"],
    },
}


# ---------------------------------------------------------------- illustrations
# Each function draws inside a PANEL_W × PANEL_H box whose origin is (0, 0).

# ---- shared "flat UI mock-up" helpers (same language as the workspace art)

def ui_window(o: list, t: dict, x: float = 14, y: float = 20, w: float = 236, h: float = 160) -> None:
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{t["ink"]}" stroke="{t["muted"]}" stroke-opacity="0.6" stroke-width="1.5"/>')
    for i, c in enumerate((ROSE, GOLD, SAGE)):
        o.append(f'<circle cx="{x + 14 + i * 10}" cy="{y + 12}" r="3" fill="{c}"/>')
    o.append(f'<rect x="{x + 58}" y="{y + 8}" width="110" height="8" rx="4" fill="{t["lane"]}"/>')


def ui_side(o: list, t: dict, x: float = 270, y: float = 66, w: float = 52, h: float = 96) -> None:
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{t["ink"]}" stroke="{t["muted"]}" stroke-opacity="0.6" stroke-width="1.5"/>')
    o.append(f'<rect x="{x + w / 2 - 8}" y="{y + 6}" width="16" height="3" rx="1.5" fill="{t["lane"]}"/>')


def ui_lines(o: list, t: dict, x: float, y: float, a: float = 30, b: float = 20) -> None:
    o.append(f'<rect x="{x}" y="{y}" width="{a}" height="4" rx="2" fill="{t["muted"]}" fill-opacity="0.7"/>')
    if b:
        o.append(f'<rect x="{x}" y="{y + 9}" width="{b}" height="4" rx="2" fill="{t["muted"]}" fill-opacity="0.4"/>')


def ui_caption(o: list, t: dict, label: str, y: float = 222) -> None:
    o.append(f'<text x="14" y="{y}" font-size="10" font-weight="700" letter-spacing="1.5" fill="{t["muted"]}">{esc(label)}</text>')


def art_higgs(t: dict, lang: str) -> str:
    o: list[str] = []
    ui_window(o, t)
    # conversation list
    o.append(f'<path d="M84 44V172" stroke="{t["lane"]}" stroke-width="1.5"/>')
    for i, (c, on) in enumerate(((PURPLE, True), (CYAN, False), (ROSE, False), (SAGE, False))):
        y = 48 + i * 30
        if on:
            o.append(f'<rect x="20" y="{y - 4}" width="58" height="26" rx="6" fill="{PURPLE}" fill-opacity="0.22"/>')
        o.append(f'<circle cx="32" cy="{y + 9}" r="7" fill="{c}"/>')
        ui_lines(o, t, 44, y + 3, 28, 18)
    # chat thread
    o.append(f'<rect x="94" y="46" width="88" height="26" rx="8" fill="{t["lane"]}"/>')
    ui_lines(o, t, 102, 53, 56, 38)
    o.append(f'<rect x="146" y="80" width="94" height="26" rx="8" fill="{PURPLE}" fill-opacity="0.85"/>')
    o.append(f'<rect x="154" y="87" width="60" height="4" rx="2" fill="#ffffff" fill-opacity="0.85"/>'
             f'<rect x="154" y="96" width="40" height="4" rx="2" fill="#ffffff" fill-opacity="0.55"/>')
    # reminder bubble
    o.append(f'<rect x="94" y="114" width="100" height="26" rx="8" fill="{t["lane"]}"/>')
    o.append(f'<circle cx="107" cy="127" r="6" fill="none" stroke="{GOLD}" stroke-width="1.8"/>'
             f'<path d="M107 124v3l2 1.5" fill="none" stroke="{GOLD}" stroke-width="1.6" stroke-linecap="round"/>')
    ui_lines(o, t, 119, 121, 56, 36)
    # typing dots
    o.append(f'<rect x="94" y="148" width="40" height="18" rx="9" fill="{t["lane"]}"/>')
    for i in range(3):
        o.append(f'<circle cx="{106 + i * 8}" cy="157" r="2.4" fill="{t["muted"]}" fill-opacity="{0.9 - i * 0.25}"/>')
    # side panel: memory cards awaiting review
    ui_side(o, t)
    for i, (c, mark) in enumerate(((CYAN, "dot"), (GOLD, "dot"), (PURPLE, "check"))):
        y = 82 + i * 24
        o.append(f'<rect x="277" y="{y}" width="38" height="19" rx="4" fill="{t["lane"]}"/>')
        o.append(f'<rect x="277" y="{y}" width="3" height="19" rx="1.5" fill="{c}"/>')
        if mark == "check":
            o.append(f'<circle cx="307" cy="{y + 9.5}" r="5.5" fill="{PURPLE}"/>'
                     f'<path d="M304.5 {y + 9.5}l2 2 3.5-4" fill="none" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>')
        else:
            o.append(f'<circle cx="307" cy="{y + 9.5}" r="5" fill="{c}"/>')
    # shield above the side panel (owner permissions)
    o.append(f'<path d="M296 33l13 5v9c0 9-6 14-13 17-7-3-13-8-13-17v-9z" fill="none" stroke="{SAGE}" stroke-width="2" stroke-linejoin="round"/>'
             f'<path d="M290.5 48l4 4 7-8" fill="none" stroke="{SAGE}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    # memory flow strip
    ui_caption(o, t, "记忆流转" if lang == "zh" else "MEMORY FLOW")
    xs = [110, 168, 226, 284]
    o.append(f'<path d="M{xs[0]} 232H{xs[-1]}" stroke="{t["lane"]}" stroke-width="4" stroke-linecap="round"/>')
    o.append(f'<path d="M{xs[0]} 232H{xs[2]}" stroke="{PURPLE}" stroke-opacity="0.45" stroke-width="4" stroke-linecap="round"/>')
    for i, (x, c) in enumerate(zip(xs, (t["muted"], CYAN, GOLD, PURPLE))):
        o.append(f'<circle cx="{x}" cy="232" r="{8 if i == 3 else 6}" fill="{c}"/>')
    o.append(f'<path d="M{xs[3] - 3.5} 232l2.5 2.5 4.5-5" fill="none" stroke="#ffffff" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')
    return "".join(o)


def art_workspace(t: dict, lang: str) -> str:
    o = []
    # laptop
    o.append(f'<rect x="14" y="20" width="236" height="160" rx="10" fill="{t["ink"]}" stroke="{t["muted"]}" stroke-opacity="0.6" stroke-width="1.5"/>')
    for i, c in enumerate((ROSE, GOLD, SAGE)):
        o.append(f'<circle cx="{28 + i * 10}" cy="32" r="3" fill="{c}"/>')
    o.append(f'<rect x="72" y="28" width="110" height="8" rx="4" fill="{t["lane"]}"/>')
    o.append(f'<path d="M2 186H262L252 196H12Z" fill="{t["lane"]}" stroke="{t["muted"]}" stroke-opacity="0.5"/>')
    cols = [(CYAN, [(1, ROSE, True), (4, GOLD, False), (7, SAGE, False)]),
            (PURPLE, [(2, ROSE, False), (5, PURPLE, True)]),
            (GOLD, [(3, GOLD, False), (6, CYAN, False), (8, SAGE, False)])]
    for ci, (hc, cards) in enumerate(cols):
        x = 24 + ci * 74
        o.append(f'<rect x="{x}" y="46" width="68" height="6" rx="3" fill="{hc}" fill-opacity="0.85"/>')
        for ri, (num, pc, flag) in enumerate(cards):
            y = 60 + ri * 37
            fill = PURPLE if flag else t["lane"]
            op = "0.22" if flag else "1"
            o.append(f'<rect x="{x}" y="{y}" width="68" height="31" rx="6" fill="{fill}" fill-opacity="{op}"/>')
            o.append(f'<rect x="{x}" y="{y}" width="4" height="31" rx="2" fill="{pc}"/>')
            o.append(f'<rect x="{x + 10}" y="{y + 9}" width="30" height="4" rx="2" fill="{t["muted"]}" fill-opacity="0.7"/>')
            o.append(f'<rect x="{x + 10}" y="{y + 18}" width="20" height="4" rx="2" fill="{t["muted"]}" fill-opacity="0.4"/>')
            o.append(f'<circle cx="{x + 55}" cy="{y + 15.5}" r="8.5" fill="{CYAN}"/>')
            o.append(f'<text x="{x + 55}" y="{y + 19.5}" font-size="10.5" font-weight="800" text-anchor="middle" fill="#0f1520">{num}</text>')
    # phone
    o.append(f'<rect x="270" y="66" width="52" height="96" rx="10" fill="{t["ink"]}" stroke="{t["muted"]}" stroke-opacity="0.6" stroke-width="1.5"/>')
    o.append(f'<rect x="288" y="72" width="16" height="3" rx="1.5" fill="{t["lane"]}"/>')
    for i, c in enumerate((ROSE, PURPLE, SAGE)):
        y = 82 + i * 24
        o.append(f'<rect x="277" y="{y}" width="38" height="19" rx="4" fill="{t["lane"]}"/>')
        o.append(f'<rect x="277" y="{y}" width="3" height="19" rx="1.5" fill="{c}"/>')
        o.append(f'<circle cx="307" cy="{y + 9.5}" r="5" fill="{CYAN}"/>')
    # sync arrows
    o.append(f'<path d="M282 48a14 14 0 0 1 24-4" fill="none" stroke="{CYAN}" stroke-width="2" stroke-linecap="round"/>'
             f'<path d="M306 37v7h-7" fill="none" stroke="{CYAN}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
             f'<path d="M310 54a14 14 0 0 1-24 4" fill="none" stroke="{CYAN}" stroke-width="2" stroke-linecap="round"/>'
             f'<path d="M286 65v-7h7" fill="none" stroke="{CYAN}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    # analytics strip
    o.append(f'<text x="14" y="222" font-size="10" font-weight="700" letter-spacing="1.5" fill="{t["muted"]}">{"统计总览" if lang == "zh" else "ANALYTICS"}</text>')
    vals = [8, 14, 11, 20, 16, 24, 19, 28, 22, 26, 31, 25]
    for i, v in enumerate(vals):
        x = 100 + i * 18
        c = CYAN if i == len(vals) - 2 else PURPLE
        o.append(f'<rect x="{x}" y="{240 - v}" width="11" height="{v}" rx="3" fill="{c}" fill-opacity="{0.95 if c == CYAN else 0.45}"/>')
    return "".join(o)


def art_mirage(t: dict, lang: str) -> str:
    o: list[str] = []
    ui_window(o, t)
    # tool rail
    o.append(f'<rect x="22" y="40" width="26" height="132" rx="7" fill="{t["lane"]}"/>')
    for i in range(5):
        y = 48 + i * 24
        on = i == 2
        o.append(f'<rect x="26" y="{y}" width="18" height="18" rx="5" fill="{ROSE if on else t["ink"]}" fill-opacity="{0.9 if on else 1}"/>')
    # tiny glyphs: comb, brush, scissors(active), clipper, dryer — kept abstract
    o.append(f'<path d="M30 57h10M31 53v4M34 53v4M37 53v4" stroke="{t["muted"]}" stroke-width="1.3" stroke-linecap="round"/>')
    o.append(f'<circle cx="35" cy="81" r="4" fill="none" stroke="{t["muted"]}" stroke-width="1.3"/>')
    o.append(f'<g stroke="#ffffff" stroke-width="1.4" fill="none" stroke-linecap="round"><circle cx="31" cy="108" r="2.3"/><circle cx="31" cy="114" r="2.3"/><path d="M33 109.5l7 4.5M33 112.5l7-4.5"/></g>')
    o.append(f'<rect x="31" y="126" width="8" height="10" rx="2" fill="none" stroke="{t["muted"]}" stroke-width="1.3"/>')
    o.append(f'<path d="M30 154h7a3 3 0 0 0 0-6h-7z" fill="none" stroke="{t["muted"]}" stroke-width="1.3"/>')
    # viewport: flat head with bob, scalp points and a cut line
    cx, cy = 140, 104
    o.append(f'<rect x="56" y="40" width="186" height="132" rx="7" fill="{t["lane"]}" fill-opacity="0.55"/>')
    o.append(f'<path d="M{cx - 14} {cy + 40}v22M{cx + 14} {cy + 40}v22" stroke="{t["muted"]}" stroke-opacity="0.5" stroke-width="1.5"/>')
    o.append(f'<path d="M{cx - 46} {cy + 46}C{cx - 48} {cy - 6} {cx - 40} {cy - 52} {cx} {cy - 52}C{cx + 40} {cy - 52} {cx + 48} {cy - 6} {cx + 46} {cy + 46}Z" fill="{PURPLE}" fill-opacity="0.75"/>')
    o.append(f'<ellipse cx="{cx}" cy="{cy + 8}" rx="27" ry="36" fill="{t["ink"]}"/><ellipse cx="{cx}" cy="{cy + 8}" rx="27" ry="36" fill="{t["muted"]}" fill-opacity="0.22"/>')
    o.append(f'<path d="M{cx - 30} {cy - 14}C{cx - 22} {cy - 40} {cx + 22} {cy - 40} {cx + 30} {cy - 14}C{cx + 14} {cy - 22} {cx - 14} {cy - 22} {cx - 30} {cy - 14}Z" fill="{PURPLE}"/>')
    for dx in (-36, -24, 24, 36):
        o.append(f'<path d="M{cx + dx} {cy - 10}V{cy + 40}" stroke="#ffffff" stroke-opacity="0.28" stroke-width="1.3" stroke-linecap="round"/>')
    o.append(f'<path d="M{cx - 40} {cy - 30}Q{cx} {cy - 46} {cx + 40} {cy - 30}" fill="none" stroke="{CYAN}" stroke-width="1.4" stroke-dasharray="3 3"/>')
    for x, y in ((cx - 40, cy - 30), (cx - 20, cy - 37), (cx, cy - 39), (cx + 20, cy - 37), (cx + 40, cy - 30)):
        o.append(f'<circle cx="{x}" cy="{y}" r="3.2" fill="{GOLD}"/>')
    o.append(f'<path d="M{cx - 66} {cy + 50}L{cx + 70} {cy + 42}" stroke="{CYAN}" stroke-width="1.8" stroke-dasharray="5 4" stroke-linecap="round"/>')
    o.append(f'<g transform="translate({cx + 80} {cy + 40}) rotate(-12)" fill="none" stroke="{t["text"]}" stroke-width="1.6" stroke-linecap="round">'
             f'<circle cx="-6" cy="-4" r="3.6"/><circle cx="-6" cy="5" r="3.6"/><path d="M-3 -2l13 6M-3 3l13-6"/></g>')
    # side panel: section / layer list
    ui_side(o, t)
    for i, c in enumerate((PURPLE, ROSE, CYAN)):
        y = 82 + i * 24
        o.append(f'<rect x="277" y="{y}" width="38" height="19" rx="4" fill="{t["lane"]}"/>')
        o.append(f'<rect x="277" y="{y}" width="3" height="19" rx="1.5" fill="{c}"/>')
        o.append(f'<rect x="284" y="{y + 7.5}" width="14" height="4" rx="2" fill="{t["muted"]}" fill-opacity="0.6"/>')
        o.append(f'<circle cx="307" cy="{y + 9.5}" r="5" fill="{c}" fill-opacity="{1 if i < 2 else 0.35}"/>')
    # layers glyph above the panel
    o.append(f'<path d="M296 34l14 7-14 7-14-7z" fill="none" stroke="{ROSE}" stroke-width="2" stroke-linejoin="round"/>'
             f'<path d="M282 47l14 7 14-7" fill="none" stroke="{ROSE}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    # scalp grid strip
    ui_caption(o, t, "头皮网格" if lang == "zh" else "SCALP GRID")
    arc = [2, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 2]
    lit = {(arc[c_], c_) for c_ in range(12)}
    for r_ in range(3):
        for c_ in range(12):
            x, y = 100 + c_ * 18, 214 + r_ * 11
            on = (r_, c_) in lit
            o.append(f'<circle cx="{x + 5}" cy="{y + 4}" r="{3.2 if on else 2.2}" fill="{ROSE if on else t["muted"]}" fill-opacity="{0.95 if on else 0.35}"/>')
    return "".join(o)


ARTS = {"higgs": art_higgs, "workspace": art_workspace, "mirage": art_mirage}


# ---------------------------------------------------------------- card

def card(key: str, lang: str, theme: str) -> str:
    p = PROJECTS[key]
    c = p[lang]
    t = THEMES[theme]
    accent = p["accent"]
    out = open_svg(W, H, f'{c["title"]} — {c["tagline"]}', " · ".join(c["points"]), t)

    px = W - PANEL_W - 24 if p["side"] == "right" else 24
    tx = 40 if p["side"] == "right" else 24 + PANEL_W + 36
    py = (H - PANEL_H) / 2

    # illustration panel
    out.append(f'<rect x="{px}" y="{py}" width="{PANEL_W}" height="{PANEL_H}" rx="12" fill="{t["panel"]}"/>')
    out.append(f'<rect x="{px}" y="{py}" width="{PANEL_W}" height="{PANEL_H}" rx="12" fill="url(#grid)"/>')
    out.append(f'<g transform="translate({px} {py})">{ARTS[p["art"]](t, lang)}</g>')

    # text column
    out.append(f'<text class="mono" x="{tx}" y="58" font-size="15" font-weight="700" fill="{accent}">{c["index"]}</text>')
    out.append(f'<path d="M{tx + 26} 53H{tx + 52}" stroke="{accent}" stroke-width="2" stroke-linecap="round"/>')
    sw = text_width(c["status"], 10) + 0.8 * len(c["status"]) + 22
    out.append(f'<rect x="{tx + 62}" y="41" width="{sw:.1f}" height="22" rx="11" fill="none" stroke="{accent}" stroke-opacity="0.7"/>')
    out.append(f'<text x="{tx + 62 + sw / 2:.1f}" y="56" font-size="10" font-weight="700" letter-spacing="0.8" text-anchor="middle" fill="{t["accent_text"][accent]}">{esc(c["status"])}</text>')
    out.append(f'<text x="{tx}" y="100" font-size="28" font-weight="800" fill="{t["text"]}">{esc(c["title"])}</text>')
    out.append(f'<text x="{tx}" y="126" font-size="14" fill="{t["muted"]}">{esc(c["tagline"])}</text>')
    for i, pt in enumerate(c["points"]):
        y = 160 + i * 25
        out.append(f'<rect x="{tx}" y="{y - 8}" width="7" height="7" rx="2" fill="{accent}" transform="rotate(45 {tx + 3.5} {y - 4.5})"/>')
        out.append(f'<text x="{tx + 18}" y="{y}" font-size="13.5" fill="{t["text"]}">{esc(pt)}</text>')
    out.append(chips(tx, 270, p["tags"], accent, t))
    out.append("</svg>")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, default=Path("assets/cards"))
    a = ap.parse_args()
    a.output.mkdir(parents=True, exist_ok=True)
    for key in PROJECTS:
        for lang in ("zh", "en"):
            for theme in THEMES:
                (a.output / f"{key}-{lang}-{theme}.svg").write_text(card(key, lang, theme), encoding="utf-8", newline="\n")
    print("cards written to", a.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
