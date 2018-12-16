from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Player:

	def __init__(self, player_name):
		#self.login_info = login_info
		self.driver = webdriver.Chrome()
		self.player_stats = {}

	def login(self):

		#login pop up is in a different IFrame, switch to it
		iframe = self.driver.find_element_by_tag_name('iframe')
		self.driver.switch_to.frame(iframe)

		login_email = self.driver.find_element_by_id('AuthEmail')
		login_email.send_keys('')
		login_pwd = self.driver.find_element_by_id('AuthPassword')
		login_pwd.send_keys('')
		submit_button = self.driver.find_element_by_id('LogInButton')
		submit_button.click()

		#Switch driver back to main webpage for webscraping
		self.driver.switch_to.default_content()


	def scrapeStats(self):

		self.driver.get('https://game-rainbow6.ubi.com/en-us/uplay/player-statistics/dbd1cef3-d69d-4296-a235-ae8d7d70363f/multiplayer')
		self.login()

		#Implicit wait for webpage to load after loggining in
		self.driver.implicitly_wait(5)

		#Pull all stats from webpage into a list
		#Particular stat value inedexes' differ if the person is ranked vs unranked so we need 2 cases
		stats_list = self.driver.find_elements_by_class_name('stat-value')
		ranked = self.driver.find_element_by_xpath('//*[@id="section"]/div/div/div[1]/div/div[1]/div/div/div[3]/div/div[2]/div/div[2]/p[2]')

		if ranked.text == 'NOT RANKED YET.':
			self.player_stats['Rank'] = 'Not Ranked'
			self.player_stats['Time Played'] = stats_list[4].text
			#self.player_stats['Headshot %'] = 
			self.player_stats['W/L'] = stats_list[11].text
			self.player_stats['K/D'] = stats_list[12].text



Dan = Player('Dan')
Dan.scrapeStats()
