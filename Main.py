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
    scrapeFavorites()

    while 1 == 1:
        func = input('Enter a command(type \'help\' for a list of commands, type 0 to exit): ')
        if func == '0':
            break

        command = func.split(' ')
        if len(command) == 1:
            function_dictionary[command[0].upper()]()
        elif len(command) == 2:
            function_dictionary[command[0].upper()](command[1])
        elif len(command) == 3:
            function_dictionary[command[0].upper()](command[1],command[2])
        elif len(command) == 4:
            function_dictionary[command[0].upper()](command[1],command[2],command[3])

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
        user_info['favorite_players'] = {}
        
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
    for key in user_info['favorite_players']:
        favorite_players[key] = user_info['favorite_players'][key]
    user_info.close()

#checks if a player has already been scraped this session
def isAlreadyScraped(name):
    if name.upper() in scraped_players:
        return scraped_players[name.upper()]
    elif name.upper() not in scraped_players and name.upper() in user_links:
        player = Player(user_links[name.upper()], login_info)
        scraped_players[name.upper()] = player
        return player

    else:
        print(name.upper() + 'is not saved in your list of players')
        return None

#list the names of all players in the user_links dictionary
def listPlayers():
    for key in user_links:
        print(key)

#adds player to favorites to be scraped on launch
def addPlayerToFavorites(name):
    if name.upper() in user_links:
        user_info = shelve.open('User_Info', writeback = True)
        favorite_players[name.upper()] = user_links[name.upper()]
        user_info['favorite_players'][name.upper()] = user_links[name.upper()]
        user_info.close()
    else:
        print(name.upper() + ' is not saved in your list of players')

#scrapes the favorites list and stores them in the scraped players dictionary for this session
def scrapeFavorites():
    for key,value in favorite_players.items():
        scraped_players[key] = Player(value, login_info)

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

#displays the general player stats
def displayPlayerStats(name):

    player = isAlreadyScraped(name)

    if player != None:
        print('Rank: ' + player.getPlayerRank())
        print('Time Played: ' + (player.getPlayerTimePlayed()))
        print('K/D: ' + player.getPlayerKillDeath())
        print('W/L: ' + player.getPlayerWinLoss())
        headshot_percent_full = str(player.getPlayerHeadshotPercentage())
        print('Headshot %: ' + headshot_percent_full[2:4] + '%')

def displayOperatorStats(player_name, operator_name):

    player = isAlreadyScraped(player_name)

    if player != None:
        print(player_name.upper() + '\'S ' + operator_name.upper() + ' STATS:')
        print('Time Played: ' + player.getOperatorTimePlayed(operator_name.upper()))
        print('K/D: ' + player.getOperatorKillDeath(operator_name.upper()))
        print('W/L: ' + player.getOperatorWinLoss(operator_name.upper()))

def comparePlayers(player_1_name, player_2_name):
    #load player stats from the dictionary or scrape the players stats if they haven't already been scraped
    player_1 = isAlreadyScraped(player_1_name)
    player_2 = isAlreadyScraped(player_2_name)

    print('\t' +player_1_name.upper() + '\t\t' + player_2_name.upper())
    print('Rank: ' + player_1.getPlayerRank() + '\t' + player_2.getPlayerRank())
    print('Time Played: ' + player_1.getPlayerTimePlayed() + '\t' + player_2.getPlayerTimePlayed())
    print('W/L: \t' + player_1.getPlayerWinLoss() + '\t\t' + player_2.getPlayerWinLoss())
    print('K/D: \t' + player_1.getPlayerKillDeath() + '\t\t' + player_2.getPlayerKillDeath())
    headshot_percent_full_1 = str(player_1.getPlayerHeadshotPercentage())
    headshot_percent_full_2 = str(player_2.getPlayerHeadshotPercentage())
    print('Headshot %: ' + headshot_percent_full_1[2:4] + '% \t' + headshot_percent_full_2[2:4] + '%')
    print('Melee Kills: ' + player_1.getPlayerMeleeKills() + '\t\t' + player_2.getPlayerMeleeKills())

def compareOperators(player_1_name, player_2_name, operator):
    #load player stats from the dictionary or scrape the players stats if they haven't already been scraped
    player_1 = isAlreadyScraped(player_1_name)
    player_2 = isAlreadyScraped(player_2_name)

    print('\t' +player_1_name.upper() + '\t' + player_2_name.upper())
    print('Time Played: ' + player_1.getOperatorTimePlayed(operator.upper()) + '\t' + player_2.getOperatorTimePlayed(operator.upper()))
    print('W/L: ' + player_1.getOperatorWinLoss(operator.upper()) + '\t' + player_2.getOperatorWinLoss(operator.upper()))
    print('K/D: ' + player_1.getOperatorKillDeath(operator.upper()) + '\t' + player_2.getOperatorKillDeath(operator.upper()))

def commandHelp():
    print('Commands and arguments are not case senesitive')
    print('make sure you have spaces between arguments and commands')
    print('Commands:')
    print('ADD_PLAYER \'name\'  -adds a player to your saved list of players to scrape and compare')
    print('ADD_FAVORITE \'name\'  -adds a player to your favorites list, this list will be scraped on launch')
    print('LIST  -lists all players saved and ready to be scraped')
    print('FAVORITES  -lists all players in your favorites list')
    print('DISP_STATS \'player name\'  -displays the general stats for a given player')
    print('OP_STATS \'player name\' \'operator name\'  -displays the operator specific stats for a given player')
    print('COMPARE_OP \'player name\' \'player name\' \'operator name\'  -displays the specific operator stats for two given players side by side')
    print('COMPARE_PLAYERS \'player name\' \'player name\'  -displays the stats for two given players side by side for comparison')


#dictionary of functions to turn user input into function calls
function_dictionary = {  'ADD_PLAYER' : addPlayerURL
                        ,'ADD_FAVORITE' : addPlayerToFavorites
                        ,'LIST' : listPlayers
                        ,'FAVORITES' : listFavorites
                        ,'DISP_STATS' : displayPlayerStats
                        ,'OP_STATS' : displayOperatorStats
                        ,'COMPARE_OP' : compareOperators
                        ,'COMPARE_PLAYERS' : comparePlayers
                        ,'HELP' : commandHelp
                        }

main()
