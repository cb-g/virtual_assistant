import json

class template:
    def __init__(self,
                 directory: str = "src/RAS/data/",
                 filename: str = "template.json",
                 ):
        self.directory = directory
        self.filename = filename

        # define how many days to wait (at least and at most) before doing the activity again. 
        self.template = {
            "activity A": {
                  "min: int": 1,
                  "max: int": 5,
                  },
            "activity B": {
                  "min: int": 2,
                  "max: int": 4,
                  },
            "activity C": {
                  "min: int": 2,
                  "max: int": 10,
                  },
            "activity D": {
                  "min: int": 3,
                  "max: int": 7,
                  },
            "activity E": {
                  "min: int": 1,
                  "max: int": 12,
                  },
            "activity F": {
                  "min: int": 1,
                  "max: int": 2,
                  },
            "activity G": {
                  "min: int": 5,
                  "max: int": 9,
                  },
            "activity H": {
                  "min: int": 6,
                  "max: int": 14,
                  },
            "activity I": {
                  "min: int": 14,
                  "max: int": 21,
                  },
        }

        keys_to_add = [
            "min: int", "min: date",
            "max: int", "max: date",
            "last: int", "last: date",
            "rest: int", "rest: date",
            "due: int", "due: date",
            "overdue: int", "overdue: date"
            ]

        # adding keys_to_add to each activity:
        self.template = {k: v.update({key: "" for key in keys_to_add if key not in v}) or v for k, v in self.template.items()}

    def create(self):
        with open(self.directory + self.filename, "w") as f:
            json.dump(self.template, f)
