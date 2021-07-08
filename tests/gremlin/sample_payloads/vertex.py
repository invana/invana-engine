"""

"""

#  Copyright 2020 Invana
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http:www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

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
