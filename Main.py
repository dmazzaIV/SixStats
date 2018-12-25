import shelve
import os
from Player import Player

#Global Variables
login_info = {}
user_links = {}
#favorite players will be scraped on launch so that you can call these players stats without waiting early on
favorite_players = {}

#dictionary of players that have already been scraped this session
#this should save time if the same person is called more than once
scraped_players = {}

def main():
    pullUserDataFromShelf()
    displayPlayerStats('joe')

def pullUserDataFromShelf():
    if os.path.isfile('User_Info.dat'):
        user_info = shelve.open('User_Info')
        login_info['email'] =  user_info['login_info']['email']
        login_info['pwd'] =   user_info['login_info']['pwd']
        copyDictFromShelf()
        user_info.close()
    else:
        runFirstTimeWelcome()
        user_info = shelve.open('User_Info', writeback = True)
        user_email = input('Ubisoft account email: ')
        user_pwd = input('Ubisoft account password: ')
        user_info['login_info'] = {'email' : user_email, 'pwd' : user_pwd}
        user_info['user_links'] = {}
        
        login_info['email'] =  user_info['login_info']['email']
        login_info['pwd'] =   user_info['login_info']['pwd']
        user_info.close()

#first time set up/ welcome message 
def runFirstTimeWelcome():
	print('Welcome to Rainbow Six Compare, an easy way to see who among your friends is truly the best at Rainbow Six Siege')
	print('You will need to input your Ubisoft email and password so that the program can fetch stats from Rainbow Six Siege Stats')
	print('(Don\'t worry they get saved locally on your machine they won\'t get leaked)')

#copy the user links from the shelf into the user_links dictionary
def copyDictFromShelf():
    user_info = shelve.open('User_Info')
    for key in user_info['user_links']:
        user_links[key] = user_info['user_links'][key]
    user_info.close()

#list the names of all players in the user_links dictionary
def listPlayers():
    for key in user_links:
        print(key)

#list the names of all players in the favorites dictionary
def listFavorites():
    for key in favorite_players:
        print(key)

#add a player to the user_links dictionary
def addPlayerURL():
    user_info = shelve.open('User_Info', writeback = True)
    #The name will be made all uppercase in the end as to avoid confusion when searching for a name
    player_name = input('Enter a name for the new player(NOT CASE SENSITIVE): ')
    player_url = input('Copy and paste the player\'s url here (search for their Ubisfot username \nand copy the FULL url from this site https://game-rainbow6.ubi.com/en-us/home): ')

    #add player URL and name to shelf and session dictionary
    if player_name.upper() in user_links:
        print(player_name + ' is already in your list of players, make sure you are not adding a duplicate or try another name')
    else:
        user_info['user_links'][player_name.upper()] = player_url
        user_links[player_name.upper()] = player_url
    user_info.close()

#desiplays the general player stats
def displayPlayerStats(name):
    if name.upper() in scraped_players:
        player = scraped_players[name.upper()]
    elif name.upper() not in scraped_players and name.upper() in user_links:
        player = Player(user_links[name.upper()], login_info)
    else:
        print(name.upper() + 'is not saved in your list of players')
        return None

    print('Rank: ' + str(player.getPlayerRank()))
    print('Time Played: ' + (player.getPlayerTimePlayed()))
    print('K/D: ' + str(player.getPlayerKillDeath()))
    print('W/L: ' + str(player.getPlayerWinLoss()))
    print('Headshot %: ' + str(player.getPlayerHeadshotPercentage()))

main()
