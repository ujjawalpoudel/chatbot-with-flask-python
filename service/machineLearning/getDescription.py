import csv


def get_description(disease):
    description_dict = {}
    try:
        with open("MasterData/symptom_Description.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            line_count = 0
            for row in csv_reader:
                _description = {row[0]: row[1]}
                description_dict.update(_description)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None

    try:
        description = description_dict[disease]
    except KeyError:
        print(f"No description found for {disease}")
        return None

    return description
