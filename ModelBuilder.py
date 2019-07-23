import csv
import Five38MLBData

prediction_data = []
with open('mlb_elo_2018.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            prediction_data.append(Five38MLBData.Five38MlbDataPoint(row))
