from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Player:

	def __init__(self, url, login_info):
		self._login_info = login_info.copy()
		self.url = url
		#make chromedriver headless as we don't need the window to be displayed
		#also makes it a tad bit faster since it is not loading grpahical elements
		self.options = Options()
		self.options.headless = True
		self.driver = webdriver.Chrome(chrome_options = self.options)
		self.player_stats = {}
		self.operator_stats = {}

		self._populate_stats()

	def _login(self):
		"""Logs the driver into https://game-rainbow6.ubi.com for given player link."""
		#_login pop up is in a different IFrame
		#Wait for it to load and switch to it
		WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe.ng-scope.ng-isolate-scope.rs-template-uplay-connect")))

		login_email = self.driver.find_element_by_id('AuthEmail')
		login_email.send_keys(self._login_info['email'])
		login_pwd = self.driver.find_element_by_id('AuthPassword')
		login_pwd.send_keys(self._login_info['pwd'])
		submit_button = self.driver.find_element_by_id('_loginButton')
		self.driver.execute_script("arguments[0].click();", submit_button)

		#Switch driver back to main webpage for webscraping
		self.driver.switch_to.default_content()

	def _calculate_headshot_percent(self, total_headshots):
		"""Returns headshot percentage for player as a float (headshots / kills).

		Keyword arguements:
		total_headshots -- String value from driver for total headshots by that player, will be recast as float
		"""
		total_kills_element = self.driver.find_element_by_xpath('//*[@id="section"]/div/div/div[2]/div/div[1]/div/div/div/div/article[1]/div[1]/div/div[2]/div[2]/div/ul/li[1]/span[2]')
		total_kills = total_kills_element.get_attribute('innerHTML')

		return float(total_headshots) / float(total_kills)

	def _scrape_player_stats(self):
		"""Driver scrapes general player stats(Rank,Time Played, Headshot %, W/L, K/D, Melee kills) and stores them in player_stats dictionary."""
		#Pull all stats from webpage into a list
		#Particular stat value inedexes' differ if the person is ranked vs unranked so we need 2 cases
		stats_list = self.driver.find_elements_by_class_name('stat-value')
		ranked = self.driver.find_element_by_xpath('//*[@id="section"]/div/div/div[1]/div/div[1]/div/div/div[3]/div/div[2]/div/div[2]/p[2]')

		if ranked.text == 'NOT RANKED YET.':
			self.player_stats['Rank'] = 'Not Ranked Yet'
			self.player_stats['Time Played'] = stats_list[4].get_attribute('innerHTML')
			self.player_stats['Headshot %']  = self._calculate_headshot_percent(stats_list[8].get_attribute('innerHTML'))
			self.player_stats['W/L'] = stats_list[11].get_attribute('innerHTML')
			self.player_stats['K/D'] = stats_list[12].get_attribute('innerHTML')
			self.player_stats['Melee Kills'] = stats_list[10].get_attribute('innerHTML')
		else:
			self.player_stats['Rank'] = stats_list[4].get_attribute('innerHTML')
			self.player_stats['Time Played'] = stats_list[6].get_attribute('innerHTML')
			self.player_stats['Headshot %']  = self._calculate_headshot_percent(stats_list[10].get_attribute('innerHTML'))
			self.player_stats['W/L'] = stats_list[13].get_attribute('innerHTML')
			self.player_stats['K/D'] = stats_list[14].get_attribute('innerHTML')
			self.player_stats['Melee Kills'] = stats_list[12].get_attribute('innerHTML')

	def _scrape_operator_stats(self):
		"""Driver scrapes stats for all the player's operators(Name,Time Played, W/L, K/D) and stores them in operator_stats dictionary."""
		#Get the li tag that is a list of all operators and thier respective stats
		operator_list_set = self.driver.find_element_by_xpath('//*[@id="section"]/div/div/div[2]/div/div[1]/div/div/div/div/article[3]/div[1]/div/div/div/nav/ul')
		operators = operator_list_set.find_elements_by_tag_name('li')

		#use xpath here because if searching for 'p' tag will return 5 stats and we only want 3
		#so it takes more writing but I think it's more efficient
		for operator in operators:
			operator_name = operator.find_element_by_xpath('.//div/div[1]/div[1]/div/div[1]/p')
			operator_time_played = operator.find_element_by_xpath('.//div/div[1]/div[1]/div/div[2]/div/div/p')
			operator_win_loss = operator.find_element_by_xpath('.//div/div[1]/div[1]/div/div[3]/div/div/p')
			operator_kill_death = operator.find_element_by_xpath('.//div/div[1]/div[1]/div/div[4]/div/div/p')

			#make a dictionary that will act as the inner dictionary for holding stats in the operator stats dictionary
			inner_dictionary = {}
			inner_dictionary['Time Played'] = operator_time_played.get_attribute('innerHTML')
			inner_dictionary['W/L'] = operator_win_loss.get_attribute('innerHTML')
			inner_dictionary['K/D'] = operator_kill_death.get_attribute('innerHTML')
			self.operator_stats[operator_name.get_attribute('innerHTML')] = inner_dictionary


	def _populate_stats(self):
		"""Calls the scrapPlayerStats() and _scrape_operator_stats() functions to populate both the player_stats and operator_stats dictionaries."""FH
		self.driver.get(self.url)
		self._login()

		#wait for K/D to be visible, this is an arbitrary choice to just wait for the stats to load
		WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#section > div > div > div.ng-scope > div > div.player-statistics-tabs.ng-isolate-scope.rs-organism-tabs > div > div > div > div > article.ng-scope.ng-isolate-scope.selected > div.player-statistics-main.rs-atom-box > div > div.statistic-group.overview-hero.ng-scope > div:nth-child(2) > div > div > div.hero-stats > div > div > div.stats > p.stat-value.ng-binding')))
		self._scrape_player_stats()
		self._scrape_operator_stats()

	
	#ALL THE GETTER FUNCTIONS ARE DOWN HERE

	#PLAYER GETTERS

	def get_player_rank(self):
		"""Returns player's rank as string."""
		return self.player_stats['Rank']

	def get_player_time_played(self):
		"""Returns player's total time played as string."""
		return self.player_stats['Time Played']

	def get_player_headshot_percentage(self):
		"""Returns player's headshot % as a float."""
		return self.player_stats['Headshot %']

	def get_player_win_loss(self):
		"""Returns player's W/L as a string."""
		return self.player_stats['W/L']

	def get_player_kill_death(self):
		"""Returns player's K/D as a string."""
		return self.player_stats['K/D']

	def get_player_melee_kills(self):
		"""Returns player's melee kills as a string."""
		return self.player_stats['Melee Kills']

	#OPERATOR GETTERS

	def get_operator_time_played(self, operator_name):
		"""Returns player's time played for the given operator as a string."""
		op_name = operator_name.upper()
		try:
			return self.operator_stats[op_name]['Time Played']
		except ValueError:
			print(f'{op_name} is not a valid operator, maybe you misspelled the name')

	def get_operator_win_loss(self, operator_name):
		"""Returns player's W/L for the given operator as a string."""
		op_name = operator_name.upper()
		try:
			return self.operator_stats[op_name]['W/L']
		except ValueError:
			print(f'{op_name} is not a valid operator, maybe you misspelled the name')

	def get_operator_kill_death(self, operator_name):
		"""Returns player's K/D for the given operator as a string."""
		op_name = operator_name.upper()
		try:
			return self.operator_stats[op_name]['K/D']
		except ValueError:
			print(f'{op_name} is not a valid operator, maybe you misspelled the name')

