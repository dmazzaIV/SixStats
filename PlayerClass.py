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

		#login pop up is in a different IFrame
		#Wait for it to load and switch to it
		WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe.ng-scope.ng-isolate-scope.rs-template-uplay-connect")))

		login_email = self.driver.find_element_by_id('AuthEmail')
		login_email.send_keys('d.mazza830@gmail.com')
		login_pwd = self.driver.find_element_by_id('AuthPassword')
		login_pwd.send_keys('Frenchtoast#1')
		submit_button = self.driver.find_element_by_id('LogInButton')
		submit_button.click()

		#Switch driver back to main webpage for webscraping
		self.driver.switch_to.default_content()


	def scrapePlayerStats(self):

		#Pull all stats from webpage into a list
		#Particular stat value inedexes' differ if the person is ranked vs unranked so we need 2 cases
		stats_list = self.driver.find_elements_by_class_name('stat-value')
		ranked = self.driver.find_element_by_xpath('//*[@id="section"]/div/div/div[1]/div/div[1]/div/div/div[3]/div/div[2]/div/div[2]/p[2]')

		if ranked.text == 'NOT RANKED YET.':
			self.player_stats['Rank'] = 'Not Ranked'
			self.player_stats['Time Played'] = stats_list[4].text
			self.player_stats['Headshots']  = stats_list[8]
			self.player_stats['W/L'] = stats_list[11].text
			self.player_stats['K/D'] = stats_list[12].text
			self.player_stats['Melee Kills'] = stats_list[10].text
		else:
			self.player_stats['Rank'] = stats_list[4].text
			self.player_stats['Time Played'] = stats_list[6].text
			self.player_stats['Headshots'] = stats_list[10]
			self.player_stats['W/L'] = stats_list[13].text
			self.player_stats['K/D'] = stats_list[14].text
			self.player_stats['Melee Kills'] = stats_list[12].text

	def scrapeOperatorStats(self):
		#navigate to operator tab
		operator_tab = self.driver.find_element_by_xpath('//*[@id="section"]/div/div/div[2]/div/div[1]/div/div/div/div/article[1]/div[2]/div/div[1]/button')
		self.driver.execute_script("arguments[0].click();", operator_tab)
		#wait for operator stats elements to load
		#TODO: figure out a way to explicitlly wait
		self.driver.implicitly_wait(2)

		#Get the li tag that is a list of all operators and thier respective stats
		operator_list_set = self.driver.find_element_by_xpath('//*[@id="section"]/div/div/div[2]/div/div[1]/div/div/div/div/article[3]/div[1]/div/div/div/nav/ul')
		operators = operator_list_set.find_elements_by_tag_name('li')

		for operator in operators:
			operator_stats = operator.find_elements_by_tag_name('p')
			for stat in operator_stats:
				print(stat.text)

	def populateStats(self):
		
		self.driver.get('https://game-rainbow6.ubi.com/en-us/uplay/player-statistics/b3f64755-8892-47db-aa6c-82929cd29f30/multiplayer')
		self.login()

		#Wait for operator stats button to be clickable
		#This tells us that the page is fully loaded and we are able to navigate to the operator page when we are done with the player stats
		WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#section > div > div > div.ng-scope > div > div.player-statistics-tabs.ng-isolate-scope.rs-organism-tabs > div > div > div > div > article.ng-scope.ng-isolate-scope.selected > div.player-statistics-most-used-operator.rs-atom-box > div > div.more-operator-stats.ng-scope > button')))
		#self.scrapePlayerStats()
		self.scrapeOperatorStats()


Dan = Player('Dan')
Dan.populateStats()
