import bs4
import GameOdds
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import jsonpickle

url_base = "https://www.oddsportal.com/baseball/usa/mlb-2014/results/#/page/"
#url_base = "https://www.oddsportal.com/baseball/usa/mlb/results/#/page/"
list_game_odds = []
for x in range(1, 50):
    try:
        url = url_base+str(x)+"/"
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        driver = webdriver.Chrome(options=chrome_options, executable_path='./chromedriver')
        driver.implicitly_wait(5)
        driver.get(url)
        driver.get("https://www.oddsportal.com/set-timezone/11/")
        driver.get(url)
        html = driver.page_source
        driver.close()
        soup = bs4.BeautifulSoup(html)
        allTR = soup.findAll("tr", {"class": "deactivate"})
        for tr in allTR:
            if tr.find("odds_text") != "none":
                try:
                    temp = GameOdds.GameOdds(tr)
                    list_game_odds.append(temp)
                    print(temp.output())
                except Exception as e:
                    print("Issue executing on url: " + url)
                    print("Error Message: " + str(e))
                    continue
    except Exception as e:
        print("Issue executing on url: "+url)
        print("Error Message: "+str(e))
        break

f = open("mlb2014endinglines.json", "w+")
f.write(jsonpickle.encode(list_game_odds))
f.close()
