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
        if self.home_score == self.away_score:
            return 0.0
        if self.home:
            if self.home_score > self.away_score:
                return float(self.bet)*self.odds_decimal
            else:
                return -float(self.bet)
        else:
            if self.away_score > self.home_score:
                return float(self.bet)*self.odds_decimal
            else:
                return -float(self.bet)


def convert_odds_to_decimal(odds):
    if odds > 0:
        return 1.0 + (odds/100)
    if odds < 0:
        return 1.0 + (100/odds)
    raise Exception("Cannot convert odds value: " + str(odds) + "to decimal odds")

