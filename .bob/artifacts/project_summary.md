# Project Summary — Sovereign AI Challenge

**Type:** Streamlit gamification demo (Python 3.12, `uv`, no cloud dependency)
**Licence:** MIT
**Purpose:** Show an audience, through play, why AI on IBM Sovereign Core (air-gapped, customer-operated) stays reliable when an external AI platform is switched off or restricted.

## What was built
| Area | Deliverable |
|---|---|
| Game | 5 scenarios: Political Kill Switch, Compliance Audit Surprise, Data Exfiltration Suspicion, GPU Shortage Emergency, New Regulation |
| Mechanics | XP, 5 tiers, speed bonus, live health bars for both platforms, sovereignty-gap penalty on wrong answers |
| Final screen | Radar SVG, comparison table, round log, JSON export to `output/` |
| Kill Switch Lab | Live simulation with Embargo and Cross-border Data Ban toggles and a cumulative chart |
| Config | All tunables via environment variables (`.env.example`) |
| Scripts | `scripts/start.sh` (detached, prints URL), `stop.sh`, `cleanup.sh`, `test.sh` |
| Docs | `README.md`, `Docs/Quickstart.md`, `Docs/Architecture.md` (Mermaid), `LICENSE` |
| Tests | 33 tests (unit + Streamlit `AppTest` end-to-end), ~95% coverage of `sovereign_game/` |

## Source messaging used (from `_sources/` decks)
- Three pillars: Sovereign from the Start, Verifiable Compliance Evidence, AI Within Your Control.
- 233 embedded compliance frameworks; governed extensible catalog; customer-operated control plane.
- Market stats quoted in the deck (Gartner, IBM IBV).

## Notes
- Metrics shown in the game are illustrative. Product claims come only from the supplied decks and were not independently verified against public IBM documentation.
- Container image: not provided (not required; app runs locally with one command).
