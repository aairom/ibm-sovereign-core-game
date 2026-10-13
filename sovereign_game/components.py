"""
components.py — Reusable HTML/CSS/Streamlit UI building blocks.

All inline CSS is scoped to short class names (``sc-*``) to avoid collisions
with Streamlit's own styles.  No external CDN fonts or icons are required —
everything falls back to system-UI defaults, keeping the app fully usable in
air-gapped environments (which is rather appropriate for the subject matter).

MIT Licence – see repository root for details.
"""

from __future__ import annotations

import math
import re
from typing import Any, Dict, List, Tuple


# ---------------------------------------------------------------------------
# Colour palette (IBM Carbon-inspired)
# ---------------------------------------------------------------------------
IBM_BLUE = "#0f62fe"
IBM_BLUE_DARK = "#0043ce"
IBM_BLUE_HOVER = "#0353e9"
IBM_CYAN = "#1192e8"
IBM_GREEN = "#198038"
IBM_GREEN_LIGHT = "#defbe6"
IBM_RED = "#da1e28"
IBM_RED_LIGHT = "#fff1f1"
IBM_ORANGE = "#ff832b"
IBM_YELLOW = "#f1c21b"
IBM_GRAY_10 = "#f4f4f4"
IBM_GRAY_20 = "#e0e0e0"
IBM_GRAY_50 = "#8d8d8d"
IBM_GRAY_70 = "#525252"
IBM_GRAY_90 = "#262626"
IBM_WHITE = "#ffffff"
SOVEREIGN_PURPLE = "#6929c4"
SOVEREIGN_TEAL = "#009d9a"


# ---------------------------------------------------------------------------
# Shared <style> block — injected once per page
# ---------------------------------------------------------------------------
def base_styles() -> str:
    """Return a ``<style>`` block with all shared CSS classes."""
    return f"""
<style>
/* ── Reset & typography ──────────────────────────────────────────────── */
:root {{
  --ibm-blue: {IBM_BLUE};
  --ibm-cyan: {IBM_CYAN};
  --ibm-green: {IBM_GREEN};
  --ibm-red: {IBM_RED};
  --ibm-orange: {IBM_ORANGE};
  --ibm-yellow: {IBM_YELLOW};
  --sovereign: {SOVEREIGN_PURPLE};
  --sovereign-teal: {SOVEREIGN_TEAL};
  --gray-10: {IBM_GRAY_10};
  --gray-20: {IBM_GRAY_20};
  --gray-50: {IBM_GRAY_50};
  --gray-70: {IBM_GRAY_70};
  --gray-90: {IBM_GRAY_90};
  --radius: 8px;
  --shadow: 0 4px 16px rgba(0,0,0,.12);
}}

/* ── Hero banner ─────────────────────────────────────────────────────── */
.sc-hero {{
  background: linear-gradient(135deg, {IBM_GRAY_90} 0%, #1a1a2e 60%, {SOVEREIGN_PURPLE}55 100%);
  border-radius: var(--radius);
  padding: 2.5rem 2rem 2rem;
  margin-bottom: 1.5rem;
  color: {IBM_WHITE};
  text-align: center;
  border: 1px solid #3a3a5c;
  box-shadow: var(--shadow);
  position: relative;
  overflow: hidden;
}}
.sc-hero::before {{
  content: '';
  position: absolute; inset: 0;
  background: repeating-linear-gradient(
    -55deg,
    transparent,
    transparent 20px,
    rgba(255,255,255,.015) 20px,
    rgba(255,255,255,.015) 40px
  );
  pointer-events: none;
}}
.sc-hero h1 {{ margin: 0 0 .4rem; font-size: 2.2rem; font-weight: 700; letter-spacing: -.5px; }}
.sc-hero .sc-sub {{ color: #a8b3cf; font-size: 1rem; margin: 0; }}
.sc-hero .sc-tag {{
  display: inline-block; margin: .25rem .2rem 0;
  padding: .15rem .6rem; border-radius: 99px;
  background: rgba(255,255,255,.1); color: {IBM_WHITE};
  font-size: .75rem; font-weight: 600; letter-spacing: .5px;
  border: 1px solid rgba(255,255,255,.2);
}}

/* ── XP & tier bar ───────────────────────────────────────────────────── */
.sc-xp-bar-wrap {{
  background: var(--gray-20); border-radius: 99px; height: 10px;
  overflow: hidden; margin: .35rem 0 .1rem;
}}
.sc-xp-bar {{
  height: 100%; border-radius: 99px;
  background: linear-gradient(90deg, {IBM_BLUE}, {SOVEREIGN_PURPLE});
  transition: width .5s ease;
}}
.sc-xp-label {{ font-size: .72rem; color: var(--gray-50); text-align: right; }}

/* ── Platform health cards ───────────────────────────────────────────── */
.sc-platform-row {{
  display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.2rem;
}}
.sc-platform-card {{
  border-radius: var(--radius); padding: 1.1rem 1.2rem 1rem;
  border: 2px solid transparent;
  box-shadow: var(--shadow);
  position: relative; overflow: hidden;
}}
.sc-platform-card.sovereign {{
  background: linear-gradient(135deg, #f0f4ff 0%, #e8e0ff 100%);
  border-color: {SOVEREIGN_PURPLE}60;
}}
.sc-platform-card.external {{
  background: linear-gradient(135deg, #fff7f0 0%, #ffe8e0 100%);
  border-color: {IBM_ORANGE}60;
}}
.sc-platform-card h3 {{ margin: 0 0 .75rem; font-size: .95rem; font-weight: 700; }}
.sc-platform-card.sovereign h3 {{ color: {SOVEREIGN_PURPLE}; }}
.sc-platform-card.external h3 {{ color: {IBM_RED}; }}

/* ── Metric rows inside platform cards ──────────────────────────────── */
.sc-metric {{ margin-bottom: .55rem; }}
.sc-metric-label {{ font-size: .72rem; color: var(--gray-70); margin-bottom: .12rem; }}
.sc-bar-outer {{
  background: var(--gray-20); border-radius: 99px; height: 8px; overflow: hidden;
}}
.sc-bar-fill {{
  height: 100%; border-radius: 99px; transition: width .6s ease;
}}
.sc-bar-fill.good {{ background: {IBM_GREEN}; }}
.sc-bar-fill.warn {{ background: {IBM_YELLOW}; }}
.sc-bar-fill.bad  {{ background: {IBM_RED}; }}
.sc-bar-fill.risk {{ background: {IBM_ORANGE}; }}
.sc-bar-fill.risk-bad {{ background: {IBM_RED}; }}
.sc-metric-val {{ font-size: .72rem; font-weight: 700; text-align: right; margin-top: .05rem; }}

/* ── Scenario card ───────────────────────────────────────────────────── */
.sc-scenario-card {{
  background: {IBM_WHITE};
  border: 2px solid var(--gray-20);
  border-radius: var(--radius);
  padding: 1.4rem 1.5rem 1.2rem;
  margin-bottom: 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,.06);
}}
.sc-scenario-card h2 {{ margin: 0 0 .5rem; font-size: 1.4rem; color: var(--gray-90); }}
.sc-scenario-tag {{
  display: inline-block; margin: 0 .3rem .5rem 0;
  padding: .15rem .55rem; border-radius: 99px;
  font-size: .7rem; font-weight: 700; letter-spacing: .4px;
  background: {IBM_BLUE}18; color: {IBM_BLUE_DARK};
  border: 1px solid {IBM_BLUE}40;
}}

/* ── Impact panels ───────────────────────────────────────────────────── */
.sc-impact-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: .75rem; margin: 1rem 0; }}
.sc-impact-panel {{
  border-radius: var(--radius); padding: 1rem 1.1rem; font-size: .85rem; line-height: 1.5;
}}
.sc-impact-panel.sov  {{ background: {IBM_GREEN_LIGHT}; border-left: 4px solid {IBM_GREEN}; }}
.sc-impact-panel.ext  {{ background: {IBM_RED_LIGHT};   border-left: 4px solid {IBM_RED}; }}
.sc-impact-panel .sc-label {{ font-weight: 700; font-size: .75rem; letter-spacing: .5px; margin-bottom: .3rem; }}
.sc-impact-panel.sov .sc-label {{ color: {IBM_GREEN}; }}
.sc-impact-panel.ext .sc-label {{ color: {IBM_RED}; }}

/* ── Answer option buttons ───────────────────────────────────────────── */
.sc-option {{
  display: block; width: 100%; text-align: left;
  padding: .85rem 1.1rem; margin-bottom: .55rem;
  border-radius: var(--radius); border: 2px solid var(--gray-20);
  background: {IBM_GRAY_10}; cursor: pointer;
  font-size: .92rem; transition: all .15s ease;
  position: relative; padding-left: 3rem;
}}
.sc-option:hover {{ background: #e8f0fe; border-color: {IBM_BLUE}70; }}
.sc-option.correct {{ background: {IBM_GREEN_LIGHT}; border-color: {IBM_GREEN}; }}
.sc-option.incorrect {{ background: {IBM_RED_LIGHT}; border-color: {IBM_RED}; }}
.sc-option.dimmed {{ opacity: .45; }}
.sc-option .sc-key {{
  position: absolute; left: .9rem; top: 50%;
  transform: translateY(-50%);
  width: 1.5rem; height: 1.5rem; border-radius: 50%;
  background: var(--gray-20); display: flex; align-items: center;
  justify-content: center; font-weight: 700; font-size: .75rem;
}}
.sc-option.correct .sc-key {{ background: {IBM_GREEN}; color: {IBM_WHITE}; }}
.sc-option.incorrect .sc-key {{ background: {IBM_RED}; color: {IBM_WHITE}; }}

/* ── Explanation panel ───────────────────────────────────────────────── */
.sc-explanation {{
  background: #f0f4ff;
  border: 2px solid {IBM_BLUE}40;
  border-radius: var(--radius);
  padding: 1.1rem 1.3rem;
  margin-top: .8rem;
  font-size: .88rem; line-height: 1.6;
}}
.sc-explanation .sc-feature {{
  margin-top: .6rem;
  padding: .4rem .8rem;
  background: {IBM_BLUE}12;
  border-radius: 4px;
  font-size: .78rem; color: {IBM_BLUE_DARK};
  font-weight: 600;
}}

/* ── Score chips ─────────────────────────────────────────────────────── */
.sc-chip {{
  display: inline-flex; align-items: center; gap: .35rem;
  padding: .25rem .75rem; border-radius: 99px;
  font-size: .8rem; font-weight: 700;
}}
.sc-chip.green {{ background: {IBM_GREEN_LIGHT}; color: {IBM_GREEN}; border: 1px solid {IBM_GREEN}60; }}
.sc-chip.red   {{ background: {IBM_RED_LIGHT}; color: {IBM_RED}; border: 1px solid {IBM_RED}60; }}
.sc-chip.blue  {{ background: #dde8ff; color: {IBM_BLUE_DARK}; border: 1px solid {IBM_BLUE}60; }}
.sc-chip.gold  {{ background: #fef3cd; color: #7d4e00; border: 1px solid {IBM_YELLOW}; }}

/* ── Scoreboard cards ────────────────────────────────────────────────── */
.sc-score-grid {{
  display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: .75rem; margin: 1rem 0;
}}
.sc-score-card {{
  background: {IBM_GRAY_10}; border-radius: var(--radius); padding: 1rem 1.1rem;
  text-align: center; border: 2px solid var(--gray-20);
}}
.sc-score-card .val {{ font-size: 2rem; font-weight: 700; line-height: 1; }}
.sc-score-card .lbl {{ font-size: .72rem; color: var(--gray-50); margin-top: .25rem; }}
.sc-score-card.highlight {{ border-color: {IBM_BLUE}; background: #dde8ff; }}
.sc-score-card.highlight .val {{ color: {IBM_BLUE_DARK}; }}

/* ── Round progress bar ──────────────────────────────────────────────── */
.sc-progress-row {{ display: flex; gap: .5rem; margin-bottom: 1.2rem; }}
.sc-progress-step {{
  flex: 1; height: 8px; border-radius: 99px;
  background: var(--gray-20); transition: background .4s ease;
}}
.sc-progress-step.done   {{ background: {IBM_GREEN}; }}
.sc-progress-step.active {{ background: {IBM_BLUE}; }}
.sc-progress-step.future {{ background: var(--gray-20); }}

/* ── Notification toasts ─────────────────────────────────────────────── */
.sc-toast {{
  padding: .8rem 1.1rem; border-radius: var(--radius); margin-bottom: .75rem;
  font-size: .88rem; font-weight: 600; display: flex; align-items: center; gap: .6rem;
}}
.sc-toast.success {{ background: {IBM_GREEN_LIGHT}; color: {IBM_GREEN}; border: 1px solid {IBM_GREEN}60; }}
.sc-toast.error   {{ background: {IBM_RED_LIGHT}; color: {IBM_RED}; border: 1px solid {IBM_RED}60; }}
.sc-toast.info    {{ background: #dde8ff; color: {IBM_BLUE_DARK}; border: 1px solid {IBM_BLUE}60; }}
.sc-toast.warn    {{ background: #fef3cd; color: #7d4e00; border: 1px solid {IBM_YELLOW}; }}

/* ── Sidebar extras ──────────────────────────────────────────────────── */
.sc-sidebar-header {{
  font-size: .75rem; font-weight: 700; letter-spacing: .8px;
  text-transform: uppercase; color: var(--gray-50); margin-bottom: .5rem;
}}

/* ── Final screen ────────────────────────────────────────────────────── */
.sc-final {{
  background: linear-gradient(135deg, {IBM_GRAY_90} 0%, {SOVEREIGN_PURPLE}50 100%);
  border-radius: var(--radius); padding: 2.5rem 2rem;
  color: {IBM_WHITE}; text-align: center;
}}
.sc-final h1 {{ font-size: 2.2rem; margin-bottom: .3rem; }}
.sc-final .sc-badge {{
  display: inline-block; margin-top: .75rem;
  padding: .4rem 1.4rem; border-radius: 99px;
  background: linear-gradient(90deg, {IBM_BLUE}, {SOVEREIGN_PURPLE});
  font-weight: 700; font-size: 1rem; letter-spacing: .3px;
}}

/* ── Animated heartbeat (pulsing status dot) ─────────────────────────── */
@keyframes sc-pulse {{
  0%, 100% {{ opacity: 1; transform: scale(1); }}
  50%       {{ opacity: .6; transform: scale(1.2); }}
}}
.sc-dot {{
  display: inline-block; width: 10px; height: 10px;
  border-radius: 50%; vertical-align: middle; margin-right: .3rem;
  animation: sc-pulse 2s infinite;
}}
.sc-dot.green  {{ background: {IBM_GREEN}; }}
.sc-dot.red    {{ background: {IBM_RED}; box-shadow: 0 0 6px {IBM_RED}; }}
.sc-dot.orange {{ background: {IBM_ORANGE}; }}

/* ── Side-by-side comparison table ──────────────────────────────────── */
.sc-compare-table {{ width: 100%; border-collapse: collapse; font-size: .85rem; margin-top: .5rem; }}
.sc-compare-table th, .sc-compare-table td {{ padding: .55rem .75rem; text-align: left; }}
.sc-compare-table th {{ font-weight: 700; font-size: .75rem; letter-spacing: .4px; }}
.sc-compare-table tr:nth-child(even) td {{ background: var(--gray-10); }}
.sc-compare-table .good {{ color: {IBM_GREEN}; font-weight: 700; }}
.sc-compare-table .bad  {{ color: {IBM_RED}; font-weight: 700; }}

/* ── Mini radar / spider chart ───────────────────────────────────────── */
.sc-radar-wrap {{ max-width: 380px; margin: 0 auto; }}

/* ── Responsive tweaks ───────────────────────────────────────────────── */
@media (max-width: 680px) {{
  .sc-platform-row {{ grid-template-columns: 1fr; }}
  .sc-impact-grid  {{ grid-template-columns: 1fr; }}
  .sc-score-grid   {{ grid-template-columns: 1fr 1fr; }}
}}
</style>
"""


# ---------------------------------------------------------------------------
# Component functions
# ---------------------------------------------------------------------------

def _bar_class(value: float, invert: bool = False) -> str:
    """Choose CSS class for a metric bar based on value."""
    if invert:
        value = 100 - value
    if value >= 70:
        return "good"
    if value >= 40:
        return "warn"
    return "bad"


def platform_health_card(
    name: str,
    uptime: float,
    compliance: float,
    ai_reliability: float,
    political_risk: float,
    card_class: str = "sovereign",
) -> str:
    """Return HTML for one platform health card."""
    metrics = [
        ("Uptime", uptime, False),
        ("Compliance", compliance, False),
        ("AI Reliability", ai_reliability, False),
        ("Political Risk", political_risk, True),
    ]
    rows = []
    text_colors = {"good": IBM_GREEN, "warn": "#b28600", "bad": IBM_RED}
    for label, val, invert in metrics:
        # For inverted metrics (political risk) a LOW value is the good state.
        cls = _bar_class(val, invert)
        display = f"{val:.0f}%"
        rows.append(f"""
<div class="sc-metric">
  <div class="sc-metric-label">{label}</div>
  <div class="sc-bar-outer">
    <div class="sc-bar-fill {cls}" style="width:{min(val,100):.1f}%"></div>
  </div>
  <div class="sc-metric-val" style="color:{text_colors[cls]}">{display}</div>
</div>""")
    rows_html = "".join(rows)
    dot_cls = "green" if (uptime + compliance + ai_reliability) / 3 >= 70 else "red"
    status = "Online" if dot_cls == "green" else "Degraded"
    return f"""
<div class="sc-platform-card {card_class}">
  <h3><span class="sc-dot {dot_cls}"></span>{name}</h3>
  <div style="font-size:.7rem;color:var(--gray-50);margin-bottom:.7rem;">
    Status: <strong>{status}</strong>
  </div>
  {rows_html}
</div>"""


def xp_progress_bar(current_xp: int, next_threshold: int, tier_name: str) -> str:
    """Return HTML XP progress bar."""
    pct = min(100, (current_xp / max(next_threshold, 1)) * 100) if next_threshold > current_xp else 100
    return f"""
<div>
  <div style="display:flex;justify-content:space-between;font-size:.75rem;margin-bottom:.2rem;">
    <span style="font-weight:700">{tier_name}</span>
    <span style="color:var(--gray-50)">{current_xp} XP</span>
  </div>
  <div class="sc-xp-bar-wrap">
    <div class="sc-xp-bar" style="width:{pct:.1f}%"></div>
  </div>
  <div class="sc-xp-label">Next tier: {next_threshold} XP</div>
</div>"""


def round_progress_bar(current_round: int, max_rounds: int) -> str:
    """Return HTML step-indicator for round progress."""
    steps = []
    for i in range(1, max_rounds + 1):
        if i < current_round:
            cls = "done"
        elif i == current_round:
            cls = "active"
        else:
            cls = "future"
        steps.append(f'<div class="sc-progress-step {cls}"></div>')
    return f'<div class="sc-progress-row">{"".join(steps)}</div>'


def scenario_header(title: str, tags: List[str], round_num: int, max_rounds: int) -> str:
    """Return HTML for the scenario card header."""
    tag_html = " ".join(f'<span class="sc-scenario-tag">{t}</span>' for t in tags)
    return f"""
<div class="sc-scenario-card">
  <div style="font-size:.72rem;color:var(--gray-50);margin-bottom:.3rem;font-weight:700;">
    ROUND {round_num} / {max_rounds}
  </div>
  <h2>{title}</h2>
  <div>{tag_html}</div>
</div>"""


def impact_grid(sovereign_text: str, external_text: str) -> str:
    """Return HTML for the two-column impact panel."""
    return f"""
<div class="sc-impact-grid">
  <div class="sc-impact-panel sov">
    <div class="sc-label">🔵 IBM SOVEREIGN CORE</div>
    {sovereign_text}
  </div>
  <div class="sc-impact-panel ext">
    <div class="sc-label">🔴 PUBLIC CLOUD AI</div>
    {external_text}
  </div>
</div>"""


def inline_md(text: str) -> str:
    """Convert ``**bold**`` markers to ``<strong>`` tags.

    Streamlit does not parse Markdown inside raw HTML blocks, so text that is
    embedded in our HTML builders must be converted explicitly.
    """
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)


def explanation_box(text: str, feature: str) -> str:
    """Return HTML for the post-answer explanation panel."""
    return f"""
<div class="sc-explanation">
  <strong>💡 Why this matters:</strong><br>{inline_md(text)}
  <div class="sc-feature">🛡️ IBM Sovereign Core Feature: {feature}</div>
</div>"""


def toast(message: str, kind: str = "info") -> str:
    """Return HTML for a notification toast (info | success | error | warn)."""
    icons = {"info": "ℹ️", "success": "✅", "error": "🔴", "warn": "⚠️"}
    icon = icons.get(kind, "ℹ️")
    return f'<div class="sc-toast {kind}">{icon} {inline_md(message)}</div>'


def score_grid(items: List[Tuple[str, Any, bool]]) -> str:
    """
    Return HTML for a row of score cards.

    Parameters
    ----------
    items : list of (label, value, highlight)
    """
    cards = []
    for label, val, highlight in items:
        cls = "highlight" if highlight else ""
        cards.append(f"""
<div class="sc-score-card {cls}">
  <div class="val">{val}</div>
  <div class="lbl">{label}</div>
</div>""")
    return f'<div class="sc-score-grid">{"".join(cards)}</div>'


def comparison_table(rows: List[Dict[str, str]]) -> str:
    """
    Return HTML for the sovereign vs external comparison table.

    Each row dict: {{"feature": str, "sovereign": str, "external": str}}.
    """
    header = """
<tr style="background:var(--gray-10);">
  <th>Capability</th>
  <th style="color:#6929c4">IBM Sovereign Core</th>
  <th style="color:#da1e28">Public Cloud AI</th>
</tr>"""
    trs = []
    for row in rows:
        trs.append(f"""
<tr>
  <td><strong>{row['feature']}</strong></td>
  <td class="good">{row['sovereign']}</td>
  <td class="bad">{row['external']}</td>
</tr>""")
    return f'<table class="sc-compare-table">{header}{"".join(trs)}</table>'


def radar_chart_svg(
    labels: List[str],
    sovereign_values: List[float],
    external_values: List[float],
    size: int = 280,
) -> str:
    """
    Generate an inline SVG spider/radar chart comparing two data series.

    Values should be in [0, 100].
    """
    n = len(labels)
    if n < 3:
        return ""
    cx, cy = size // 2, size // 2
    r = (size // 2) - 50  # radius leaving room for labels

    def point(angle_deg: float, value: float) -> Tuple[float, float]:
        angle_rad = math.radians(angle_deg - 90)
        scaled = (value / 100.0) * r
        return cx + scaled * math.cos(angle_rad), cy + scaled * math.sin(angle_rad)

    angles = [i * (360 / n) for i in range(n)]

    # --- grid rings
    rings = []
    for pct in (0.25, 0.5, 0.75, 1.0):
        pts = " ".join(
            f"{cx + pct*r*math.cos(math.radians(a-90)):.1f},"
            f"{cy + pct*r*math.sin(math.radians(a-90)):.1f}"
            for a in angles
        )
        rings.append(
            f'<polygon points="{pts}" fill="none" stroke="#e0e0e0" stroke-width="1"/>'
        )

    # --- axis lines
    axes = []
    for a in angles:
        ex = cx + r * math.cos(math.radians(a - 90))
        ey = cy + r * math.sin(math.radians(a - 90))
        axes.append(f'<line x1="{cx}" y1="{cy}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="#e0e0e0" stroke-width="1"/>')

    # --- data polygons
    def series_poly(values: List[float], color: str, opacity: str) -> str:
        pts = " ".join(
            f"{point(a, v)[0]:.1f},{point(a, v)[1]:.1f}"
            for a, v in zip(angles, values)
        )
        return (
            f'<polygon points="{pts}" fill="{color}" fill-opacity="{opacity}" '
            f'stroke="{color}" stroke-width="2.5" stroke-linejoin="round"/>'
        )

    sov_poly = series_poly(sovereign_values, SOVEREIGN_PURPLE, "0.25")
    ext_poly = series_poly(external_values, IBM_RED, "0.18")

    # --- dot markers
    def dots(values: List[float], color: str) -> str:
        return "".join(
            f'<circle cx="{point(a, v)[0]:.1f}" cy="{point(a, v)[1]:.1f}" r="5" fill="{color}"/>'
            for a, v in zip(angles, values)
        )

    sov_dots = dots(sovereign_values, SOVEREIGN_PURPLE)
    ext_dots = dots(external_values, IBM_RED)

    # --- labels
    label_elems = []
    for i, (a, lbl) in enumerate(zip(angles, labels)):
        lx = cx + (r + 28) * math.cos(math.radians(a - 90))
        ly = cy + (r + 28) * math.sin(math.radians(a - 90))
        anchor = "middle"
        if lx < cx - 5:
            anchor = "end"
        elif lx > cx + 5:
            anchor = "start"
        label_elems.append(
            f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" '
            f'dominant-baseline="middle" font-size="11" fill="#525252" font-weight="600">{lbl}</text>'
        )

    # --- legend
    legend = (
        f'<rect x="10" y="{size-30}" width="12" height="12" fill="{SOVEREIGN_PURPLE}" fill-opacity=".6" rx="2"/>'
        f'<text x="26" y="{size-22}" font-size="10" fill="#262626">IBM Sovereign Core</text>'
        f'<rect x="{size//2+10}" y="{size-30}" width="12" height="12" fill="{IBM_RED}" fill-opacity=".5" rx="2"/>'
        f'<text x="{size//2+26}" y="{size-22}" font-size="10" fill="#262626">Public Cloud AI</text>'
    )

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 {size} {size}" style="max-width:100%;height:auto;">'
        + "".join(rings)
        + "".join(axes)
        + sov_poly + ext_poly
        + sov_dots + ext_dots
        + "".join(label_elems)
        + legend
        + "</svg>"
    )


COMPARISON_ROWS = [
    {
        "feature": "Political / vendor kill switch",
        "sovereign": "✅ Immune — air-gapped, customer-controlled",
        "external": "❌ Single executive decision shuts it down",
    },
    {
        "feature": "Compliance evidence",
        "sovereign": "✅ 233 frameworks, auto-generated, continuous",
        "external": "❌ Manual, slow, incomplete",
    },
    {
        "feature": "Data residency proof",
        "sovereign": "✅ In-boundary, metered, auditable",
        "external": "❌ Vendor black box, no operator visibility",
    },
    {
        "feature": "Infrastructure flexibility",
        "sovereign": "✅ Any CPU/GPU/hardware on your site",
        "external": "❌ Provider quota limits, distant regions",
    },
    {
        "feature": "New regulation readiness",
        "sovereign": "✅ Governed catalog — add in hours",
        "external": "❌ Depends on vendor roadmap (months)",
    },
    {
        "feature": "Time to operational sovereignty",
        "sovereign": "✅ 1 day with Sovereign from the Start",
        "external": "❌ Months of integration & validation",
    },
]
