"""Data export utilities for tabular CSV and Excel file formats."""

from pathlib import Path
import pandas as pd


def export_results_to_csv(
    df: pd.DataFrame,
    filename: str,
    output_dir: Path
) -> Path:
    """
    Export results DataFrame to CSV file.

    Parameters
    ----------
    df : pd.DataFrame
        Data to export.
    filename : str
        Target filename.
    output_dir : Path
        Target directory.

    Returns
    -------
    Path
        Path to exported CSV file.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / filename
    df.to_csv(out_path, index=False)
    return out_path


def export_results_to_excel(
    dataframes_dict: dict[str, pd.DataFrame],
    filename: str,
    output_dir: Path
) -> Path:
    """
    Export multiple result tables to separate sheets in a single Excel workbook.

    Parameters
    ----------
    dataframes_dict : dict[str, pd.DataFrame]
        Mapping of sheet names to DataFrames.
    filename : str
        Target workbook name.
    output_dir : Path
        Directory destination.

    Returns
    -------
    Path
        Path to saved Excel file.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / filename

    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        for sheet_name, df in dataframes_dict.items():
            df.to_excel(writer, sheet_name=sheet_name[:31], index=False)

    return out_path
