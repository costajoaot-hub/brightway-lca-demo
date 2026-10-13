"""Database generation for biosphere and foreground technosphere inventory data."""

import bw2data as bd


def create_synthetic_biosphere(biosphere_name: str = "synthetic_biosphere") -> bd.Database:
    """
    Build and register a synthetic biosphere database with elementary flows and LCIA methods.

    Parameters
    ----------
    biosphere_name : str
        Database key identifier for the biosphere.

    Returns
    -------
    bd.Database
        Registered Brightway Biosphere Database instance.
    """
    if biosphere_name in bd.databases:
        del bd.databases[biosphere_name]

    bio_db = bd.Database(biosphere_name)
    bio_data = {
        (biosphere_name, "co2"): {
            "name": "Carbon dioxide, fossil",
            "unit": "kilogram",
            "type": "emission",
            "categories": ("air",),
        },
        (biosphere_name, "ch4"): {
            "name": "Methane, fossil",
            "unit": "kilogram",
            "type": "emission",
            "categories": ("air",),
        },
        (biosphere_name, "water_use"): {
            "name": "Water, fresh resource",
            "unit": "cubic meter",
            "type": "natural resource",
            "categories": ("natural resource", "in water"),
        },
        (biosphere_name, "crude_oil"): {
            "name": "Oil, crude resource",
            "unit": "megajoule",
            "type": "natural resource",
            "categories": ("natural resource", "in ground"),
        },
    }
    bio_db.write(bio_data)

    # Define synthetic LCIA methods
    gwp_method = bd.Method(("IPCC_2021_Synthetic", "Climate Change", "GWP100"))
    gwp_method.register()
    gwp_method.write([
        ((biosphere_name, "co2"), 1.0),
        ((biosphere_name, "ch4"), 28.0),
    ])

    water_method = bd.Method(("AWARE_Synthetic", "Water Depletion", "WDP"))
    water_method.register()
    water_method.write([
        ((biosphere_name, "water_use"), 1.0),
    ])

    fossil_method = bd.Method(("ReCiPe_Synthetic", "Fossil Resource Depletion", "FFP"))
    fossil_method.register()
    fossil_method.write([
        ((biosphere_name, "crude_oil"), 1.0),
    ])

    return bio_db


def create_synthetic_foreground(
    fg_name: str = "packaging_foreground",
    bio_name: str = "synthetic_biosphere"
) -> bd.Database:
    """
    Build and register synthetic foreground activities and product supply chains.

    Parameters
    ----------
    fg_name : str
        Foreground database identifier.
    bio_name : str
        Associated biosphere database identifier.

    Returns
    -------
    bd.Database
        Registered Brightway Foreground Database instance.
    """
    if fg_name in bd.databases:
        del bd.databases[fg_name]

    fg_db = bd.Database(fg_name)

    # System Activities
    fg_data = {
        # Shared Energy/Transport Backgrounds
        (fg_name, "electricity_grid"): {
            "name": "Electricity grid mix, regional",
            "unit": "kilowatt hour",
            "type": "process",
            "exchanges": [
                {"input": (fg_name, "electricity_grid"), "amount": 1.0, "type": "production"},
                {"input": (bio_name, "co2"), "amount": 0.45, "type": "biosphere"},
                {"input": (bio_name, "crude_oil"), "amount": 3.5, "type": "biosphere"},
            ],
        },
        (fg_name, "transport_freight"): {
            "name": "Freight transport, lorry",
            "unit": "ton kilometer",
            "type": "process",
            "exchanges": [
                {"input": (fg_name, "transport_freight"), "amount": 1.0, "type": "production"},
                {"input": (bio_name, "co2"), "amount": 0.12, "type": "biosphere"},
                {"input": (bio_name, "crude_oil"), "amount": 1.8, "type": "biosphere"},
            ],
        },
        # PET Packaging Supply Chain
        (fg_name, "pet_granules"): {
            "name": "PET resin production",
            "unit": "kilogram",
            "type": "process",
            "exchanges": [
                {"input": (fg_name, "pet_granules"), "amount": 1.0, "type": "production"},
                {"input": (fg_name, "electricity_grid"), "amount": 1.5, "type": "technosphere"},
                {"input": (bio_name, "co2"), "amount": 1.8, "type": "biosphere"},
                {"input": (bio_name, "water_use"), "amount": 0.05, "type": "biosphere"},
                {"input": (bio_name, "crude_oil"), "amount": 42.0, "type": "biosphere"},
            ],
        },
        (fg_name, "pet_bottle_manufacturing"): {
            "name": "PET bottle blow molding & delivery",
            "unit": "unit",
            "type": "process",
            "exchanges": [
                {"input": (fg_name, "pet_bottle_manufacturing"), "amount": 1.0, "type": "production"},
                {"input": (fg_name, "pet_granules"), "amount": 0.025, "type": "technosphere"},
                {"input": (fg_name, "electricity_grid"), "amount": 0.1, "type": "technosphere"},
                {"input": (fg_name, "transport_freight"), "amount": 0.025 * 100 / 1000, "type": "technosphere"},
                {"input": (bio_name, "co2"), "amount": 0.005, "type": "biosphere"},
            ],
        },
        # Aluminum Packaging Supply Chain
        (fg_name, "aluminum_ingot"): {
            "name": "Primary Aluminum production",
            "unit": "kilogram",
            "type": "process",
            "exchanges": [
                {"input": (fg_name, "aluminum_ingot"), "amount": 1.0, "type": "production"},
                {"input": (fg_name, "electricity_grid"), "amount": 12.0, "type": "technosphere"},
                {"input": (bio_name, "co2"), "amount": 3.2, "type": "biosphere"},
                {"input": (bio_name, "water_use"), "amount": 0.15, "type": "biosphere"},
            ],
        },
        (fg_name, "recycled_aluminum"): {
            "name": "Secondary Recycled Aluminum production",
            "unit": "kilogram",
            "type": "process",
            "exchanges": [
                {"input": (fg_name, "recycled_aluminum"), "amount": 1.0, "type": "production"},
                {"input": (fg_name, "electricity_grid"), "amount": 0.8, "type": "technosphere"},
                {"input": (bio_name, "co2"), "amount": 0.3, "type": "biosphere"},
                {"input": (bio_name, "water_use"), "amount": 0.01, "type": "biosphere"},
            ],
        },
        (fg_name, "aluminum_can_manufacturing"): {
            "name": "Aluminum can stamping & delivery",
            "unit": "unit",
            "type": "process",
            "exchanges": [
                {"input": (fg_name, "aluminum_can_manufacturing"), "amount": 1.0, "type": "production"},
                {"input": (fg_name, "aluminum_ingot"), "amount": 0.015 * 0.25, "type": "technosphere"},
                {"input": (fg_name, "recycled_aluminum"), "amount": 0.015 * 0.75, "type": "technosphere"},
                {"input": (fg_name, "electricity_grid"), "amount": 0.05, "type": "technosphere"},
                {"input": (fg_name, "transport_freight"), "amount": 0.015 * 100 / 1000, "type": "technosphere"},
                {"input": (bio_name, "co2"), "amount": 0.002, "type": "biosphere"},
            ],
        },
    }

    fg_db.write(fg_data)
    return fg_db
