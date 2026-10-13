"""Publication-ready chart and figure generation using Matplotlib."""

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def plot_comparative_results(
    df_results: pd.DataFrame,
    output_dir: Path
) -> Path:
    """
    Generate comparative bar plot for options across impact categories.

    Parameters
    ----------
    df_results : pd.DataFrame
        DataFrame with columns ['Option', 'Method', 'Score', 'Unit'].
    output_dir : Path
        Directory to save output image.

    Returns
    -------
    Path
        Path to output saved figure.
    """
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)

    pivot_df = df_results.pivot(index="Method", columns="Option", values="Score")
    norm_df = pivot_df.div(pivot_df.max(axis=1), axis=0) * 100.0

    norm_df.plot(kind="bar", ax=ax, width=0.6, colormap="viridis")

    ax.set_title("Comparative Environmental Impact (% Relative Peak)", fontsize=12, fontweight="bold")
    ax.set_ylabel("Relative Impact (%)", fontsize=10)
    ax.set_xlabel("Impact Category", fontsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()

    out_path = output_dir / "comparative_impacts.png"
    plt.savefig(out_path)
    plt.close()
    return out_path


def plot_scenario_results(
    scenario_dict: dict,
    output_dir: Path
) -> Path:
    """
    Plot scenario analysis sensitivity comparison.

    Parameters
    ----------
    scenario_dict : dict
        Nested dictionary of scenario results.
    output_dir : Path
        Directory to save output plot.

    Returns
    -------
    Path
        Path to saved figure file.
    """
    df = pd.DataFrame.from_dict({
        (opt, scen): metrics
        for opt, scens in scenario_dict.items()
        for scen, metrics in scens.items()
    }, orient="index")

    df.index = pd.MultiIndex.from_tuples(df.index, names=["Option", "Scenario"])
    df_unstacked = df["GWP100"].unstack(level=0)

    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    df_unstacked.plot(kind="bar", ax=ax, colormap="Accent", width=0.7)

    ax.set_title("Climate Change Sensitivity across Scenarios", fontsize=12, fontweight="bold")
    ax.set_ylabel("Climate Change Impact (kg CO2 eq)", fontsize=10)
    ax.set_xlabel("Scenario Identifier", fontsize=10)
    ax.grid(axis="y", linestyle=":", alpha=0.6)
    plt.xticks(rotation=0)
    plt.tight_layout()

    out_path = output_dir / "scenario_sensitivity.png"
    plt.savefig(out_path)
    plt.close()
    return out_path
