import datetime


class BmMlbGame:
    def __init__(self, xml):
        self.game_id = xml.attrib['idgm']
        self.date = datetime.datetime.strptime(xml.attrib['gmdt'], '%Y%m%d').date()
        self.home_team = xml.attrib['htm']
        self.away_team = xml.attrib['vtm']
        self.home_odds = int(xml[0].attrib['hoddst'])
        self.away_odds = int(xml[0].attrib['voddst'])
