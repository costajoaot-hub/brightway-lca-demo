"""Tests for database building and inventory parameter logic."""

import pytest
import bw2data as bd
from brightway_lca_demo.config import setup_brightway_project, load_config
from brightway_lca_demo.database import create_synthetic_biosphere, create_synthetic_foreground
from brightway_lca_demo.inventory import get_functional_unit


@pytest.fixture(autouse=True)
def init_test_project():
    """Setup isolated test environment before each test function."""
    setup_brightway_project("Test_BW_Project", overwrite=True)
    config = load_config()
    create_synthetic_biosphere(config["databases"]["biosphere"])
    create_synthetic_foreground(config["databases"]["foreground"], config["databases"]["biosphere"])
    yield


def test_database_creation():
    """Verify databases are registered and contain expected activities."""
    assert "synthetic_biosphere" in bd.databases
    assert "packaging_foreground" in bd.databases

    fg = bd.Database("packaging_foreground")
    assert len(fg) >= 5


def test_functional_unit_scaling():
    """Check functional unit scaling calculations."""
    config = load_config()
    fu_pet = get_functional_unit(config, option="pet")

    act_node = list(fu_pet.keys())[0]
    amount = fu_pet[act_node]

    # 1000L / 0.5L = 2000 units
    assert amount == pytest.approx(2000.0)
