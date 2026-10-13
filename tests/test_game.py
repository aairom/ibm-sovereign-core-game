"""Unit tests for the Sovereign AI Challenge game logic and UI helpers."""

import pytest

from sovereign_game import components as ui
from sovereign_game.config import Config, load_config
from sovereign_game.game_state import GameState, PlatformHealth
from sovereign_game.scenarios import SCENARIOS, SCENARIO_BY_ID

CFG = Config()


# ---------------------------------------------------------------- scenarios
def test_scenarios_are_well_formed():
    assert len(SCENARIOS) == 5
    ids = [s["id"] for s in SCENARIOS]
    assert len(set(ids)) == len(ids)
    for s in SCENARIOS:
        assert s["correct"] in s["options"]
        assert len(s["options"]) == 4
        assert set(s["disruption"]) == {"sovereign", "external"}
        for side in s["disruption"].values():
            assert set(side) == {"uptime_loss", "compliance_loss", "ai_loss", "risk_gain"}
        assert s["explanation"] and s["ibm_feature"]


def test_correct_answers_are_not_always_same_letter():
    assert len({s["correct"] for s in SCENARIOS}) > 1


def test_scenario_lookup():
    assert SCENARIO_BY_ID["kill_switch"] is SCENARIOS[0]


# ------------------------------------------------------------------- health
def test_disruption_is_clamped():
    p = PlatformHealth("x")
    p.apply_disruption(uptime_loss=500, risk_gain=500)
    assert p.uptime == 0.0
    assert p.political_risk == 100.0


def test_overall_health_average():
    p = PlatformHealth("x", uptime=90, compliance_score=60, ai_reliability=30)
    assert p.overall_health == pytest.approx(60.0)


# --------------------------------------------------------------- game state
def test_correct_fast_answer_gets_speed_bonus():
    gs = GameState()
    gs.start_round(1)
    r = gs.record_answer(0, SCENARIOS[0], SCENARIOS[0]["correct"], CFG, now=gs.round_start + 3)
    assert r.correct and r.xp_earned == CFG.base_xp + CFG.speed_bonus_xp
    assert gs.xp == r.xp_earned


def test_correct_slow_answer_no_bonus():
    gs = GameState()
    r = gs.record_answer(0, SCENARIOS[0], SCENARIOS[0]["correct"], CFG, now=gs.round_start + 60)
    assert r.xp_earned == CFG.base_xp


def test_wrong_answer_penalises_sovereign_side_and_gives_no_xp():
    gs = GameState()
    r = gs.record_answer(0, SCENARIOS[0], "a", CFG)
    assert not r.correct and r.xp_earned == 0 and gs.xp == 0
    assert gs.sovereign.compliance_score == 100 - CFG.wrong_answer_penalty
    assert gs.sovereign.ai_reliability == 100 - CFG.wrong_answer_penalty


def test_answer_is_scored_only_once():
    gs = GameState()
    first = gs.record_answer(0, SCENARIOS[0], SCENARIOS[0]["correct"], CFG, now=gs.round_start + 1)
    again = gs.record_answer(0, SCENARIOS[0], "a", CFG)
    assert again is first
    assert gs.xp == first.xp_earned and gs.total_answered == 1


def test_disruption_applied_once():
    gs = GameState()
    d = SCENARIOS[0]["disruption"]
    gs.apply_scenario_disruption(0, d)
    snapshot = gs.external.uptime
    gs.apply_scenario_disruption(0, d)
    assert gs.external.uptime == snapshot
    assert gs.external.uptime == 100 - d["external"]["uptime_loss"]


def test_sovereign_beats_external_after_full_perfect_game():
    gs = GameState()
    for i, s in enumerate(SCENARIOS):
        gs.apply_scenario_disruption(i, s["disruption"])
        gs.record_answer(i, s, s["correct"], CFG, now=gs.round_start + 1)
    assert gs.correct_count == 5
    assert gs.sovereign.overall_health > gs.external.overall_health
    assert gs.sovereign.uptime == 100


def test_tiers_progress_with_xp():
    gs = GameState()
    assert gs.tier == "Observer"
    gs.xp = 250
    assert gs.tier == "Analyst" and gs.next_tier_xp == 500
    gs.xp = 5000
    assert gs.tier == "Master of Sovereignty" and gs.next_tier_xp == 5000


def test_start_round_and_finish():
    gs = GameState()
    gs.start_round(3)
    assert gs.round_number == 3 and gs.elapsed_seconds() >= 0
    gs.finish_game()
    assert gs.game_over


def test_summary_is_serialisable():
    import json

    gs = GameState()
    gs.record_answer(0, SCENARIOS[0], "b", CFG, now=gs.round_start + 1)
    out = json.loads(json.dumps(gs.summary()))
    assert out["correct_answers"] == 1 and out["rounds"][0]["scenario"] == "kill_switch"


# ------------------------------------------------------------------- config
def test_config_defaults_and_overrides():
    assert load_config({}) == Config()
    c = load_config({"BASE_XP": "300", "SHOW_DISCLAIMER": "false", "OUTPUT_DIR": "o"})
    assert c.base_xp == 300 and c.show_disclaimer is False and c.output_dir == "o"


def test_config_rejects_bad_values():
    c = load_config({"BASE_XP": "abc", "SPEED_BONUS_XP": "-5", "SIM_REQUESTS_PER_TICK": "0"})
    assert c.base_xp == Config().base_xp
    assert c.speed_bonus_xp == 0
    assert c.sim_requests_per_tick == 1


# --------------------------------------------------------------- UI helpers
def test_styles_are_offline_safe():
    css = ui.base_styles()
    assert "<style>" in css and "http" not in css  # no CDN / remote assets


def test_platform_card_states():
    ok = ui.platform_health_card("A", 100, 100, 100, 0, "sovereign")
    bad = ui.platform_health_card("B", 10, 10, 10, 90, "external")
    assert "Online" in ok and "Degraded" in bad


def test_progress_and_xp_bars():
    html = ui.round_progress_bar(2, 5)
    assert html.count("done") == 1 and html.count("active") == 1 and html.count("future") == 3
    assert "width:100.0%" in ui.xp_progress_bar(500, 500, "Max")
    assert "width:50.0%" in ui.xp_progress_bar(100, 200, "T")


def test_misc_components_render():
    assert "sc-toast error" in ui.toast("x", "error")
    assert "42" in ui.score_grid([("L", 42, True)])
    assert "Capability" in ui.comparison_table(ui.COMPARISON_ROWS)
    assert "IBM Sovereign Core" in ui.impact_grid("a", "b") or "SOVEREIGN" in ui.impact_grid("a", "b")
    assert "why" in ui.explanation_box("why", "feat").lower()
    assert "ROUND 1 / 5" in ui.scenario_header("T", ["tag"], 1, 5)


def test_radar_chart():
    svg = ui.radar_chart_svg(["a", "b", "c"], [10, 50, 90], [20, 30, 40])
    assert svg.startswith("<svg") and svg.count("<polygon") >= 6
    assert ui.radar_chart_svg(["a", "b"], [1, 2], [1, 2]) == ""


# --------------------------------------------------------------- simulation
from sovereign_game import simulation as sim  # noqa: E402


def test_sim_normal_traffic():
    lab = sim.LabState()
    sim.step(lab, 100)
    assert lab.sov_served == 100 and lab.ext_served == 100
    assert lab.history[-1] == (1, 100, 100)


def test_sim_embargo_stops_cloud_only():
    lab = sim.LabState(embargo=True)
    for _ in range(3):
        sim.step(lab, 50)
    assert lab.sov_served == 150 and lab.ext_served == 0 and lab.ext_failed == 150
    assert sim.availability(lab.ext_served, lab.ext_failed) == 0.0
    assert sim.availability(lab.sov_served, lab.sov_failed) == 100.0


def test_sim_cross_border_ban_creates_violations_only_on_cloud():
    lab = sim.LabState(cross_border_ban=True)
    sim.step(lab, 40)
    assert lab.ext_violations == 40 and lab.sov_violations == 0
    assert sim.compliance_rate(lab.ext_served, lab.ext_violations) == 0.0


def test_sim_rates_with_no_traffic_and_reset():
    assert sim.availability(0, 0) == 100.0 and sim.compliance_rate(0, 0) == 100.0
    lab = sim.LabState(embargo=True, running=True)
    sim.step(lab, 10)
    sim.reset(lab)
    assert lab.tick == 0 and not lab.embargo and not lab.running and lab.history == [(0, 0, 0)]


def test_low_political_risk_is_green_high_is_red():
    low = ui.platform_health_card("A", 100, 100, 100, 0, "sovereign")
    high = ui.platform_health_card("B", 100, 100, 100, 90, "external")
    # 4 healthy metrics -> all green when risk is 0
    assert low.count("color:#da1e28") == 0
    # only the political-risk value turns red when risk is 90
    assert high.count("color:#da1e28") == 1


def test_inline_md_converts_bold_in_html_builders():
    """Regression: **bold** must not leak into raw HTML blocks."""
    from sovereign_game.components import explanation_box, inline_md, toast

    assert inline_md("a **b** c **d**") == "a <strong>b</strong> c <strong>d</strong>"
    assert "**" not in explanation_box("x **y**", "feat")
    assert "<strong>y</strong>" in toast("x **y**", "info")
