"""Tests for scenario sensitivity variations."""

from brightway_lca_demo.config import setup_brightway_project, load_config
from brightway_lca_demo.database import create_synthetic_biosphere, create_synthetic_foreground
from brightway_lca_demo.scenarios import run_scenario_analysis


def test_scenario_analysis_execution():
    """Ensure scenarios execute and return lower carbon score under renewable grid."""
    setup_brightway_project("Test_BW_Project_Scenarios", overwrite=True)
    config = load_config()
    create_synthetic_biosphere(config["databases"]["biosphere"])
    create_synthetic_foreground(config["databases"]["foreground"], config["databases"]["biosphere"])

    results = run_scenario_analysis(config, options=["pet"])

    base_score = results["pet"]["Baseline"]["GWP100"]
    grid_score = results["pet"]["Renewable_Grid"]["GWP100"]

    assert grid_score < base_score
