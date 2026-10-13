"""
simulation.py — Pure logic for the interactive "Kill Switch Lab".

Two platforms serve the same stream of AI requests every tick:

* IBM Sovereign Core: customer-operated and in-boundary, so it keeps serving
  whatever happens outside the boundary (it has no runtime dependency on a
  foreign endpoint).
* Public Cloud AI: depends on the vendor's API, so an embargo stops it, and a
  cross-border data ban turns every request it serves into a compliance
  violation.

The module has no Streamlit imports so it is trivially unit testable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class LabState:
    """Mutable state of one Kill Switch Lab session."""

    tick: int = 0
    embargo: bool = False            # foreign provider cuts access
    cross_border_ban: bool = False   # regulator forbids data leaving the boundary
    running: bool = False
    sov_served: int = 0
    sov_failed: int = 0
    sov_violations: int = 0
    ext_served: int = 0
    ext_failed: int = 0
    ext_violations: int = 0
    # (tick, sovereign cumulative served, external cumulative served)
    history: List[Tuple[int, int, int]] = field(default_factory=lambda: [(0, 0, 0)])


def step(lab: LabState, requests_per_tick: int) -> None:
    """Advance the simulation by one tick of *requests_per_tick* AI requests."""
    lab.tick += 1

    # Sovereign Core: always served inside the boundary, never a violation.
    lab.sov_served += requests_per_tick

    # Public cloud: embargo blocks everything; otherwise requests are served,
    # but a cross-border ban makes each served request a violation.
    if lab.embargo:
        lab.ext_failed += requests_per_tick
    else:
        lab.ext_served += requests_per_tick
        if lab.cross_border_ban:
            lab.ext_violations += requests_per_tick

    lab.history.append((lab.tick, lab.sov_served, lab.ext_served))


def availability(served: int, failed: int) -> float:
    """Percentage of requests served successfully (100.0 when no traffic)."""
    total = served + failed
    return 100.0 if total == 0 else served / total * 100.0


def compliance_rate(served: int, violations: int) -> float:
    """Percentage of served requests that were compliant (100.0 when none)."""
    return 100.0 if served == 0 else (served - violations) / served * 100.0


def reset(lab: LabState) -> None:
    """Reset counters and history in place (keeps nothing running)."""
    fresh = LabState()
    lab.__dict__.update(fresh.__dict__)
