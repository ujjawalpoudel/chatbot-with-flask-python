import csv


def getSeverityDict():
    with open("csv_data/symptom_severity.csv") as csv_file:
        severityDictionary = {}

        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        try:
            for row in csv_reader:
                _diction = {row[0]: int(row[1])}
                severityDictionary.update(_diction)
        except:
            pass

        return severityDictionary
