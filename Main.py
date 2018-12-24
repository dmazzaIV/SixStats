import shelve
import os
from Player import Player

#Global Variables
login_info = {}
user_links = {}
scraped_players = {}

def main():
    pullUserDataFromShelf()
    Dan = Player('Dan' , 'https://game-rainbow6.ubi.com/en-us/uplay/player-statistics/dbd1cef3-d69d-4296-a235-ae8d7d70363f/multiplayer', login_info)

    print(Dan.getPlayerKillDeath())

def pullUserDataFromShelf():
    if os.path.isfile('User_Info.dat'):
        user_info = shelve.open('User_Info')
        login_info['email'] =  user_info['login_info']['email']
        login_info['pwd'] =   user_info['login_info']['pwd']
        user_info.close()
    else:
        runFirstTimeWelcome()
        user_info = shelve.open('User_Info', writeback = True)
        user_email = input('Ubisoft account email: ')
        user_pwd = input('Ubisoft account password: ')
        user_info['login_info'] = {'email' : user_email, 'pwd' : user_pwd}
        
        login_info['email'] =  user_info['login_info']['email']
        login_info['pwd'] =   user_info['login_info']['pwd']
        user_info.close()

def runFirstTimeWelcome():
	print('Welcome to Rainbow Six Compare, an easy way to see who among your friends is truly the best at Rainbow Six Siege')
	print('You will need to input your Ubisoft email and password so that the program can fetch stats from Rainbow Six Siege Stats')
	print('(Don\'t worry they get saved locally on your machine they won\'t get leaked)')

main()
