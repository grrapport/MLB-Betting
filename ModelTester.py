import csv
import Five38MLBData
import jsonpickle
import datetime
import GameOdds
import BetHandler
import time

prediction_data = []
with open('mlb_elo_2018.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            #print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            prediction_data.append(Five38MLBData.Five38MlbDataPoint(row))

with open('mlb2018endinglines.json') as lines:
    betting_odds = jsonpickle.decode(lines.read())

bankroll = 10000.00
for odd in betting_odds:
    time.sleep(1)
    game_match = None
    bet_obj = None
    if bankroll <= 0:
        break
    odd_date = datetime.datetime.strptime(odd.date, '%d %b  %Y').date()
    for game in prediction_data:
        if datetime.datetime.strptime(game.date, '%m/%d/%y').date() == odd_date and GameOdds.convert_team_to_five38name(odd.home_team) == game.home_team:
            game_match = game
            break
    if game_match is None:
        continue
    if float(game_match.rating_prob1) > odd.home_team_imp_prob:
        prob_diff = float(game_match.rating_prob1) - odd.home_team_imp_prob
        amount = prob_diff*bankroll
        bet_obj = BetHandler.MoneylineBet(odd, amount, True, game_match.score1, game_match.score2)
        bet_obj.output()
        print("Perceived edge is "+str(prob_diff*100)+"%")
        bankroll += bet_obj.outcome()
        print("Bankroll is now "+str(bankroll))
        continue
    if float(game_match.rating_prob2) > odd.away_team_imp_prob:
        prob_diff = float(game_match.rating_prob2) - odd.away_team_imp_prob
        amount = prob_diff*bankroll
        bet_obj = BetHandler.MoneylineBet(odd, amount, False, game_match.score1, game_match.score2)
        bet_obj.output()
        print("Perceived edge is "+str(prob_diff*100)+"%")
        bankroll += bet_obj.outcome()
        print("Bankroll is now " + str(bankroll))
        continue
print(str(bankroll))
