import csv
import Five38MLBData
import jsonpickle
import datetime
import GameOdds
import BetHandler
import time


def get_kelly_criterion(prob, win_rate):
    return prob - ((1-prob)/win_rate)


prediction_data = []
with open('mlb_elo.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            #print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            prediction_data.append(Five38MLBData.Five38MlbDataPoint(row))

with open('mlb2016endinglines.json') as lines:
    betting_odds2016 = jsonpickle.decode(lines.read())

betting_odds2016.reverse()

with open('mlb2017endinglines.json') as lines:
    betting_odds2017 = jsonpickle.decode(lines.read())

betting_odds2017.reverse()

with open('mlb2018endinglines.json') as lines:
    betting_odds2018 = jsonpickle.decode(lines.read())

betting_odds2018.reverse()

betting_odds = betting_odds2016 + betting_odds2017 + betting_odds2018

bankroll = 500.00
goal_adv = 0.035
total_bets = 0
total_wagered = 0.0
sharp_money = 0.0
sharp_bets = 0
won_bets = 0
profit_expectation_percent = 0.0
profit_expectation = 0.0

for odd in betting_odds:
    #time.sleep(1)
    game_match = None
    bet_obj = None
    if bankroll <= 0:
        break
    odd_date = datetime.datetime.strptime(odd.date, '%d %b  %Y').date()
    for game in prediction_data:
        if datetime.datetime.strptime(game.date, '%Y-%m-%d').date() == odd_date and GameOdds.convert_team_to_five38name(odd.home_team) == game.home_team:
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
            best_opening_odd = odd.get_best_opening_odd(True)
            opening_decimal = BetHandler.convert_odds_to_decimal(odd.get_best_opening_odd(True).opening_home)
            current_decimal = BetHandler.convert_odds_to_decimal(odd.get_best_current_odd(True).current_home)
            if best_opening_odd.opening_home > 250:
                # there are some weirdly high values in the opening odds sometimes, this filters them out
                continue
            kelly = get_kelly_criterion(float(game_match.rating_prob1), (opening_decimal-1))
            if kelly < 0:
                continue
            print("Kelly Criterion: "+str(kelly))
            amount = kelly * bankroll
            total_wagered += amount
            bet_obj = BetHandler.MoneylineBet(best_opening_odd.opening_home, amount, True, game_match.score1, game_match.score2)
            if game_match.score1 > game_match.score2:
                won_bets += 1
            print("Betting on "+odd.home_team+" on "+odd.date+" at "+best_opening_odd.bookmaker)
            bet_obj.output()
            print("Perceived edge is " + str(prob_diff * 100) + "%")
            bankroll += bet_obj.outcome()
            print("Bankroll is now " + str(bankroll))
            total_bets += 1
            line_edge = (opening_decimal / current_decimal) - 1
            print("Profit Expectation: "+str(line_edge))
            profit_expectation_percent += line_edge
            profit_expectation += line_edge * amount

            if opening_decimal > current_decimal:
                sharp_bets += 1
                sharp_money += amount
            print("")
            continue
    else:
        if away_adv > goal_adv:
            prob_diff = float(game_match.rating_prob2) - opening_away_imp_prob
            best_opening_odd = odd.get_best_opening_odd(False)
            opening_decimal = BetHandler.convert_odds_to_decimal(odd.get_best_opening_odd(False).opening_away)
            current_decimal = BetHandler.convert_odds_to_decimal(odd.get_best_current_odd(False).current_away)
            if best_opening_odd.opening_away > 250:
                # there are some weirdly high values in the opening odds sometimes, this filters them out
                continue
            kelly = get_kelly_criterion(float(game_match.rating_prob2), (opening_decimal-1))
            if kelly < 0:
                continue
            print("Kelly Criterion: " + str(kelly))
            amount = kelly * bankroll
            total_wagered += amount
            bet_obj = BetHandler.MoneylineBet(best_opening_odd.opening_away, amount, False, game_match.score1, game_match.score2)
            print("Betting on " + odd.away_team + " on " + odd.date+" at "+best_opening_odd.bookmaker)
            if game_match.score2 > game_match.score1:
                won_bets += 1
            bet_obj.output()
            print("Perceived edge is " + str(prob_diff * 100) + "%")
            bankroll += bet_obj.outcome()
            print("Bankroll is now " + str(bankroll))
            total_bets += 1
            line_edge = (opening_decimal / current_decimal) - 1
            print("Profit Expectation: " + str(line_edge))
            profit_expectation_percent += line_edge
            profit_expectation += line_edge * amount
            if opening_decimal > current_decimal:
                sharp_bets += 1
                sharp_money += amount
            print("")
            continue

print("")
print("*****************************************************")
print("Minimum Advantage is: "+str(goal_adv))
print("Ending bankroll: "+str(bankroll))
print("Total bets placed: "+str(total_bets))
print("Total amount wagered: "+str(total_wagered))
print("Percentage of bets won: "+str(100*(won_bets/total_bets))+"%")
print("Percentage of sharp bets: "+str(100*(sharp_bets/total_bets))+"%")
print("Average Profit Expectation Percentage per bet: "+str(100*(profit_expectation_percent/total_bets)))
print("Total profit expectation: "+str(profit_expectation))
print("Percentage of sharp money: "+str(100*(sharp_money/total_wagered))+"%")




