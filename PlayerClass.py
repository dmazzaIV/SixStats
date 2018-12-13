from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Player:

	def __init__(self, player_name,login_info):
		self.login_info = login_info
		self.driver = webdriver.Chrome()
		#self.login_info = login_info
		self.player_stats = {}

	def login(self):

		#login pop up is in a different IFrame, switch to it
		iframe = self.driver.find_element_by_tag_name('iframe')
		self.driver.switch_to.frame(iframe)

		login_email = self.driver.find_element_by_id('AuthEmail')
		login_email.send_keys(self.login_info['email'])
		login_pwd = self.driver.find_element_by_id('AuthPassword')
		login_pwd.send_keys(self.login_info['pwd'])
		submit_button = self.driver.find_element_by_id('LogInButton')
		submit_button.click()

		#Switch driver back to main webpage for webscraping
		self.driver.switch_to.default_content()

	def scrapeStats(self):

		self.driver.get('https://game-rainbow6.ubi.com/en-us/uplay/player-statistics/dbd1cef3-d69d-4296-a235-ae8d7d70363f/multiplayer')
		self.login()

		WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(By.ID, 'section'))
		stats = self.driver.find_elements_by_class_name('stat-value')
		if len(stats) > 0:
			print('found')
		else:
			print('fuck this')

		#page_soup = soup(self.driver.page_source, 'html.parser')

		#stats_list = page_soup.find_all('p', {'class': 'stat-value ng-binding'})

Dan = Player('Dan')
Dan.scrapeStats()
