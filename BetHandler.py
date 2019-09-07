import GameOdds


class MoneylineBet:
    def __init__(self, game_odds, bet_size, home, home_score, away_score):
        self.odds = game_odds
        self.odds_decimal = convert_odds_to_decimal(self.odds)
        self.bet = bet_size
        self.home_score = home_score
        self.away_score = away_score
        self.home = home

    def outcome(self):
        amount = float(self.bet)*(self.odds_decimal-1)
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
        print("Bet "+str(self.bet)+" at odds of "+str(self.odds))


class BetToMake:
    def __init__(self, idgm, date, home_tm, away_tm, home, hodds, aodds, kelly, perceived_adv):
        self.game_id = idgm
        self.date = date
        self.home_team = home_tm
        self.away_team = away_tm
        self.home = home
        self.home_odds = hodds
        self.away_odds = aodds
        self.kelly_criterion = kelly
        self.perceived_adv = perceived_adv

    def __lt__(self, other):
        return self.perceived_adv < other.perceived_adv

    def __eq__(self, other):
        return self.game_id == other.game_id

    def output(self):
        outstring = ""
        outstring += str(self.date) + "  "
        outstring += self.game_id+"  "
        if self.home:
            outstring += self.home_team+" over "+self.away_team
            outstring += " at "+str(self.home_odds)
        else:
            outstring += self.away_team + " over " + self.home_team
            outstring += " at " + str(self.away_odds)
        outstring += "   Kelly Criterion: "+str(self.kelly_criterion)[0:5]
        outstring += " Perceived Adv = " + str(self.perceived_adv*100)[0:4]+"%"
        return outstring


def convert_odds_to_decimal(odds):
    if odds > 0:
        return 1.0 + (odds/100)
    if odds < 0:
        return 1.0 + (100/abs(odds))
    raise Exception("Cannot convert odds value: " + str(odds) + "to decimal odds")

