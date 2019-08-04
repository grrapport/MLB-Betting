# MLB-Betting
Getting started:
After pulling the repo, you will need to download the chromedriver for the version of Chrome that is running on your computer. You should be able to download this from google.
Put
The following packages are dependencies for this project, and can be installed with pip:
  * BeautifulSoup4
  * Selenium
  * jsonpickle
  * Any of the dependencies of the above apps (I can't remember them)


TestScraper.py - scraps odds off oddsportal, runs on whatever season you specify in the script. saves a json of GameOdds using jsonpickle, which you can rehydrate later

ModelTester.py - simulates the outcome of your bets and games. Right now it just runs off the fivethirtyeight.com prediction model
