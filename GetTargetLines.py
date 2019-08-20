import Five38MLBData
import csv
import datetime
import GameOdds
import requests
import xml.etree.ElementTree as ET
import BookMakerData
import BetHandler


def get_kelly_criterion(prob, win_rate):
    return prob - ((1-prob)/win_rate)


def get_bookmaker_odds(response):
    root = ET.fromstring(response)
    games = []
    for child in root.findall("./Leagues/league"):
        if child.attrib['IdLeague'] == "5":
            mlb_elem = child
            break

    for child in mlb_elem.findall("./game"):
        try:
            games.append(BookMakerData.BmMlbGame(child))
        except Exception as e:
            print(e)
            continue
    return games


five38_url = "https://projects.fivethirtyeight.com/mlb-api/mlb_elo_latest.csv"
bookmaker_url = "http://lines.bookmaker.eu/"

prediction_data = []
available_lines = []
bets_to_make = []

target_adv = 0.035
tomorrow = datetime.date.today() + datetime.timedelta(days=1)

five38_response = requests.get(five38_url)
with open('mlb_elo_latest.csv', 'wb') as file:
    file.write(five38_response.content)


with open('mlb_elo_latest.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            prediction_data.append(Five38MLBData.Five38MlbDataPoint(row))

bookmaker_response = requests.get(bookmaker_url)
available_lines = get_bookmaker_odds(bookmaker_response.content)


for line in available_lines:
    game_match = None
    for game in prediction_data:
        if datetime.datetime.strptime(game.date, '%Y-%m-%d').date() == line.date and GameOdds.convert_team_to_five38name(line.home_team) == game.home_team:
            game_match = game
            break
    if game_match is None:
        continue
    home_imp_prob = GameOdds.odds_to_imp_prob(line.home_odds)
    away_imp_prob = GameOdds.odds_to_imp_prob(line.away_odds)
    home_adv = float(game_match.rating_prob1) - home_imp_prob
    away_adv = float(game_match.rating_prob2) - away_imp_prob

    if home_adv > away_adv:
        if home_adv < target_adv:
            continue
        prob_diff = float(game_match.rating_prob1) - home_imp_prob
        decimal_odds = BetHandler.convert_odds_to_decimal(line.home_odds)
        kelly = get_kelly_criterion(float(game_match.rating_prob1), (decimal_odds - 1))
        if kelly < 0:
            continue
        bet_to_make = BetHandler.BetToMake(line.game_id, line.date, line.home_team, line.away_team, True, line.home_odds, line.away_odds, kelly, home_adv)
        bets_to_make.append(bet_to_make)
    else:
        if away_adv < target_adv:
            continue
        prob_diff = float(game_match.rating_prob2) - away_imp_prob
        decimal_odds = BetHandler.convert_odds_to_decimal(line.away_odds)
        kelly = get_kelly_criterion(float(game_match.rating_prob2), (decimal_odds - 1))
        if kelly < 0:
            continue
        bet_to_make = BetHandler.BetToMake(line.game_id, line.date, line.home_team, line.away_team, False, line.home_odds, line.away_odds, kelly, away_adv)
        bets_to_make.append(bet_to_make)

sort_bets = sorted(bets_to_make, reverse=True)
for bet in sort_bets:
    print(bet.output())



# for prediction in prediction_data:
#     if datetime.datetime.strptime(prediction.date, '%Y-%m-%d').date() != tomorrow:
#         continue
#     home_target_line = GameOdds.imp_prob_to_odds(float(prediction.rating_prob1) - target_adv)
#     away_target_line = GameOdds.imp_prob_to_odds(float(prediction.rating_prob2) - target_adv)
#     print(prediction.home_team+"  " + str(home_target_line)+"              "+prediction.away_team+"  "+str(away_target_line))










