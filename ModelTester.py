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

betting_odds.reverse()

bankroll = 10000.00
goal_adv = 0.0
total_bets = 0
total_wagered = 0
sharp_money = 0
sharp_bets = 0
won_bets = 0
for odd in betting_odds:
    #time.sleep(1)
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
    opening_home_imp_prob = GameOdds.odds_to_imp_prob(odd.get_best_opening_odd(True).opening_home)
    opening_away_imp_prob = GameOdds.odds_to_imp_prob(odd.get_best_opening_odd(False).opening_away)
    home_adv = float(game_match.rating_prob1) - opening_home_imp_prob
    away_adv = float(game_match.rating_prob2) - opening_away_imp_prob
    if home_adv > away_adv:
        if home_adv > goal_adv:
            prob_diff = float(game_match.rating_prob1) - opening_home_imp_prob
            amount = prob_diff * bankroll
            total_wagered += amount
            best_opening_odd = odd.get_best_opening_odd(True)
            bet_obj = BetHandler.MoneylineBet(best_opening_odd.opening_home, amount, True, game_match.score1, game_match.score2)
            if game_match.score1 > game_match.score2:
                won_bets += 1
            print("Betting on "+odd.home_team+" on "+odd.date+" at "+best_opening_odd.bookmaker)
            bet_obj.output()
            print("Perceived edge is " + str(prob_diff * 100) + "%")
            bankroll += bet_obj.outcome()
            print("Bankroll is now " + str(bankroll))
            total_bets += 1
            if odd.get_best_opening_odd(True).opening_home > odd.get_best_current_odd(True).current_home:
                sharp_bets += 1
                sharp_money += amount
            print("")
            continue
    else:
        if away_adv > goal_adv:
            prob_diff = float(game_match.rating_prob2) - opening_away_imp_prob
            amount = prob_diff * bankroll
            total_wagered += amount
            best_opening_odd = odd.get_best_opening_odd(False)
            bet_obj = BetHandler.MoneylineBet(best_opening_odd.opening_away, amount, False, game_match.score1, game_match.score2)
            print("Betting on " + odd.away_team + " on " + odd.date+" at "+best_opening_odd.bookmaker)
            if game_match.score2 > game_match.score1:
                won_bets += 1
            bet_obj.output()
            print("Perceived edge is " + str(prob_diff * 100) + "%")
            bankroll += bet_obj.outcome()
            print("Bankroll is now " + str(bankroll))
            total_bets += 1
            if odd.get_best_opening_odd(False).opening_away > odd.get_best_current_odd(False).current_away:
                sharp_bets += 1
                sharp_money += amount
            print("")
            continue

    # if float(game_match.rating_prob1) - odd.home_team_imp_prob > 0.12:
    #     prob_diff = float(game_match.rating_prob1) - odd.home_team_imp_prob
    #     amount = prob_diff*bankroll
    #     bet_obj = BetHandler.MoneylineBet(odd, amount, True, game_match.score1, game_match.score2)
    #     bet_obj.output()
    #     print("Perceived edge is "+str(prob_diff*100)+"%")
    #     bankroll += bet_obj.outcome()
    #     print("Bankroll is now "+str(bankroll))
    #     continue
    # if float(game_match.rating_prob2) - odd.away_team_imp_prob > 0.12:
    #     prob_diff = float(game_match.rating_prob2) - odd.away_team_imp_prob
    #     amount = prob_diff*bankroll
    #     bet_obj = BetHandler.MoneylineBet(odd, amount, False, game_match.score1, game_match.score2)
    #     bet_obj.output()
    #     print("Perceived edge is "+str(prob_diff*100)+"%")
    #     bankroll += bet_obj.outcome()
    #     print("Bankroll is now " + str(bankroll))
    #     continue
print("")
print("*****************************************************")
print("Ending bankroll: "+str(bankroll))
print("Total bets placed: "+str(total_bets))
print("Percentage of bets won: "+str(100*(won_bets/total_bets))+"%")
print("Percentage of sharp bets: "+str(100*(sharp_bets/total_bets))+"%")
print("Total amount wagered: "+str(total_wagered))
print("Percentage of sharp money: "+str(100*(sharp_money/total_wagered))+"%")


