import GameOdds


class MoneylineBet:
    def __init__(self, game_odds, bet_size, home, home_score, away_score):
        self.odds_obj = game_odds
        self.bet = bet_size
        self.home_score = home_score
        self.away_score = away_score
        self.home = home
        if self.home:
            self.team = self.odds_obj.home_team
            self.odds = self.odds_obj.home_team_odds
            self.odds_decimal = convert_odds_to_decimal(self.odds)
        else:
            self.team = self.odds_obj.away_team
            self.odds = self.odds_obj.away_team_odds
            self.odds_decimal = convert_odds_to_decimal(self.odds)

    def outcome(self):
        amount = float(self.bet)*self.odds_decimal
        if self.home_score == self.away_score:
            print("Game was a tie, no action")
            return 0.0
        if self.home:
            if self.home_score > self.away_score:
                print("Bet wins "+str(amount))
                return amount
            else:
                print("Bet loses " + str(self.bet))
                return -float(self.bet)
        else:
            if self.away_score > self.home_score:
                print("Bet wins "+str(amount))
                return amount
            else:
                print("Bet loses "+str(self.bet))
                return -float(self.bet)

    def output(self):
        print(self.odds_obj.date+": Bet "+str(self.bet)+" on "+self.team+" at odds of "+str(self.odds))


def convert_odds_to_decimal(odds):
    if odds > 0:
        return 1.0 + (odds/100)
    if odds < 0:
        return 1.0 + (100/odds)
    raise Exception("Cannot convert odds value: " + str(odds) + "to decimal odds")

