"""

"""

VERTICES_SAMPLES = [
    {
        "label": "Star",
        "properties": {
            "name": "Sun",
            "mass_in_kgs": float(1989000000000000000000000000000),
            "radius_in_kms": 696340
        }
    },
    {
        "label": "Planet",
        "properties": {
            "name": "Earth",
            "mass_in_kgs": float(5972000000000000000000000),
            "radius_in_kms": 6371
        }
    },
    {
        "label": "Planet",
        "properties": {
            "name": "Mars",
            "mass_in_kgs": float(641700000000000000000000),
            "radius_in_kms": 3396
        }
    },
    {
        "label": "Satellite",
        "properties": {
            "name": "Moon",
            "mass_in_kgs": float(73476730900000000000000)
        }
    },
    {
        "label": "Satellite",
        "properties": {
            "name": "Phobos",
            "mean_radius": 11
        }
    }, {
        "label": "Satellite",
        "properties": {
            "name": "Deimos",
            "mean_radius": 6
        }
    }
]

EDGES_SAMPLES = [
    {
        "label": "has_satellite",
        "properties": {
            "distance_in_kms": 384400
        },
        "from_vertex_filters": {
            "has__label": "Planet",
            "has__name": "Earth"
        },
        "to_vertex_filters": {
            "has__label": "Satellite",
            "has__name": "Moon"
        }
    },
    {
        "label": "has_satellite",
        "properties": {
            "distance_in_kms": 6000

        },
        "from_vertex_filters": {
            "has__label": "Planet",
            "has__name": "Mars"
        },
        "to_vertex_filters": {
            "has__label": "Satellite",
            "has__name": "Phobos"
        }
    },
    {
        "label": "has_satellite",
        "properties": {
            "distance_in_kms": 23458
        },
        "from_vertex_filters": {
            "has__label": "Planet",
            "has__name": "Mars"
        },
        "to_vertex_filters": {
            "has__label": "Satellite",
            "has__name": "Deimos"
        }
    },
    {
        "label": "has_planet",
        "properties": {
            "distance_in_kms": float(250000000)
        },
        "from_vertex_filters": {
            "has__label": "Star",
            "has__name": "Sun"
        },
        "to_vertex_filters": {
            "has__label": "Planet",
            "has__name": "Mars"
        }
    },
    {
        "label": "has_planet",
        "properties": {
            "distance_in_kms": float(152000000)
        },
        "from_vertex_filters": {
            "has__label": "Star",
            "has__name": "Sun"
        },
        "to_vertex_filters": {
            "has__label": "Planet",
            "has__name": "Earth"
        }
    },

]
