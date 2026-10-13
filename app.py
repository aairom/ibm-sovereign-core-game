"""
app.py — Sovereign AI Challenge: Main Streamlit application.

A five-round gamified demonstration contrasting IBM Sovereign Core
(air-gapped, customer-operated AI platform) against a generic public-cloud
AI service across realistic crisis scenarios drawn from the IBM Sovereign Core
product documentation and presentation decks (2026).

Run with:
    streamlit run app.py

MIT Licence – see repository root for details.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import streamlit as st

# ── Local modules ──────────────────────────────────────────────────────────
from sovereign_game.game_state import (
    MAX_ROUNDS_DEFAULT,
    GameState,
    init_state,
    reset_state,
)
from sovereign_game.scenarios import SCENARIOS
from sovereign_game.components import (
    base_styles,
    comparison_table,
    COMPARISON_ROWS,
    explanation_box,
    impact_grid,
    platform_health_card,
    radar_chart_svg,
    round_progress_bar,
    scenario_header,
    score_grid,
    toast,
    xp_progress_bar,
    IBM_GREEN,
    IBM_RED,
)
from sovereign_game.config import load_config

MAX_ROUNDS = MAX_ROUNDS_DEFAULT

# ---------------------------------------------------------------------------
# Page configuration — must be the very first Streamlit call
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title=load_config().app_title,
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://www.ibm.com/docs/en/sovereign-core/1.2.0",
        "Report a bug": None,
        "About": (
            "**Sovereign AI Challenge** — An interactive demonstration of IBM Sovereign Core.\n\n"
            "Source: IBM Sovereign Core documentation & presentation decks (2026).\n"
            "© 2026 IBM Corporation. Demonstration purposes only."
        ),
    },
)

# ---------------------------------------------------------------------------
# Config & state
# ---------------------------------------------------------------------------
cfg = load_config()
gs: GameState = init_state()

# ---------------------------------------------------------------------------
# Global styles
# ---------------------------------------------------------------------------
st.markdown(base_styles(), unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

def _health_gauge(name: str, health: float, color: str) -> None:
    """Compact progress bar in sidebar for a platform's overall health."""
    pct = max(0.0, min(100.0, health))
    st.markdown(
        f"""
<div style="margin-bottom:.6rem;">
  <div style="display:flex;justify-content:space-between;font-size:.72rem;margin-bottom:.15rem;">
    <span>{name}</span><span style="font-weight:700;color:{color}">{pct:.0f}%</span>
  </div>
  <div style="background:#e0e0e0;border-radius:99px;height:6px;">
    <div style="width:{pct:.1f}%;background:{color};border-radius:99px;height:100%;
                transition:width .5s;"></div>
  </div>
</div>""",
        unsafe_allow_html=True,
    )


def _sidebar() -> None:
    with st.sidebar:
        st.markdown(
            '<div class="sc-sidebar-header">🛡️ Sovereign AI Challenge</div>',
            unsafe_allow_html=True,
        )
        st.markdown("---")

        # --- XP bar ---
        st.markdown(xp_progress_bar(gs.xp, gs.next_tier_xp, gs.tier), unsafe_allow_html=True)
        st.markdown("")

        # --- Platform health ---
        st.markdown(
            '<div class="sc-sidebar-header">Platform Status</div>',
            unsafe_allow_html=True,
        )
        sov_health = gs.sovereign.overall_health
        ext_health = gs.external.overall_health
        _health_gauge("IBM Sovereign Core", sov_health, IBM_GREEN if sov_health >= 70 else IBM_RED)
        _health_gauge("Public Cloud AI", ext_health, IBM_RED if ext_health < 70 else "#f1c21b")

        st.markdown("---")

        if st.button("🔄 Restart Game", use_container_width=True):
            reset_state()
            st.rerun()

        st.markdown("---")

        with st.expander("📖 IBM Sovereign Core", expanded=False):
            st.markdown(
                """
**Key capabilities:**
- 🚀 Sovereign from the Start — operational in **1 day**
- 📋 **233** embedded compliance frameworks
- 🤖 AI Within Your Control — CPU & GPU inferencing
- 🔒 Customer-operated control plane
- 🗂️ Governed extensible catalog
- 🏗️ Hardware optionality via OpenShift

[Documentation ↗](https://www.ibm.com/docs/en/sovereign-core/1.2.0)
"""
            )

        if cfg.show_disclaimer:
            st.caption(
                "Demonstration purposes only. Metrics are illustrative. "
                "© 2026 IBM Corporation."
            )


# ---------------------------------------------------------------------------
# Screen: Welcome
# ---------------------------------------------------------------------------

def _screen_welcome() -> None:
    st.markdown(
        """
<div class="sc-hero">
  <div style="font-size:3.5rem;margin-bottom:.5rem">🛡️</div>
  <h1>Sovereign AI Challenge</h1>
  <p class="sc-sub">
    Five crisis scenarios. Two platforms. One winner.<br>
    Can IBM Sovereign Core keep your AI running when the world turns upside down?
  </p>
  <span class="sc-tag">Data Sovereignty</span>
  <span class="sc-tag">Operational Continuity</span>
  <span class="sc-tag">Regulatory Compliance</span>
  <span class="sc-tag">AI Governance</span>
</div>
""",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("### What is this game?")
        st.markdown(
            """
You are the **Chief Digital Officer** of an enterprise running AI on **two platforms at once**:

| Platform | Description |
|---|---|
| 🔵 **IBM Sovereign Core** | Air-gapped, customer-operated. Runs on *your* hardware, under *your* control, deployable in **1 day**. |
| 🔴 **Public Cloud AI** | Hyperscaler-hosted. Fast to start, but dependent on vendor goodwill and geopolitics. |

Each round a real-world crisis strikes. Choose the correct response — and learn *why* IBM Sovereign
Core is immune — to score XP and climb the tier ladder.

**5 rounds · 5 crises · 1 key lesson per round.**
"""
        )
        st.markdown("### Why sovereignty matters")
        st.markdown(
            """
> *58 % of IT leaders experienced business disruption in 2025 due to technology supply-chain choke points.*  
> *35 % of enterprises will face regulatory scrutiny by 2027 for inadequate AI risk management.*  
> — IBM Institute for Business Value, 2026

By 2030, **75 % of enterprises** will have a digital sovereignty strategy.  
IBM Sovereign Core is the platform that makes that strategy actionable — on day one.
"""
        )

    with col2:
        st.markdown("### Platform comparison")
        st.markdown(comparison_table(COMPARISON_ROWS[:4]), unsafe_allow_html=True)

    st.markdown("---")
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        if st.button("🚀  Start the Challenge", use_container_width=True, type="primary"):
            gs.start_round(1)
            st.rerun()


# ---------------------------------------------------------------------------
# Screen: Round
# ---------------------------------------------------------------------------

def _screen_round(scenario_idx: int) -> None:
    scenario = SCENARIOS[scenario_idx]

    # Apply disruptions exactly once
    gs.apply_scenario_disruption(scenario_idx, scenario["disruption"])

    # ── Round progress bar ───────────────────────────────────────────────
    st.markdown(
        round_progress_bar(gs.round_number, MAX_ROUNDS),
        unsafe_allow_html=True,
    )

    # ── Platform health cards ────────────────────────────────────────────
    st.markdown(
        f"""
<div class="sc-platform-row">
  {platform_health_card(
      "IBM Sovereign Core",
      gs.sovereign.uptime,
      gs.sovereign.compliance_score,
      gs.sovereign.ai_reliability,
      gs.sovereign.political_risk,
      "sovereign",
  )}
  {platform_health_card(
      "Public Cloud AI",
      gs.external.uptime,
      gs.external.compliance_score,
      gs.external.ai_reliability,
      gs.external.political_risk,
      "external",
  )}
</div>
""",
        unsafe_allow_html=True,
    )

    # ── Scenario header ──────────────────────────────────────────────────
    st.markdown(
        scenario_header(scenario["title"], scenario["tags"], gs.round_number, MAX_ROUNDS),
        unsafe_allow_html=True,
    )

    # ── Narrative ────────────────────────────────────────────────────────
    st.markdown(scenario["narrative"])

    # ── Impact grid ──────────────────────────────────────────────────────
    st.markdown(
        impact_grid(scenario["sovereign_impact"], scenario["external_impact"]),
        unsafe_allow_html=True,
    )

    # ── Question ─────────────────────────────────────────────────────────
    st.markdown(f"**❓ {scenario['question']}**")

    if gs.is_answered(scenario_idx):
        _show_answered_options(scenario, scenario_idx)
        _show_result_panel(scenario, scenario_idx)
        _nav_buttons(scenario_idx)
    else:
        _show_unanswered_options(scenario, scenario_idx)


def _show_unanswered_options(scenario: dict, idx: int) -> None:
    """Render clickable answer buttons before the player has answered."""
    elapsed = gs.elapsed_seconds()
    time_color = IBM_GREEN if elapsed <= 10 else ("#f1c21b" if elapsed <= 20 else IBM_RED)
    speed_hint = "  ⚡ Speed bonus available!" if elapsed <= cfg.speed_bonus_seconds else ""
    st.markdown(
        f'<div style="text-align:right;font-size:.75rem;color:{time_color};font-weight:700;'
        f'margin-bottom:.3rem;">⏱ {elapsed:.0f}s elapsed{speed_hint}</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(2)
    for i, (key, text) in enumerate(scenario["options"].items()):
        with cols[i % 2]:
            if st.button(
                f"**{key.upper()}.** {text}",
                key=f"opt_{idx}_{key}",
                use_container_width=True,
            ):
                gs.record_answer(scenario_index=idx, scenario=scenario, chosen=key, cfg=cfg)
                st.rerun()


def _show_answered_options(scenario: dict, idx: int) -> None:
    """Render options with correct/incorrect styling after answering."""
    result = gs.results.get(idx)
    chosen = result.chosen if result else None
    correct_key = scenario["correct"]

    parts = []
    for key, text in scenario["options"].items():
        if key == correct_key:
            cls, icon = "correct", "✅"
        elif key == chosen and key != correct_key:
            cls, icon = "incorrect", "❌"
        else:
            cls, icon = "dimmed", "·"
        parts.append(
            f'<div class="sc-option {cls}">'
            f'<span class="sc-key">{key.upper()}</span>'
            f"{icon} {text}</div>"
        )
    st.markdown("".join(parts), unsafe_allow_html=True)


def _show_result_panel(scenario: dict, idx: int) -> None:
    """Post-answer feedback: XP + explanation."""
    result = gs.results.get(idx)
    if result is None:
        return
    st.markdown("---")
    if result.correct:
        speed_note = " ⚡ Speed bonus included!" if result.seconds <= cfg.speed_bonus_seconds else ""
        st.markdown(
            toast(f"Correct! +{result.xp_earned} XP{speed_note}  |  Total: {gs.xp} XP", "success"),
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            toast(
                f"Not quite. The right answer was **{scenario['correct'].upper()}**. "
                "See the explanation below.",
                "error",
            ),
            unsafe_allow_html=True,
        )

    st.markdown(
        explanation_box(scenario["explanation"], scenario["ibm_feature"]),
        unsafe_allow_html=True,
    )


def _nav_buttons(scenario_idx: int) -> None:
    st.markdown("")
    col_l, col_r = st.columns([1, 3])
    with col_l:
        if scenario_idx > 0:
            if st.button("← Previous", key=f"prev_{scenario_idx}"):
                gs.start_round(scenario_idx)  # back = round == idx (1-based)
                st.rerun()
    with col_r:
        if scenario_idx < MAX_ROUNDS - 1:
            if st.button(
                "Next Round →",
                key=f"next_{scenario_idx}",
                type="primary",
                use_container_width=True,
            ):
                gs.start_round(scenario_idx + 2)  # 1-based
                st.rerun()
        else:
            if st.button(
                "🏁 View Final Results",
                key="finish",
                type="primary",
                use_container_width=True,
            ):
                gs.finish_game()
                st.rerun()


# ---------------------------------------------------------------------------
# Screen: Final Results
# ---------------------------------------------------------------------------

def _screen_final() -> None:
    correct = gs.correct_count
    total = MAX_ROUNDS
    pct = int(correct / total * 100)

    tier_emojis = ["🌱", "🔍", "🏗️", "🛡️", "👑"]
    tier_emoji = tier_emojis[min(gs.tier_index, len(tier_emojis) - 1)]

    st.markdown(
        f"""
<div class="sc-final">
  <div style="font-size:3rem">{tier_emoji}</div>
  <h1>Challenge Complete!</h1>
  <p style="color:#a8b3cf;font-size:1rem;margin:.3rem 0 .7rem;">
    You scored <strong>{correct}/{total}</strong> correct answers and earned <strong>{gs.xp} XP</strong>.
  </p>
  <div class="sc-badge">{gs.tier}</div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("")

    sov_h = f"{gs.sovereign.overall_health:.0f}%"
    ext_h = f"{gs.external.overall_health:.0f}%"
    st.markdown(
        score_grid([
            ("XP Earned", gs.xp, True),
            ("Correct Answers", f"{correct}/{total}", False),
            ("Accuracy", f"{pct}%", False),
            ("Sovereign Health", sov_h, False),
            ("Cloud Health", ext_h, False),
            ("Tier Achieved", gs.tier, False),
        ]),
        unsafe_allow_html=True,
    )

    tab_radar, tab_compare, tab_log = st.tabs(
        ["📊 Platform Radar", "⚖️ Full Comparison", "📋 Round Log"]
    )

    with tab_radar:
        st.markdown("### Platform Capability Radar")
        st.markdown(
            "After five crises, here is how each platform fared across the five key "
            "sovereignty dimensions:"
        )
        sov = gs.sovereign
        ext = gs.external
        labels = ["Uptime", "Compliance", "AI Reliability", "Data Control", "Reg. Agility"]
        sov_vals = [
            sov.uptime,
            sov.compliance_score,
            sov.ai_reliability,
            max(0.0, 100.0 - sov.political_risk),
            min(100.0, sov.compliance_score + 8.0),
        ]
        ext_vals = [
            ext.uptime,
            ext.compliance_score,
            ext.ai_reliability,
            max(0.0, 100.0 - ext.political_risk),
            max(0.0, ext.compliance_score - 8.0),
        ]

        _, col2, _ = st.columns([1, 2, 1])
        with col2:
            svg = radar_chart_svg(labels, sov_vals, ext_vals, size=340)
            st.markdown(
                f'<div class="sc-radar-wrap" style="text-align:center">{svg}</div>',
                unsafe_allow_html=True,
            )

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(
                platform_health_card(
                    "IBM Sovereign Core",
                    sov.uptime, sov.compliance_score, sov.ai_reliability, sov.political_risk,
                    "sovereign",
                ),
                unsafe_allow_html=True,
            )
        with col_b:
            st.markdown(
                platform_health_card(
                    "Public Cloud AI",
                    ext.uptime, ext.compliance_score, ext.ai_reliability, ext.political_risk,
                    "external",
                ),
                unsafe_allow_html=True,
            )

    with tab_compare:
        st.markdown("### Full Platform Comparison")
        st.markdown(comparison_table(COMPARISON_ROWS), unsafe_allow_html=True)
        st.markdown("---")
        st.markdown(
            """
#### The IBM Sovereign Core Advantage

| Dimension | IBM Sovereign Core | Typical Public Cloud AI |
|---|---|---|
| Time to sovereignty | **1 day** | Months |
| Compliance frameworks | **233 embedded** | Manual / none |
| Infrastructure dependency | **None — your hardware** | 100 % vendor |
| AI model control | **Full — deploy any model** | Vendor-approved only |
| Regulatory evidence | **Continuous, automated** | Periodic, manual |
| Political risk | **Immune** | High |

> *By 2030, 75 % of enterprises will have a digital sovereignty strategy.* — Gartner, 2025
"""
        )

    with tab_log:
        st.markdown("### Round-by-Round Log")
        if not gs.results:
            st.info("No rounds completed this session.")
        else:
            for idx in sorted(gs.results):
                r = gs.results[idx]
                icon = "✅" if r.correct else "❌"
                speed = f"  ⚡ {r.seconds:.1f}s" if r.correct and r.seconds <= cfg.speed_bonus_seconds else f"  ⏱ {r.seconds:.1f}s"
                st.markdown(
                    f"**Round {r.round_number}** — {r.title}  "
                    f"{icon} Chose **{r.chosen.upper()}**{speed}  ·  +{r.xp_earned} XP"
                )

        st.markdown("---")
        if st.button("💾 Export Results (JSON)"):
            out_dir = Path(cfg.output_dir)
            out_dir.mkdir(exist_ok=True)
            fname = out_dir / f"results_{int(time.time())}.json"
            with open(fname, "w") as fh:
                json.dump(gs.summary(), fh, indent=2)
            st.success(f"Results saved to `{fname}`")

    st.markdown("---")
    _, col_mid, _ = st.columns([1, 2, 1])
    with col_mid:
        if st.button("🔄 Play Again", use_container_width=True, type="primary"):
            reset_state()
            st.rerun()

    st.caption(
        "IBM Sovereign Core — A sovereign, AI-ready platform with full operational control "
        "on any infrastructure. © 2026 IBM Corporation. Demonstration purposes only."
    )


# ---------------------------------------------------------------------------
# Main router
# ---------------------------------------------------------------------------

def main() -> None:
    # Apply the current round's disruption *before* the sidebar renders so the
    # sidebar gauges and the main panel always show the same numbers.
    if 1 <= gs.round_number <= len(SCENARIOS) and not gs.game_over:
        idx = gs.round_number - 1
        gs.apply_scenario_disruption(idx, SCENARIOS[idx]["disruption"])

    _sidebar()

    if gs.round_number == 0 and not gs.game_over:
        _screen_welcome()
    elif gs.game_over or gs.round_number > MAX_ROUNDS:
        _screen_final()
    else:
        scenario_idx = gs.round_number - 1  # 1-based → 0-based
        if scenario_idx >= len(SCENARIOS):
            gs.finish_game()
            st.rerun()
        else:
            _screen_round(scenario_idx)


if __name__ == "__main__":
    main()
