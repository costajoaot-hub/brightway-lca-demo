"""Functional unit scaling and inventory reference flow derivation."""

import bw2data as bd


def get_functional_unit(
    config: dict,
    option: str = "pet"
) -> dict[bd.Node, float]:
    """
    Calculate Brightway functional unit demand dictionary based on reference flows.

    Parameters
    ----------
    config : dict
        Project configuration metadata.
    option : str
        Packaging option key ('pet' or 'aluminum').

    Returns
    -------
    dict[bd.Node, float]
        Dictionary mapping activity node to calculated demand scalar.
    """
    fg_name = config["databases"]["foreground"]
    fg_db = bd.Database(fg_name)

    target_volume = config["functional_unit"]["target_volume_liters"]

    if option.lower() == "pet":
        unit_vol = config["functional_unit"]["pet_bottle_volume_liters"]
        number_of_units = target_volume / unit_vol
        activity = fg_db.get("pet_bottle_manufacturing")
    elif option.lower() in ("aluminum", "can"):
        unit_vol = config["functional_unit"]["aluminum_can_volume_liters"]
        number_of_units = target_volume / unit_vol
        activity = fg_db.get("aluminum_can_manufacturing")
    else:
        raise ValueError(f"Unknown option '{option}'. Must be 'pet' or 'aluminum'.")

    return {activity: float(number_of_units)}
