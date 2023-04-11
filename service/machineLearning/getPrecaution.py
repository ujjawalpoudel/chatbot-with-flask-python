import csv


def get_precaution(disease):
    precaution_dict = {}
    try:
        with open("csv_data/symptom_precaution.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            for row in csv_reader:
                _prec = {row[0]: [row[1], row[2], row[3], row[4]]}
                precaution_dict.update(_prec)
    except FileNotFoundError as e:
        print(f"Error occurred: {str(e)}")
        return None
    try:
        precaution = precaution_dict[disease]
    except KeyError:
        print(f"No precaution found for {disease}")
        return None

    return precaution
