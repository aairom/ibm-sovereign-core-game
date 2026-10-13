# Quickstart — Sovereign AI Challenge

> Get the demo running and ready for an audience in under 5 minutes.

---

## Prerequisites

| Requirement | Version | Notes |
|---|---|---|
| Python | 3.12+ | 3.11 will also work |
| [uv](https://docs.astral.sh/uv/) | any recent | `brew install uv` on macOS |
| macOS / Linux | — | Windows WSL2 also works |

No cloud account, no API key, no internet access needed.

---

## 1. Set Up

```bash
# From the project root
cp .env.example .env   # optional — all defaults work out of the box
```

All configuration is optional. Open `.env` only if you need to change the port or tune XP values.

---

## 2. Start the Application

```bash
bash scripts/start.sh
```

The script:
1. Creates a `.venv` with `uv` (Python 3.12) if it doesn't already exist.
2. Installs dependencies from `requirements.txt` into the venv.
3. Starts Streamlit in detached mode (background).
4. Waits up to 30 s for the health endpoint to respond.
5. Prints the URL.

Expected output:
```
Sovereign AI Challenge is running (PID 12345)
Open: http://localhost:8501
```

---

## 3. Open the App

Navigate to **http://localhost:8501** in your browser.

You'll see the welcome screen — "🛡️ Sovereign AI Challenge" — with the Start button and a live sidebar showing both platform health bars.

---

## 4. Playing the Game

| Screen | What to do |
|---|---|
| **Welcome** | Click "🚀 Start the Challenge" |
| **Round (1–5)** | Read the scenario narrative and impact panels, then click your answer |
| **Result** | See the correct answer highlighted, XP awarded, and the IBM feature explanation |
| **Next Round** | Click "Next Round →" or "🏁 View Final Results" on round 5 |
| **Final screen** | Review the radar chart and platform summaries; click "💾 Export Results (JSON)" |
| **Kill Switch Lab** | Click "Kill Switch Lab" in the left sidebar |

### Answering Quickly

A ⚡ speed bonus (+50 XP) is awarded if you answer within **10 seconds** of the round appearing. An elapsed-time counter is shown above the answers.

### XP Tiers

| XP | Tier |
|---|---|
| 0 | Observer |
| 200 | Analyst |
| 500 | Architect |
| 800 | Sovereign Guardian |
| 1100 | Master of Sovereignty |

Perfect score (all 5 correct with speed bonuses): **1,250 XP**.

---

## 5. Kill Switch Lab

Navigate to **Kill Switch Lab** in the left sidebar.

1. Click **▶ Start Simulation** — both platform lines rise together.
2. Click **⚡ Trigger Embargo** — the cloud AI line flatlines; IBM Sovereign Core continues.
3. Click **📜 Trigger Data Ban** — the cloud compliance score drops; Sovereign Core stays green.
4. Click **🔄 Reset** to start over.

Expand the "💡 Why does IBM Sovereign Core stay green?" panel for a talking-point table suitable for Q&A.

---

## 6. Stop the Application

```bash
bash scripts/stop.sh
```

---

## 7. Clean Up (End of Demo)

To remove the virtual environment and all generated artefacts:

```bash
bash scripts/cleanup.sh
```

This removes `.venv`, `__pycache__`, `.pytest_cache`, `.run/` and any `node_modules` folders. It does **not** touch `_sources/`, `input/` or `output/`.

---

## 8. Run the Test Suite

```bash
bash scripts/test.sh
```

Expected output: 32+ tests passing, ≥ 90% coverage on `sovereign_game/`.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `Port 8501 already in use` | Run `bash scripts/stop.sh` first, or set `SERVER_PORT=8502` in `.env` |
| `uv not found` | Install with `curl -Lf https://astral.sh/uv/install.sh \| sh` |
| White page / JS error | Hard-refresh the browser (Cmd+Shift+R / Ctrl+Shift+R) |
| `ModuleNotFoundError` | Delete `.venv/` and re-run `bash scripts/start.sh` |
| Kill Switch Lab chart not updating | Streamlit WebSocket may have disconnected; reload the page |

---

## Demo Tips

- **Audience intro**: open the welcome screen before the meeting, hide the sidebar to maximise impact.
- **Live Kill Switch**: trigger the Embargo mid-demo for a dramatic real-time divergence effect.
- **Export JSON**: show the `output/` file as evidence the game can be run offline with no data leaving the room.
- **Customise scenarios**: edit `sovereign_game/scenarios.py` for audience-specific industries (finance, healthcare, defence). All changes take effect after a page reload.
