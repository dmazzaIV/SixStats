import shelve
import os
import PlayerClass as Player

#Global Variables
login_info = {}
user_links = {}

def main():
    pullUserDataFromShelf()

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
