"""Master execution script running full LCA pipeline."""

import logging
from pathlib import Path
import pandas as pd

from .config import load_config, setup_brightway_project, get_project_root
from .database import create_synthetic_biosphere, create_synthetic_foreground
from .inventory import get_functional_unit
from .lca import perform_lca, calculate_hotspots
from .scenarios import run_scenario_analysis
from .visualization import plot_comparative_results, plot_scenario_results
from .export import export_results_to_csv, export_results_to_excel

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def main() -> None:
    """Execute end-to-end LCA calculation pipeline."""
    logging.info("Starting Brightway LCA Demonstration pipeline...")

    # 1. Load Setup & Initialize Project
    config = load_config()
    project_name = setup_brightway_project(config["project"]["name"])
    logging.info(f"Initialized active Brightway project context: {project_name}")

    # 2. Build Synthetic Databases
    bio_db = create_synthetic_biosphere(config["databases"]["biosphere"])
    fg_db = create_synthetic_foreground(
        config["databases"]["foreground"],
        config["databases"]["biosphere"]
    )
    logging.info(f"Registered databases: {list(bio_db.name for bio_db in [bio_db, fg_db])}")

    # 3. Define Functional Units & Methods
    methods = [
        (("IPCC_2021_Synthetic", "Climate Change", "GWP100"), "kg CO2 eq"),
        (("AWARE_Synthetic", "Water Depletion", "WDP"), "m3 water eq"),
        (("ReCiPe_Synthetic", "Fossil Resource Depletion", "FFP"), "MJ eq"),
    ]

    options = ["pet", "aluminum"]
    results_list = []
    hotspots_dict = {}

    # 4. Perform Comparative LCAs
    for opt in options:
        fu = get_functional_unit(config, option=opt)
        for method_tuple, unit in methods:
            lca_obj, score = perform_lca(fu, method_tuple)
            method_label = method_tuple[1]
            results_list.append({
                "Option": opt.upper(),
                "Method": method_label,
                "Score": score,
                "Unit": unit
            })

            if method_tuple[0] == "IPCC_2021_Synthetic":
                hotspots_df = calculate_hotspots(lca_obj, top_n=5)
                hotspots_dict[f"{opt.upper()}_GWP_Hotspots"] = hotspots_df

    df_results = pd.DataFrame(results_list)
    logging.info("\n=== Comparative LCA Results ===\n" + df_results.to_string(index=False))

    # 5. Scenario Analysis
    scenario_res = run_scenario_analysis(config, options=options)
    logging.info("Completed scenario sensitivity analysis.")

    # 6. Visualization & Export
    out_dir = get_project_root() / config["output_paths"]["reports"]
    out_dir.mkdir(parents=True, exist_ok=True)

    plot_comparative_results(df_results, out_dir)
    plot_scenario_results(scenario_res, out_dir)

    export_results_to_csv(df_results, "comparative_lca_results.csv", out_dir)

    excel_data = {"Comparative_Summary": df_results}
    excel_data.update(hotspots_dict)
    export_results_to_excel(excel_data, "lca_full_report.xlsx", out_dir)

    logging.info(f"Pipeline executed successfully. Outputs exported to: {out_dir.resolve()}")


if __name__ == "__main__":
    main()
