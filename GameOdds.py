from selenium import webdriver
import bs4
from selenium.webdriver.chrome.options import Options


class GameOdds:
    def __init__(self, odds_row):
        self.html = str(odds_row)
        self.date = ""
        self.home_team = ""
        self.away_team = ""
        self.home_team_odds = 0
        self.away_team_odds = 0
        self.home_team_imp_prob = 0
        self.away_team_imp_prob = 0
        self.get_team_odds()
        self.get_teams_and_date()
        delattr(self, 'html')

    def get_team_odds(self):
        first_odd_index = self.html.find("odds_text")
        odds_only = self.html[first_odd_index:]
        self.home_team_odds = int(odds_only[11:odds_only.find("</a>")])
        second_odd_index = odds_only[1:].find("odds_text")
        odds_only2 = odds_only[second_odd_index + 1:]
        self.away_team_odds = int(odds_only2[11:odds_only2.find("</a>")])
        self.home_team_imp_prob = odds_to_imp_prob(self.home_team_odds)
        self.away_team_imp_prob = odds_to_imp_prob(self.away_team_odds)

    def get_teams_and_date(self):
        soup = bs4.BeautifulSoup(self.html)
        game_href = soup.find(href=True)['href']
        base_url = "https://www.oddsportal.com"
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        driver = webdriver.Chrome(options=chrome_options, executable_path='./chromedriver')
        driver.get(base_url+game_href)
        game_html = driver.page_source
        driver.close()
        new_soup = bs4.BeautifulSoup(game_html)
        teams = new_soup.find('h1').text.split("-")
        self.home_team = teams[0].replace("-", "").strip()
        self.away_team = teams[1].replace("-", "").strip()
        date_loc = game_html.find("date")
        date_general_string = game_html[date_loc:date_loc+60]
        date_untrimmed = date_general_string[date_general_string.find(">")+1:date_general_string.find("</p>")].split(",")
        self.date = date_untrimmed[1].replace(",", "").strip()

    def output(self):
        return self.date+"  "+self.home_team+":"+str(self.home_team_odds)+"  "+str(self.home_team_imp_prob)+"     "+self.away_team+":"+str(self.away_team_odds)+"  "+str(self.away_team_imp_prob)


def odds_to_imp_prob(odds):
    try:
        odds = float(odds)
    except Exception as e:
        print("Issue converting odds to double on odds value: " + str(odds))
        print("Error Message: " + str(e))
        return ""
    if odds < 0:
        return abs(odds)/(abs(odds)+100.0)
    if odds > 0:
        return 100.0/(odds+100.0)
    raise Exception("Cannot cover odds value: "+str(odds)+"to implied probability")
    return ""
