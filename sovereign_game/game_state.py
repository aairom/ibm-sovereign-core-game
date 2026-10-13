"""
game_state.py — Pure game logic and session-state helpers.

The dataclasses here contain no Streamlit code so they can be unit tested
directly. Only the three helper functions at the bottom touch
``st.session_state``.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from sovereign_game.config import Config

MAX_ROUNDS_DEFAULT = 5

TIER_LABELS = ["Observer", "Analyst", "Architect", "Sovereign Guardian", "Master of Sovereignty"]
TIER_THRESHOLDS = [0, 200, 500, 800, 1100]


def _clamp(value: float) -> float:
    """Clamp *value* to the 0-100 range."""
    return max(0.0, min(100.0, value))


@dataclass
class PlatformHealth:
    """Live health metrics (0-100) for one platform."""

    name: str
    uptime: float = 100.0
    compliance_score: float = 100.0
    ai_reliability: float = 100.0
    political_risk: float = 0.0  # higher is worse

    def apply_disruption(
        self,
        uptime_loss: float = 0.0,
        compliance_loss: float = 0.0,
        ai_loss: float = 0.0,
        risk_gain: float = 0.0,
    ) -> None:
        """Lower health metrics after a crisis event."""
        self.uptime = _clamp(self.uptime - uptime_loss)
        self.compliance_score = _clamp(self.compliance_score - compliance_loss)
        self.ai_reliability = _clamp(self.ai_reliability - ai_loss)
        self.political_risk = _clamp(self.political_risk + risk_gain)

    @property
    def overall_health(self) -> float:
        """Average of uptime, compliance and AI reliability."""
        return (self.uptime + self.compliance_score + self.ai_reliability) / 3.0


@dataclass
class RoundResult:
    """Outcome of one answered round."""

    round_number: int
    scenario_id: str
    title: str
    chosen: str
    correct: bool
    xp_earned: int
    seconds: float


@dataclass
class GameState:
    """Full game session state."""

    xp: int = 0
    round_number: int = 0  # 0 = welcome screen, 1..max_rounds = playing
    max_rounds: int = MAX_ROUNDS_DEFAULT
    results: Dict[int, RoundResult] = field(default_factory=dict)  # keyed by scenario index
    sovereign: PlatformHealth = field(default_factory=lambda: PlatformHealth("IBM Sovereign Core"))
    external: PlatformHealth = field(
        default_factory=lambda: PlatformHealth(
            "Public Cloud AI", compliance_score=70.0, ai_reliability=85.0, political_risk=35.0
        )
    )
    game_over: bool = False
    round_start: float = field(default_factory=time.time)
    disruptions_applied: List[int] = field(default_factory=list)  # scenario indices

    # ---- tiers -----------------------------------------------------------
    @property
    def tier_index(self) -> int:
        level = 0
        for i, threshold in enumerate(TIER_THRESHOLDS):
            if self.xp >= threshold:
                level = i
        return level

    @property
    def tier(self) -> str:
        return TIER_LABELS[self.tier_index]

    @property
    def next_tier_xp(self) -> int:
        """XP needed for the next tier (current XP if already at the top)."""
        idx = self.tier_index
        return TIER_THRESHOLDS[idx + 1] if idx + 1 < len(TIER_THRESHOLDS) else self.xp

    # ---- round lifecycle -------------------------------------------------
    def start_round(self, round_number: int) -> None:
        """Move to *round_number* (1-based) and restart the round timer."""
        self.round_number = round_number
        self.round_start = time.time()

    def elapsed_seconds(self) -> float:
        return time.time() - self.round_start

    def is_answered(self, scenario_index: int) -> bool:
        return scenario_index in self.results

    def apply_scenario_disruption(self, scenario_index: int, disruption: dict) -> None:
        """Apply a scenario's metric changes exactly once."""
        if scenario_index in self.disruptions_applied:
            return
        self.sovereign.apply_disruption(**disruption["sovereign"])
        self.external.apply_disruption(**disruption["external"])
        self.disruptions_applied.append(scenario_index)

    def record_answer(
        self,
        scenario_index: int,
        scenario: dict,
        chosen: str,
        cfg: Config,
        now: Optional[float] = None,
    ) -> RoundResult:
        """
        Score an answer. Ignored (existing result returned) if already answered.

        A correct answer earns ``cfg.base_xp`` plus a speed bonus when answered
        within ``cfg.speed_bonus_seconds``. A wrong answer opens a "sovereignty
        gap": the sovereign-side compliance and AI metrics drop by
        ``cfg.wrong_answer_penalty``.
        """
        if scenario_index in self.results:
            return self.results[scenario_index]

        seconds = (now if now is not None else time.time()) - self.round_start
        correct = chosen == scenario["correct"]
        xp = 0
        if correct:
            xp = cfg.base_xp
            if seconds <= cfg.speed_bonus_seconds:
                xp += cfg.speed_bonus_xp
        else:
            self.sovereign.apply_disruption(
                compliance_loss=cfg.wrong_answer_penalty, ai_loss=cfg.wrong_answer_penalty
            )
        self.xp += xp
        result = RoundResult(
            round_number=scenario_index + 1,
            scenario_id=scenario["id"],
            title=scenario["title"],
            chosen=chosen,
            correct=correct,
            xp_earned=xp,
            seconds=seconds,
        )
        self.results[scenario_index] = result
        return result

    def finish_game(self) -> None:
        self.game_over = True

    # ---- summaries -------------------------------------------------------
    @property
    def correct_count(self) -> int:
        return sum(1 for r in self.results.values() if r.correct)

    @property
    def total_answered(self) -> int:
        return len(self.results)

    def summary(self) -> dict:
        """JSON-serialisable summary used for the results export."""
        return {
            "xp": self.xp,
            "tier": self.tier,
            "correct_answers": self.correct_count,
            "rounds_answered": self.total_answered,
            "total_rounds": self.max_rounds,
            "sovereign_health": round(self.sovereign.overall_health, 1),
            "external_health": round(self.external.overall_health, 1),
            "rounds": [
                {
                    "round": r.round_number,
                    "scenario": r.scenario_id,
                    "chosen": r.chosen,
                    "correct": r.correct,
                    "xp": r.xp_earned,
                    "seconds": round(r.seconds, 1),
                }
                for _, r in sorted(self.results.items())
            ],
        }


# ---------------------------------------------------------------------------
# Streamlit session helpers
# ---------------------------------------------------------------------------
def init_state() -> GameState:
    """Return the session's GameState, creating it on first use."""
    import streamlit as st

    if "gs" not in st.session_state:
        st.session_state["gs"] = GameState()
    return st.session_state["gs"]


def reset_state() -> GameState:
    """Hard-reset the game (new game)."""
    import streamlit as st

    st.session_state["gs"] = GameState()
    return st.session_state["gs"]
