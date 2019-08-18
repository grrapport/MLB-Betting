import Five38MLBData
import csv
import datetime
import GameOdds
import requests

five38_url = "https://projects.fivethirtyeight.com/mlb-api/mlb_elo_latest.csv"

five38_response = requests.get(five38_url)

prediction_data = []
target_adv = 0.075
tomorrow = datetime.date.today() + datetime.timedelta(days=1)
with open('mlb_elo_latest.csv', 'wb') as file:
    file.write(five38_response.content)


with open('mlb_elo_latest.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            #print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            prediction_data.append(Five38MLBData.Five38MlbDataPoint(row))
print("Target Lines for "+str(tomorrow))
print("Advantage: "+str(target_adv*100)+"%")
print("*********************************************")
print("")

for prediction in prediction_data:
    if datetime.datetime.strptime(prediction.date, '%Y-%m-%d').date() != tomorrow:
        continue
    home_target_line = GameOdds.imp_prob_to_odds(float(prediction.rating_prob1) - target_adv)
    away_target_line = GameOdds.imp_prob_to_odds(float(prediction.rating_prob2) - target_adv)
    print(prediction.home_team+"  "+ str(home_target_line)+"              "+prediction.away_team+"  "+str(away_target_line))