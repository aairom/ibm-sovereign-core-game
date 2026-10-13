"""
config.py — Runtime configuration for the Sovereign AI Challenge.

Every tunable value is read from environment variables (optionally provided
through a ``.env`` file, see ``.env.example``). Nothing is hard-coded in the
game logic, which keeps demos easy to adapt for different audiences.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping, Optional


def _int(env: Mapping[str, str], key: str, default: int) -> int:
    """Read an int from *env*, falling back to *default* on missing/invalid."""
    try:
        return int(env.get(key, default))
    except (TypeError, ValueError):
        return default


def _bool(env: Mapping[str, str], key: str, default: bool) -> bool:
    """Read a boolean flag (1/true/yes/on) from *env*."""
    raw = env.get(key)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Config:
    """Immutable application settings."""

    app_title: str = "Sovereign AI Challenge"
    base_xp: int = 200                # XP for a correct answer
    speed_bonus_xp: int = 50          # extra XP for a fast correct answer
    speed_bonus_seconds: int = 10     # "fast" threshold in seconds
    wrong_answer_penalty: int = 15    # sovereign-side metric loss on a wrong answer
    sim_requests_per_tick: int = 120  # AI requests per tick in the Kill Switch Lab
    show_disclaimer: bool = True
    output_dir: str = "output"


def load_config(env: Optional[Mapping[str, str]] = None) -> Config:
    """Build a :class:`Config` from *env* (defaults to ``os.environ``)."""
    env = os.environ if env is None else env
    d = Config()
    return Config(
        app_title=env.get("APP_TITLE", d.app_title),
        base_xp=max(0, _int(env, "BASE_XP", d.base_xp)),
        speed_bonus_xp=max(0, _int(env, "SPEED_BONUS_XP", d.speed_bonus_xp)),
        speed_bonus_seconds=max(0, _int(env, "SPEED_BONUS_SECONDS", d.speed_bonus_seconds)),
        wrong_answer_penalty=max(0, _int(env, "WRONG_ANSWER_PENALTY", d.wrong_answer_penalty)),
        sim_requests_per_tick=max(1, _int(env, "SIM_REQUESTS_PER_TICK", d.sim_requests_per_tick)),
        show_disclaimer=_bool(env, "SHOW_DISCLAIMER", d.show_disclaimer),
        output_dir=env.get("OUTPUT_DIR", d.output_dir),
    )
