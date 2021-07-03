"""

"""

CREATE_VERTICES_SAMPLES = {
    "planet": {
        "label": "Planet",
        "properties": {
            "name": "Earth",
            "mass_in_kgs": float(5972000000000000000000000),
            "radius_in_kms": 6371
        }
    },
    "satellite": {
        "label": "Satellite",
        "properties": {
            "name": "Moon",
            "mass_in_kgs": int(73476730900000000000000)
        }
    }
}

SAMPLE_DATA = [
                  {
                      "label": "Student",
                      "properties": {
                          "name": "student {}".format(i),
                          "age": i,
                      }
                  } for i in range(12, 50)
              ] + [
                  {
                      "label": "Teacher",
                      "properties": {
                          "name": "teacher {}".format(i),
                          "age": i,
                      }
                  } for i in range(25, 35)
              ]
