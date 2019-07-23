class Five38MlbDataPoint:
    def __init__(self,row):
        #date, season, neutral, playoff, team1, team2, elo1_pre, elo2_pre, elo_prob1, elo_prob2, elo1_post, elo2_post, rating1_pre,
        # rating2_pre, pitcher1, pitcher2, pitcher1_rgs, pitcher2_rgs,
    #       pitcher1_adj, pitcher2_adj, rating_prob1, rating_prob2, rating1_post, rating2_post, score1, score2
        self.date = row[0]
        self.season = row[1]
        self.neutral = row[2]
        self.playoff = row[3]
        self.team1 = row[4]
        self.home_team = row[4]
        self.team2 = row[5]
        self.away_team = row[5]
        self.elo1_pre = row[6]
        self.elo2_pre = row[7]
        self.elo_prob1 = row[8]
        self.elo_prob2 = row[9]
        self.elo1_post = row[10]
        self.elo2_post = row[11]
        self.rating1_pre = row[12]
        self.rating2_pre = row[13]
        self.pitcher1 = row[14]
        self.pitcher2 = row[15]
        self.pitcher1_rgs = row[16]
        self.pitcher2_rgs = row[17]
        self.pitcher1_adj = row[18]
        self.pitcher2_adj = row[19]
        self.rating_prob1 = row[20]
        self.rating_prob2 = row[21]
        self.rating1_post = row[22]
        self.rating2_post = row[23]
        self.score1 = row[24]
        self.score2 = row[25]


