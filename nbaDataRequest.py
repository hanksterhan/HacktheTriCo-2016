import base64
import requests
import json
import csv

def send_request():
	try: 
		response = requests.get(
			#url = "https://www.mysportsfeeds.com/api/feed/pull/nba/2016-2017-regular/cumulative_player_stats.csv?playerstats=2PA,2PM,3PA,3PM,FTA,FTM",
			url = "https://www.mysportsfeeds.com/api/feed/pull/nba/2016-2017-regular/daily_player_stats.csv?fordate=20170324&playerstats=2PA,2PM,3PA,3PM,FTA,FTM",
			headers={
				"Authorization": "Basic " + base64.b64encode('hanksterhan' + ":" + '2grr!@rw')
				#"Authorization": b'Basic ' + base64.b64encode(b'hanksterhan:2grr!@rw') 
			}
		)
		print('Response HTTP Status Code: {status_code}'.format(
			status_code=response.status_code))
		#print('Response HTTP Response Body: {content}'.format(
			#content=response.content))

		myFile = open("output.csv", "w")
		for player in response:
			myFile.write(player)
		myFile.close()

	except requests.exceptions.RequestException:
		print 'HTTP Request failed'

def main():
	send_request()

main()