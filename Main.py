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

    while True:
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
    s = ('Welcome to Rainbow Six Compare, an easy way to see who among your friends is truly the best at Rainbow Six Siege\n'
         'You will need to input your Ubisoft email and password so that the program can fetch stats from Rainbow Six Siege Stats\n'
         '(Don\'t worry they get saved locally on your machine they won\'t get leaked)')
    print(s)

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
    #if the name is already in scraped players then the stats are already stored this session and there is no need to make a new player object
    if name in scraped_players:
        return scraped_players[name]
    #if the name is not in the scraped players, but is in the list of player links, that player's stats have not been scraped
    #and we must create a new player object to scrape and store the stats for the player
    elif name not in scraped_players and name in user_links:
        player = Player(user_links[name], login_info)
        scraped_players[name] = player
        return player

    else:
        print('{} is not saved in your list of players'.format(name))
        return None

#list the names of all players in the user_links dictionary
def listPlayers():
    for key in user_links:
        print(key)

#adds player to favorites to be scraped on launch
def addPlayerToFavorites(name):
    name = name.upper()

    if name in user_links:
        user_info = shelve.open('User_Info', writeback = True)
        favorite_players[name] = user_links[name]
        user_info['favorite_players'][name] = user_links[name]
        user_info.close()
    else:
        print('{} is not saved in your list of players'.format(name))

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
    player_name = player_name.upper()

    #add player URL and name to shelf and session dictionary
    if player_name in user_links:
        print('{} is already in your list of players, make sure you are not adding a duplicate or try another name'.format(player_name))
    else:
        user_info['user_links'][player_name] = player_url
        user_links[player_name] = player_url
    user_info.close()

#displays the general player stats
def displayPlayerStats(name):

    player = isAlreadyScraped(name.upper())

    if player != None:
        #recast the floating point value of headshot percentage to a string to be sliced and printed
        headshot_percent_full = str(player.getPlayerHeadshotPercentage())

        s = (f'Rank: {player.getPlayerRank()}\n'
             f'Time Played: {player.getPlayerTimePlayed()}\n'
             f'K/D: {player.getPlayerKillDeath()}\n'
             f'W/L: {player.getPlayerWinLoss()}\n'
             #Turn the long string of headshot percentage into an actual percentage by 'moving the decimal over 2 spots'
             #just take the first two numbers after the decimal point in the string and put a % sign after them
             f'Headshot %: {headshot_percent_full[2:4]}%\n'
             )
        print(s)

def displayOperatorStats(player_name, operator_name):

    player_name = player_name.upper()
    operator_name = operator_name.upper()
    player = isAlreadyScraped(player_name)

    if player != None:
        s = (f'{player_name}\'S {operator_name} STATS:\n'
             f'Time Played: {player.getOperatorTimePlayed(operator_name)}\n'
             f'K/D: {player.getOperatorKillDeath(operator_name)}\n'
             f'W/L: {player.getOperatorWinLoss(operator_name)}\n'
            )
        print(s)

def comparePlayers(player_1_name, player_2_name):
    #load player stats from the dictionary or scrape the players stats if they haven't already been scraped
    player_1 = isAlreadyScraped(player_1_name)
    player_2 = isAlreadyScraped(player_2_name)

    #recast both players floating point headshot value as strings 
    headshot_percent_full_1 , headshot_percent_full_2 = str(player_1.getPlayerHeadshotPercentage()) , str(player_2.getPlayerHeadshotPercentage())

    s = (f'\t{player_1_name.upper()}\t\t{player_2_name.upper()}\n'
         f'Rank: {player_1.getPlayerRank()}\t{player_2.getPlayerRank()}\n'
         f'Time Played: {player_1.getPlayerTimePlayed()}\t{player_2.getPlayerTimePlayed()}\n'
         f'W/L: \t{player_1.getPlayerWinLoss()}\t\t{player_2.getPlayerWinLoss()}\n'
         f'K/D: \t{player_1.getPlayerKillDeath()}\t\t{player_2.getPlayerKillDeath()}\n'
         f'Headshot %: {headshot_percent_full_1[2:4]}%\t{headshot_percent_full_2[2:4]}%\n'
         f'Melee Kills: {player_1.getPlayerMeleeKills()}\t\t{player_2.getPlayerMeleeKills()}\n'
        )
    print(s)

def compareOperators(player_1_name, player_2_name, operator):
    operator = operator.upper()
    #load player stats from the dictionary or scrape the players stats if they haven't already been scraped
    player_1 = isAlreadyScraped(player_1_name)
    player_2 = isAlreadyScraped(player_2_name)

    s = (f'\t{player_1_name.upper()}\t{player_2_name.upper()}\n'
         f'Time Played: {player_1.getOperatorTimePlayed(operator)}\t{player_2.getOperatorTimePlayed(operator)}\n'
         f'W/L: {player_1.getOperatorWinLoss(operator)}\t{player_2.getOperatorWinLoss(operator)}\n'
         f'K/D: {player_1.getOperatorKillDeath(operator)}\t{player_2.getOperatorKillDeath(operator)}\n'
        )
    print(s)

def commandHelp():
    s = ('Commands and arguments are not case senesitive\n'
         'make sure you have spaces between arguments and commands\n'
         'Commands:\n'
         'ADD_PLAYER \'name\'  -adds a player to your saved list of players to scrape and compare\n'
         'ADD_FAVORITE \'name\'  -adds a player to your favorites list, this list will be scraped on launch\n'
         'LIST  -lists all players saved and ready to be scraped\n'
         'FAVORITES  -lists all players in your favorites list\n'
         'DISP_STATS \'player name\'  -displays the general stats for a given player\n'
         'OP_STATS \'player name\' \'operator name\'  -displays the operator specific stats for a given player\n'
         'COMPARE_OP \'player name\' \'player name\' \'operator name\'  -displays the specific operator stats for two given players side by side\n'
         'COMPARE_PLAYERS \'player name\' \'player name\'  -displays the stats for two given players side by side for comparison\n'
        )
    print(s)


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
