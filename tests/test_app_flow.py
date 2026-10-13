"""End-to-end UI tests driving the real Streamlit pages with AppTest."""

from pathlib import Path

from streamlit.testing.v1 import AppTest

from sovereign_game.scenarios import SCENARIOS

ROOT = Path(__file__).resolve().parent.parent


def _app() -> AppTest:
    return AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()


def _click(at: AppTest, label_part: str) -> AppTest:
    btn = next(b for b in at.button if label_part in b.label)
    return btn.click().run()


def test_welcome_screen_renders():
    at = _app()
    assert not at.exception
    assert any("Start the Challenge" in b.label for b in at.button)


def test_full_perfect_playthrough_reaches_final_screen():
    at = _click(_app(), "Start the Challenge")
    for i, scenario in enumerate(SCENARIOS):
        assert not at.exception
        at = at.button(f"opt_{i}_{scenario['correct']}").click().run()
        assert not at.exception
        at = _click(at, "Next Round" if i < len(SCENARIOS) - 1 else "View Final Results")
    assert not at.exception
    assert any("Challenge Complete" in m.value for m in at.markdown)
    assert at.session_state["gs"].correct_count == len(SCENARIOS)
    assert at.session_state["gs"].game_over


def test_wrong_answer_shows_error_feedback():
    at = _click(_app(), "Start the Challenge")
    wrong = next(k for k in SCENARIOS[0]["options"] if k != SCENARIOS[0]["correct"])
    at = at.button(f"opt_0_{wrong}").click().run()
    assert not at.exception
    assert any("Not quite" in m.value for m in at.markdown)
    assert at.session_state["gs"].xp == 0


def test_restart_resets_state():
    at = _click(_app(), "Start the Challenge")
    at = _click(at, "Restart Game")
    assert at.session_state["gs"].round_number == 0


def test_kill_switch_lab_page_renders_and_controls():
    at = AppTest.from_file(str(ROOT / "pages" / "1_Kill_Switch_Lab.py"), default_timeout=30).run()
    assert not at.exception
    labels = [b.label for b in at.button]
    assert any("Start Simulation" in label for label in labels)
    # Embargo/ban controls are disabled until the simulation runs
    assert all(b.disabled for b in at.button if "Embargo" in b.label or "Data Ban" in b.label)


def test_sidebar_matches_round_disruption_immediately():
    at = _click(_app(), "Start the Challenge")
    gs = at.session_state["gs"]
    expected = 100 - SCENARIOS[0]["disruption"]["external"]["uptime_loss"]
    assert gs.external.uptime == expected
    # sidebar gauge for the cloud reflects the disrupted overall health
    assert f"{gs.external.overall_health:.0f}%" in " ".join(m.value for m in at.sidebar.markdown)
