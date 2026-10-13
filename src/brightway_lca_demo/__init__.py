"""
Brightway LCA Demo Package.

A modular framework for demonstrating Life Cycle Assessment using Brightway 2.5.
"""

__version__ = "1.0.0"
__author__ = "Brightway LCA Demo Contributors"

from .config import load_config, setup_brightway_project
from .database import create_synthetic_biosphere, create_synthetic_foreground
from .inventory import get_functional_unit
from .lca import perform_lca, calculate_hotspots
from .scenarios import run_scenario_analysis
from .visualization import plot_comparative_results, plot_scenario_results
from .export import export_results_to_csv, export_results_to_excel

__all__ = [
    "load_config",
    "setup_brightway_project",
    "create_synthetic_biosphere",
    "create_synthetic_foreground",
    "get_functional_unit",
    "perform_lca",
    "calculate_hotspots",
    "run_scenario_analysis",
    "plot_comparative_results",
    "plot_scenario_results",
    "export_results_to_csv",
    "export_results_to_excel",
]
