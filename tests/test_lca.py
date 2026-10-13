"""Tests for LCA matrix inversion and calculation outputs."""

from brightway_lca_demo.config import setup_brightway_project, load_config
from brightway_lca_demo.database import create_synthetic_biosphere, create_synthetic_foreground
from brightway_lca_demo.inventory import get_functional_unit
from brightway_lca_demo.lca import perform_lca, calculate_hotspots


def test_lca_calculation():
    """Test LCA matrix inversion and non-zero positive impact score return."""
    setup_brightway_project("Test_BW_Project_LCA", overwrite=True)
    config = load_config()
    create_synthetic_biosphere(config["databases"]["biosphere"])
    create_synthetic_foreground(config["databases"]["foreground"], config["databases"]["biosphere"])

    fu = get_functional_unit(config, option="pet")
    method = ("IPCC_2021_Synthetic", "Climate Change", "GWP100")

    lca_obj, score = perform_lca(fu, method)

    assert score > 0.0
    assert lca_obj.inventory is not None


def test_hotspot_calculation():
    """Test process hotspot generation."""
    setup_brightway_project("Test_BW_Project_LCA", overwrite=True)
    config = load_config()
    create_synthetic_biosphere(config["databases"]["biosphere"])
    create_synthetic_foreground(config["databases"]["foreground"], config["databases"]["biosphere"])

    fu = get_functional_unit(config, option="pet")
    method = ("IPCC_2021_Synthetic", "Climate Change", "GWP100")

    lca_obj, _ = perform_lca(fu, method)
    df_hotspots = calculate_hotspots(lca_obj, top_n=3)

    assert not df_hotspots.empty
    assert "Percentage Contribution (%)" in df_hotspots.columns
