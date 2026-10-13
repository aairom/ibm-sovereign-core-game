"""
lab.py — "Kill Switch Lab" Streamlit page.

Users can trigger a live AI-request simulation that compares IBM Sovereign
Core against a public-cloud AI service in real time.  Controls simulate two
real-world crisis events:
  * Political embargo — the foreign API provider suspends access.
  * Cross-border data ban — the regulator bans data leaving the national boundary.

MIT Licence – see repository root for details.
"""

from __future__ import annotations

import time

import streamlit as st

from sovereign_game.components import (
    IBM_GREEN,
    IBM_RED,
    IBM_YELLOW,
    SOVEREIGN_PURPLE,
    toast,
)
from sovereign_game.config import load_config
from sovereign_game.simulation import LabState, availability, compliance_rate, reset, step

cfg = load_config()


def init_lab() -> LabState:
    if "lab" not in st.session_state:
        st.session_state["lab"] = LabState()
    return st.session_state["lab"]


def _metric_card(title: str, value: str, delta_text: str, color: str) -> str:
    return f"""
<div style="background:#f4f4f4;border:2px solid {color}30;border-radius:8px;padding:1rem;text-align:center;">
  <div style="font-size:.75rem;font-weight:700;color:#525252;margin-bottom:.2rem;text-transform:uppercase;">{title}</div>
  <div style="font-size:1.9rem;font-weight:700;color:{color}">{value}</div>
  <div style="font-size:.7rem;color:#8d8d8d;margin-top:.15rem">{delta_text}</div>
</div>"""


def render_lab() -> None:
    """Render the Kill Switch Lab page."""
    lab = init_lab()

    st.markdown(
        """
<div style="background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);border-radius:8px;
            padding:1.5rem;color:#fff;margin-bottom:1.2rem;border:1px solid #3a3a5c;">
  <h2 style="margin:0 0 .3rem;font-size:1.5rem">🧪 Kill Switch Lab</h2>
  <p style="color:#a8b3cf;margin:0;font-size:.9rem">
    Interactive simulation: two platforms, live AI traffic, real-world crises.
    Trigger the controls below and watch the metrics diverge.
  </p>
</div>""",
        unsafe_allow_html=True,
    )

    # ── Controls ────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])

    with col1:
        if lab.running:
            if st.button("⏹ Stop Simulation", use_container_width=True):
                lab.running = False
                st.rerun()
        else:
            if st.button("▶ Start Simulation", use_container_width=True, type="primary"):
                lab.running = True
                st.rerun()

    with col2:
        embargo_label = "🔴 Embargo ON" if lab.embargo else "⚡ Trigger Embargo"
        if st.button(embargo_label, use_container_width=True, disabled=not lab.running):
            lab.embargo = not lab.embargo

    with col3:
        ban_label = "🟠 Data Ban ON" if lab.cross_border_ban else "📜 Trigger Data Ban"
        if st.button(ban_label, use_container_width=True, disabled=not lab.running):
            lab.cross_border_ban = not lab.cross_border_ban

    with col4:
        if st.button("🔄 Reset", use_container_width=True):
            reset(lab)
            st.rerun()

    # ── Status banners ───────────────────────────────────────────────────
    if lab.embargo:
        st.markdown(
            toast("🔴 EMBARGO ACTIVE — Public cloud AI is cut off. IBM Sovereign Core unaffected.", "error"),
            unsafe_allow_html=True,
        )
    if lab.cross_border_ban:
        st.markdown(
            toast("🟠 DATA BAN ACTIVE — Cross-border AI requests now violate regulations.", "warn"),
            unsafe_allow_html=True,
        )

    # ── Tick the simulation ──────────────────────────────────────────────
    if lab.running:
        step(lab, cfg.sim_requests_per_tick)

    # ── Metrics ──────────────────────────────────────────────────────────
    ext_avail = availability(lab.ext_served, lab.ext_failed)
    ext_comp = compliance_rate(lab.ext_served, lab.ext_violations)

    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
    with mcol1:
        st.markdown(
            _metric_card("Sovereign Served", f"{lab.sov_served:,}", "100% in-boundary", SOVEREIGN_PURPLE),
            unsafe_allow_html=True,
        )
    with mcol2:
        ext_avail_color = IBM_GREEN if ext_avail > 90 else IBM_YELLOW if ext_avail > 50 else IBM_RED
        st.markdown(
            _metric_card("Cloud Served", f"{lab.ext_served:,}", f"{ext_avail:.0f}% availability", ext_avail_color),
            unsafe_allow_html=True,
        )
    with mcol3:
        ext_fail_color = IBM_GREEN if lab.ext_failed == 0 else IBM_RED
        st.markdown(
            _metric_card("Cloud Failed", f"{lab.ext_failed:,}", "embargo-dropped", ext_fail_color),
            unsafe_allow_html=True,
        )
    with mcol4:
        comp_color = IBM_GREEN if ext_comp >= 99 else IBM_YELLOW if ext_comp >= 70 else IBM_RED
        st.markdown(
            _metric_card("Cloud Compliance", f"{ext_comp:.0f}%", f"{lab.ext_violations:,} violations", comp_color),
            unsafe_allow_html=True,
        )

    # ── Throughput chart using Streamlit native ──────────────────────────
    if len(lab.history) > 1:
        import pandas as pd

        df = pd.DataFrame(lab.history, columns=["Tick", "IBM Sovereign Core", "Public Cloud AI"])
        df = df.set_index("Tick")
        st.markdown("#### AI Requests Served (cumulative)")
        st.line_chart(df, color=[f"#{SOVEREIGN_PURPLE[1:]}", f"#{IBM_RED[1:]}"])

    # ── Explanation ───────────────────────────────────────────────────────
    with st.expander("💡 Why does IBM Sovereign Core stay green?", expanded=False):
        st.markdown(
            """
The IBM Sovereign Core architecture places the entire AI stack — models, inference
service, data, and the control plane — **inside the customer's own boundary** (a
private data-centre, on-premise rack, or sovereign cloud region).

There is **no runtime dependency** on any IBM endpoint, any foreign government's network,
or any public hyperscaler API. This means:

| Crisis | Public Cloud AI | IBM Sovereign Core |
|---|---|---|
| Political embargo | ❌ API blocked | ✅ No external API needed |
| Cross-border data ban | ❌ Every request is a violation | ✅ Data never leaves the boundary |
| Vendor price hike | ❌ Pay or lose service | ✅ You own the stack |

> *"Enterprises don't need another cloud. Enterprises need sovereignty and control they can prove."*  
> — IBM Sovereign Core (2026)
"""
        )

    # ── Auto-rerun while running ─────────────────────────────────────────
    if lab.running:
        time.sleep(0.8)
        st.rerun()
