# MLB-Betting
# Getting started:
After pulling the repo, you will need to download the chromedriver for the version of Chrome that is running on your computer. You should be able to download this from google. Place is at the root directory of the project. It's already in the git.ignore, so no worries there. 

FiveThirtyEight Data is available at https://github.com/fivethirtyeight/data/tree/master/mlb-elo and you need the mlb_elo.csv for ModelTester.py and mlb_elo_latest.csv for GetTargetLines.py.

Python 3.7 is required for this project.
The following packages are dependencies for this project, and can be installed with pip:
  * BeautifulSoup4
  * Selenium
  * jsonpickle
  * Any of the dependencies of the above apps (I can't remember them)

# What does what?
TestScraper.py - scraps odds off oddsportal, runs on whatever season you specify in the script. saves a json of GameOdds using jsonpickle, which you can rehydrate later

ModelTester.py - simulates the outcome of your bets and games. Right now it just runs off the fivethirtyeight.com prediction model

GetTargetLines.py - Gets the lines you should be looking for to bet for the next days slate of games. You can change the advantage you're looking by editing the script. I recommend 7.5% for optimizing sharpness on the lines, but really, you will bet on around 2.5% of games using that strategy. You can go as low as 5% and be sharp, but not as often.

The other .py files in the project are classes that get called from these two files.

# Nomenclature, Variable Styling, and Design Decisions in project
* The argument "home" is used throughout. It needs to be boolean, where True means the home team is being selected, and false denotes the away team
* Variables named or containing odds should be assumed to be in the American odds style, unless otherwise specified in the code. There are functions to convert the odds to implied probability in GameOdds.py and decimal (European) odds in BetHandler.py. American odds are messy programatically, and I don't like them for that, but that's how my mind works regarding actual betting.
* Dates are generally stored as a string until they need to be compared. This is a product of laziness, and there is an open issue about it. I would suggest not assuming that anything is a DateTime type without checking or parsing it into one.
* In both the fivethirtyeight data and old OddsPortal, the first team listed is the Home Team. I know this is garbage, but that's how it is. Literally nowhere else is the home team first. I save them by name (home_team and away_team) in the GameOdds class, but because those are the long names, and fivethirtyeight uses short names, I have a conversion function in GameOdds.py
