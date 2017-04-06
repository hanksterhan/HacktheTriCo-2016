import requests, sqlite3  
from bs4 import BeautifulSoup
from urllib2 import urlopen

BASE_URL = "http://www.basketball-reference.com/players/{player_id}/gamelog/2017/"

conn = sqlite3.connect('CarmeloAnthony.db')
c = conn.cursor()

active_players = []
active_players_ids = []

##Creates the table will all the columns we need
##Does not create if the table already exists
##
def create_table():
	#Use all caps for pure sql and lower case for things that aren't
	c.execute('CREATE TABLE IF NOT EXISTS stuffToPlot(game_season TEXT, data_game TEXT, age TEXT, team_id TEXT, game_location TEXT, opp_id TEXT, game_result TEXT, gs TEXT, mp TEXT, fg TEXT, fga TEXT, fg_pct TEXT, fg3 TEXT, fg3a TEXT, fg3_pct TEXT, ft TEXT, fta TEXT, ft_pct TEXT, orb TEXT, drb TEXT, trb TEXT, ast TEXT, stl TEXT, blk TEXT, tov TEXT, pf TEXT, pts TEXT, game_score TEXT, plus_minus TEXT)')

## I don't know if I still need this. 
def dynamic_data_entry():
	#c.executemany("INSERT INTO stuffToPlot (game_season, data_game, age, team_id, game_location, opp_id, game_result, gs, mp, fg, fga, fg_pct, fg3, fg3a, fg3_pct, ft, fta, ft_pct, orb, drb, trb , ast, stl, blk, tov, pf, pts, game_score, plus_minus) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (data2,))
	#variables: game_season, data_game, age, team_id, game_location, opp_id, game_result, gs, mp, fg, fga, fg3, fg3a, fg3_pct, ft, fta, ft_pct, orb, drb, trb , ast, stl, blk, tov, pf, pts, game_score, plus_minus
	conn.commit()

## Given a letter, this function gets all the active players with last names starting with that letter
## The names are stored in active_players and their ids are stored in active_players_id
def get_active_players(letter):
	url = "http://www.basketball-reference.com/players/" + letter
	soup = make_soup(url)
	tbody = soup.find("tbody")

	tr = tbody.find_all("strong")
	for player in tr:
		active_players.append(player.text.encode('utf-8'))
		active_players_ids.append(player.find("a").get("href"))


##parse active_players_ids so that we can insert it into the url 
def extractPlayerIds():
	for i in range(len(active_players_ids)):
		temp = active_players_ids[i]
		active_players_ids[i] = temp[8:(len(temp)-5)]

## Takes all the IDs and writes it into playerIDs.txt
def writePlayerIdstoFile():
	my_file = open("playerIDs.txt", "r+")
	for playerID in active_players_ids:
		my_file.write(str(playerID) + "\n")
	my_file.close()



##helper function to populate an array with an alphabet
##so that we can easily find all the active players
def populateArrayWithAlphabet():
	alphabet = []	
	ascii_code = 97
	for i in range(26):
		alphabet.append(chr(ascii_code) + '/')
		ascii_code += 1
	alphabet.remove('x/')
	return alphabet

##Actually appends to the database
##Need to add columns like player name and payer ID
def get_game_data(playerID):

	playerStats = []
	gameIDs = []

	gameIDs = get_game_IDs(playerID)

	soup = make_soup(BASE_URL.format(player_id = playerID))
	## Figure out this nested for loop
	##First for loop goes vertically and captures each game played in a season
	##Second goes horizontally and captures each stat accumulated in a game
	for gameID in gameIDs:
		tbody = soup.find(id=gameID)
		#Error on this line
		# tbody2 = tbody.findALL("td")
		for td in tbody.findAll("td"):
			#print td.get("data-stat") + ":" + td.text
			playerStats.append(td.text.encode('utf-8'))
		c.executemany("INSERT INTO stuffToPlot (game_season, data_game, age, team_id, game_location, opp_id, game_result, gs, mp, fg, fga, fg_pct, fg3, fg3a, fg3_pct, ft, fta, ft_pct, orb, drb, trb , ast, stl, blk, tov, pf, pts, game_score, plus_minus) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (playerStats,))
		#variables: game_season, data_game, age, team_id, game_location, opp_id, game_result, gs, mp, fg, fga, fg3, fg3a, fg3_pct, ft, fta, ft_pct, orb, drb, trb , ast, stl, blk, tov, pf, pts, game_score, plus_minus
		conn.commit()
	
##helper function
def make_soup(url):
	html = urlopen(url).read()
	return BeautifulSoup(html, "lxml")

##Function to populate an array with all the game IDs for a particular player
##in a particular season
def get_game_IDs(playerID):
	gameIDs = []

	soup = make_soup(BASE_URL.format(player_id = playerID))
	tbody = soup.find_all("tr")
	for tr in tbody:
		gameIDs.append(tr.get("id"))
	#The following gets rid of rows that don't have the appropriate data
	numOfNones = gameIDs.count(None)
	for i in range(0,numOfNones):
		gameIDs.remove(None)
	return gameIDs

def main():
	# create_table()
	# for id in ids:
	# 	get_game_data(id)
	# 	dynamic_data_entry()
	# get_active_players()

	get_game_data("a/aldrila01")

	########################################################
	####        Extracted all the player IDs already    ####
	########################################################
	# alphabet = []
	# alphabet = populateArrayWithAlphabet()
	# for i in range(len(alphabet)):
	# 	get_active_players(alphabet[i])
	# extractPlayerIds()
	# writePlayerIdstoFile()

	# dynamic_data_entry()
	c.close()
	conn.close()

main()

