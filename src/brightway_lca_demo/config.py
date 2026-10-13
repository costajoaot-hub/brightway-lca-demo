"""Configuration loader and Brightway project environment setup."""

from pathlib import Path
import yaml
import bw2data as bd


def get_project_root() -> Path:
    """Return the root path of the repository."""
    return Path(__file__).resolve().parent.parent.parent


def load_config(config_path: Path | None = None) -> dict:
    """
    Load project configuration settings from a YAML file.

    Parameters
    ----------
    config_path : Path, optional
        Path to settings.yaml file. Defaults to config/settings.yaml.

    Returns
    -------
    dict
        Configuration dictionary.
    """
    if config_path is None:
        config_path = get_project_root() / "config" / "settings.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def setup_brightway_project(project_name: str, overwrite: bool = True) -> str:
    """
    Initialize and set current Brightway project space.

    Parameters
    ----------
    project_name : str
        Name of the Brightway project.
    overwrite : bool
        If True, deletes existing project with same name to ensure clean state.

    Returns
    -------
    str
        Active project name.
    """
    if overwrite and project_name in bd.projects:
        bd.projects.delete_project(project_name, delete_dir=True)

    bd.projects.set_current(project_name)
    return bd.projects.current
