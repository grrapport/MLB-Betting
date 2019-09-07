from selenium import webdriver
import bs4
from selenium.webdriver.chrome.options import Options


class GameOdds:
    def __init__(self, odds_row):
        self.html = str(odds_row)
        self.date = ""
        self.home_team = ""
        self.away_team = ""
        self.home_team_current_odds_avg = 0
        self.away_team_current_odds_avg = 0
        self.home_team_opening_odds_avg = 0
        self.away_team_opening_odds_avg = 0
        self.home_team_imp_prob_current = 0
        self.away_team_imp_prob_current = 0
        self.odds_by_bookmaker = []
        soup = bs4.BeautifulSoup(self.html)
        self.game_href = soup.find(href=True)['href']
        self.base_url = "https://www.oddsportal.com"
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--window-size=1920x1080")
        self.driver = webdriver.Chrome(options=self.chrome_options, executable_path='./chromedriver')
        self.driver.get(self.base_url + self.game_href)
        self.driver.get("https://www.oddsportal.com/set-timezone/11/")
        self.driver.get(self.base_url + self.game_href)
        self.get_team_current_odds_avg()
        self.get_teams_and_date()
        self.get_odds_by_bookmaker()
        self.get_opening_odds_avg()
        delattr(self, 'html')
        delattr(self, 'chrome_options')
        delattr(self, 'driver')

    def get_team_current_odds_avg(self):
        first_odd_index = self.html.find("odds_text")
        odds_only = self.html[first_odd_index:]
        self.home_team_current_odds_avg = int(odds_only[11:odds_only.find("</a>")])
        second_odd_index = odds_only[1:].find("odds_text")
        odds_only2 = odds_only[second_odd_index + 1:]
        self.away_team_current_odds_avg = int(odds_only2[11:odds_only2.find("</a>")])
        self.home_team_imp_prob_current = odds_to_imp_prob(self.home_team_current_odds_avg)
        self.away_team_imp_prob_current = odds_to_imp_prob(self.away_team_current_odds_avg)

    def get_teams_and_date(self):
        game_html = self.driver.page_source
        new_soup = bs4.BeautifulSoup(game_html)
        teams = new_soup.find('h1').text.split("-")
        self.home_team = teams[0].replace("-", "").strip()
        self.away_team = teams[1].replace("-", "").strip()
        date_loc = game_html.find("date")
        date_general_string = game_html[date_loc:date_loc+60]
        date_untrimmed = date_general_string[date_general_string.find(">")+1:date_general_string.find("</p>")].split(",")
        self.date = date_untrimmed[1].replace(",", "").strip()

    def get_odds_by_bookmaker(self):
        table_rows = []
        table_rows += self.driver.find_elements_by_class_name("lo")
        actions = webdriver.ActionChains(self.driver)
        for row in table_rows:
            try:
                actions.move_to_element(row)
                actions.perform()
                book_name = row.find_element_by_class_name("name").text
                odd_columns = row.find_elements_by_class_name("right")
                home_odd_current = float(odd_columns[0].text)
                actions.move_to_element(odd_columns[0])
                actions.perform()
                tool_tip_text_home = self.driver.find_element_by_id("tooltipdiv").text
                if tool_tip_text_home.startswith("Opening"):
                    current_odd_time = self.date
                    home_odd_opening = float(tool_tip_text_home.split(":")[2].split(" ")[1])
                else:
                    current_odd_time = " ".join(tool_tip_text_home.split(" ")[0:3])
                    home_odd_opening = float(tool_tip_text_home.split(":")[3].split(" ")[1])
                away_odd_current = float(odd_columns[1].text)
                actions.move_to_element(odd_columns[1])
                actions.perform()
                tool_tip_text_away = self.driver.find_element_by_id("tooltipdiv").text
                if tool_tip_text_away.startswith("Opening"):
                    away_odd_opening = float(tool_tip_text_away.split(":")[2].split(" ")[1])
                else:
                    away_odd_opening = float(tool_tip_text_away.split(":")[3].split(" ")[1])
                self.odds_by_bookmaker.append(BookmakerOdds(book_name, home_odd_opening, away_odd_opening, current_odd_time, home_odd_current, away_odd_current))
            except Exception as e:
                print("Error Message: " + str(e))
                print(book_name)
                continue

    def get_opening_odds_avg(self):
        num = 0
        home_tot = 0.0
        away_tot = 0.0
        for odd in self.odds_by_bookmaker:
            if odd.opening_home is None or odd.opening_away is None or odd.opening_home == 0.0 or odd.opening_away == 0.0:
                continue
            num += 1
            home_tot += odds_to_imp_prob(odd.opening_home)
            away_tot += odds_to_imp_prob(odd.opening_away)
        self.home_team_opening_odds_avg = imp_prob_to_odds(home_tot/num)
        self.away_team_opening_odds_avg = imp_prob_to_odds(away_tot/num)
        return

    def get_best_opening_odd(self, home):
        best_odd = BookmakerOdds("default", -100000.0, -100000.0, self.date, -100000.0, -100000.0)
        if home:
            for odd in self.odds_by_bookmaker:
                if odd.opening_home > best_odd.opening_home:
                    best_odd = odd
        else:
            for odd in self.odds_by_bookmaker:
                if odd.opening_away > best_odd.opening_away:
                    best_odd = odd
        return best_odd

    def get_best_current_odd(self, home):
        best_odd = BookmakerOdds("default", -100000.0, -100000.0, self.date, -100000.0, -100000.0)
        if home:
            for odd in self.odds_by_bookmaker:
                if odd.current_home > best_odd.current_home:
                    best_odd = odd
        else:
            for odd in self.odds_by_bookmaker:
                if odd.current_away > best_odd.current_away:
                    best_odd = odd
        return best_odd

    def get_odd_by_bookmaker(self, book_name):
        for odd in self.odds_by_bookmaker:
            if book_name == odd.bookmaker:
                return odd
        raise Exception("No book with name "+book_name + " for this game")

    def output(self):
        return self.date + "  " + self.home_team + ":" + str(self.home_team_current_odds_avg)+"  Opened at "+str(self.home_team_opening_odds_avg) + "  " + str(self.home_team_imp_prob_current) + "     " + self.away_team + ":" + str(self.away_team_current_odds_avg) + "  " + str(self.away_team_imp_prob_current)+"  opened at: "+str(self.away_team_opening_odds_avg)


class BookmakerOdds:
    def __init__(self, bookmaker, opening_home, opening_away, time_date, current_home, current_away):
        self.bookmaker = bookmaker
        self.opening_home = opening_home
        self.opening_away = opening_away
        self.current_odd_time = time_date
        self.current_home = current_home
        self.current_away = current_away


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


def imp_prob_to_odds(prob):
    decimal_odds = 1.0/float(prob)
    if decimal_odds >= 2.0:
        return (decimal_odds - 1.0)*100
    if decimal_odds < 2.0:
        return -100.0/(decimal_odds - 1.0)


def convert_team_to_five38name(name):
    if name == "Los Angeles Dodgers":
        return "LAD"
    if name == "Boston Red Sox":
        return "BOS"
    if name == "Milwaukee Brewers":
        return "MIL"
    if name == "Houston Astros":
        return "HOU"
    if name == "New York Yankees":
        return "NYY"
    if name == "Atlanta Braves":
        return "ATL"
    if name == "Cleveland Indians":
        return "CLE"
    if name == "Colorado Rockies":
        return "COL"
    if name == "Chicago Cubs":
        return "CHC"
    if name == "Kansas City Royals":
        return "KCR"
    if name == "Seattle Mariners":
        return "SEA"
    if name == "San Diego Padres":
        return "SDP"
    if name == "New York Mets":
        return "NYM"
    if name == "Minnesota Twins":
        return "MIN"
    if name == "Cincinnati Reds":
        return "CIN"
    if name == "Los Angeles Angels":
        return "ANA"
    if name == "San Francisco Giants":
        return "SFG"
    if name == "Philadelphia Phillies":
        return "PHI"
    if name == "Baltimore Orioles":
        return "BAL"
    if name == "Arizona Diamondbacks":
        return "ARI"
    if name == "Chicago White Sox":
        return "CHW"
    if name == "St. Louis Cardinals" or name == "St.Louis Cardinals":
        return "STL"
    if name == "Toronto Blue Jays":
        return "TOR"
    if name == "Washington Nationals":
        return "WSN"
    if name == "Oakland Athletics":
        return "OAK"
    if name == "Texas Rangers":
        return "TEX"
    if name == "Pittsburgh Pirates":
        return "PIT"
    if name == "Miami Marlins" or name == "Florida Marlins":
        return "FLA"
    if name == "Detroit Tigers":
        return "DET"
    if name == "Tampa Bay Rays":
        return "TBD"
    else:
        print("No name match found for "+name)
        return ""


