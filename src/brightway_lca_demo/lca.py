"""Core LCA calculation, impact assessment, and contribution analysis using Brightway 2.5 API."""

import bw2data as bd
import bw2calc as bc
import pandas as pd


def perform_lca(
    functional_unit: dict,
    method_tuple: tuple
) -> tuple[bc.LCA, float]:
    """
    Perform matrix inversion and calculate LCIA score for given demand and impact method.

    Parameters
    ----------
    functional_unit : dict
        Brightway functional unit dictionary {ActivityNode: demand_amount}.
    method_tuple : tuple
        Key identifier of registered LCIA Method.

    Returns
    -------
    tuple[bc.LCA, float]
        Instantiated LCA object and calculated total impact score.
    """
    lca = bc.LCA(functional_unit, method_tuple)
    lca.lci()
    lca.lcia()
    return lca, float(lca.score)


def calculate_hotspots(
    lca_object: bc.LCA,
    top_n: int = 5
) -> pd.DataFrame:
    """
    Decompose total score into process-level top impact contributors (hotspots).

    Parameters
    ----------
    lca_object : bc.LCA
        Solved LCA instance after lcia() execution.
    top_n : int
        Number of top process contributors to return.

    Returns
    -------
    pd.DataFrame
        Ranked DataFrame containing process names and absolute/percentage impacts.
    """
    total_score = lca_object.score
    contributions = []

    for activity_node, col_idx in lca_object.dicts.activity.items():
        act_obj = bd.get_node(id=activity_node)
        col_score = float(lca_object.characterized_inventory[:, col_idx].sum())

        if total_score != 0:
            pct = (col_score / total_score) * 100.0
        else:
            pct = 0.0

        contributions.append({
            "Activity": act_obj["name"],
            "Database": act_obj["database"],
            "Code": act_obj["code"],
            "Absolute Contribution": col_score,
            "Percentage Contribution (%)": pct,
        })

    df = pd.DataFrame(contributions)
    df = df.sort_values(by="Absolute Contribution", ascending=False).head(top_n)
    return df.reset_index(drop=True)
