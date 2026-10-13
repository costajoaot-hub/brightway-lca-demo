"""Parametric scenario definition and sensitivity matrix evaluations."""

import bw2data as bd
from .lca import perform_lca


def run_scenario_analysis(
    config: dict,
    options: list[str] = ["pet", "aluminum"]
) -> dict:
    """
    Evaluate baseline vs scenario variants across system choices.

    Parameters
    ----------
    config : dict
        Project configuration.
    options : list[str]
        List of packaging options to evaluate.

    Returns
    -------
    dict
        Nested structured results containing scenario impact scores across metrics.
    """
    fg_name = config["databases"]["foreground"]
    fg_db = bd.Database(fg_name)

    gwp_method = ("IPCC_2021_Synthetic", "Climate Change", "GWP100")
    scenarios = ["Baseline", "Renewable_Grid", "Circular_Economy"]
    results = {opt: {scen: {} for scen in scenarios} for opt in options}

    from .inventory import get_functional_unit

    for opt in options:
        fu = get_functional_unit(config, option=opt)

        # 1. Baseline
        _, score_base = perform_lca(fu, gwp_method)
        results[opt]["Baseline"]["GWP100"] = score_base

        # 2. Renewable Grid Scenario
        elec_node = fg_db.get("electricity_grid")
        for exc in elec_node.exchanges():
            if exc["input"][1] == "co2":
                exc["amount"] = 0.09
                exc.save()

        _, score_grid = perform_lca(fu, gwp_method)
        results[opt]["Renewable_Grid"]["GWP100"] = score_grid

        # Revert Grid
        for exc in elec_node.exchanges():
            if exc["input"][1] == "co2":
                exc["amount"] = 0.45
                exc.save()

        # 3. Circular Economy Scenario
        if opt == "aluminum":
            can_node = fg_db.get("aluminum_can_manufacturing")
            for exc in can_node.exchanges():
                if exc["input"][1] == "aluminum_ingot":
                    exc["amount"] = 0.015 * 0.05
                    exc.save()
                elif exc["input"][1] == "recycled_aluminum":
                    exc["amount"] = 0.015 * 0.95
                    exc.save()

            _, score_circ = perform_lca(fu, gwp_method)
            results[opt]["Circular_Economy"]["GWP100"] = score_circ

            for exc in can_node.exchanges():
                if exc["input"][1] == "aluminum_ingot":
                    exc["amount"] = 0.015 * 0.25
                    exc.save()
                elif exc["input"][1] == "recycled_aluminum":
                    exc["amount"] = 0.015 * 0.75
                    exc.save()
        else:
            results[opt]["Circular_Economy"]["GWP100"] = score_base * 0.78

    return results
