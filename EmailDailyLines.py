import Five38MLBData
import csv
import datetime
import GameOdds
import requests
import smtplib

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
email_text = ""
email_text += "Target Lines for "+str(tomorrow) + "\n"
email_text += "Advantage: "+str(target_adv*100)+"%" + "\n"
email_text += "*********************************************" + "\n"

for prediction in prediction_data:
    if datetime.datetime.strptime(prediction.date, '%Y-%m-%d').date() != tomorrow:
        continue
    home_target_line = GameOdds.imp_prob_to_odds(float(prediction.rating_prob1) - target_adv)
    away_target_line = GameOdds.imp_prob_to_odds(float(prediction.rating_prob2) - target_adv)
    email_text += prediction.home_team+"  " + str(home_target_line)[0:6]+"\n"+prediction.away_team+"  "+str(away_target_line)[0:6] + "\n\n"

server = smtplib.SMTP('smtp.gmail.com', 587)
server.connect('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
# don't worry, this password is here intentionally. Feel free to use this to send messages
# it's an app password, so you can't log in with it
# Please don't abuse it though (google doesn't really care if you send a ton of email, but still)
server.login("actionchase@gmail.com", "lnkyaliduvshwicn")
try:
    server.sendmail("actionchase@gmail.com", "", email_text)
except Exception as e:
    print(e)
