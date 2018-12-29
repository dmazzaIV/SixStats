from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Player:

	def __init__(self, url, login_info):
		self.login_info = login_info.copy()
		self.url = url
		#make chromedriver headless as we don't need the window to be displayed
		#also makes it a tad bit faster since it is not loading grpahical elements
		self.options = Options()
		self.options.headless = True
		self.driver = webdriver.Chrome(chrome_options = self.options)
		self.player_stats = {}
		self.operator_stats = {}

		self.populateStats()

	def login(self):

		#login pop up is in a different IFrame
		#Wait for it to load and switch to it
		WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe.ng-scope.ng-isolate-scope.rs-template-uplay-connect")))

		login_email = self.driver.find_element_by_id('AuthEmail')
		login_email.send_keys(self.login_info['email'])
		login_pwd = self.driver.find_element_by_id('AuthPassword')
		login_pwd.send_keys(self.login_info['pwd'])
		submit_button = self.driver.find_element_by_id('LogInButton')
		self.driver.execute_script("arguments[0].click();", submit_button)

		#Switch driver back to main webpage for webscraping
		self.driver.switch_to.default_content()

	def calculateHeadShotPercent(self, total_headshots):
		total_kills_element = self.driver.find_element_by_xpath('//*[@id="section"]/div/div/div[2]/div/div[1]/div/div/div/div/article[1]/div[1]/div/div[2]/div[2]/div/ul/li[1]/span[2]')
		total_kills = total_kills_element.get_attribute('innerHTML')

		return float(total_headshots) / float(total_kills)

	def scrapePlayerStats(self):

		#Pull all stats from webpage into a list
		#Particular stat value inedexes' differ if the person is ranked vs unranked so we need 2 cases
		stats_list = self.driver.find_elements_by_class_name('stat-value')
		ranked = self.driver.find_element_by_xpath('//*[@id="section"]/div/div/div[1]/div/div[1]/div/div/div[3]/div/div[2]/div/div[2]/p[2]')

		if ranked.text == 'NOT RANKED YET.':
			self.player_stats['Rank'] = 'Not Ranked Yet'
			self.player_stats['Time Played'] = stats_list[4].get_attribute('innerHTML')
			self.player_stats['Headshot %']  = self.calculateHeadShotPercent(stats_list[8].get_attribute('innerHTML'))
			self.player_stats['W/L'] = stats_list[11].get_attribute('innerHTML')
			self.player_stats['K/D'] = stats_list[12].get_attribute('innerHTML')
			self.player_stats['Melee Kills'] = stats_list[10].get_attribute('innerHTML')
		else:
			self.player_stats['Rank'] = stats_list[4].get_attribute('innerHTML')
			self.player_stats['Time Played'] = stats_list[6].get_attribute('innerHTML')
			self.player_stats['Headshot %']  = self.calculateHeadShotPercent(stats_list[10].get_attribute('innerHTML'))
			self.player_stats['W/L'] = stats_list[13].get_attribute('innerHTML')
			self.player_stats['K/D'] = stats_list[14].get_attribute('innerHTML')
			self.player_stats['Melee Kills'] = stats_list[12].get_attribute('innerHTML')

	def scrapeOperatorStats(self):

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


	def populateStats(self):
		
		self.driver.get(self.url)
		self.login()

		#wait for K/D to be visible, this is an arbitrary choice to just wait for the stats to load
		WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#section > div > div > div.ng-scope > div > div.player-statistics-tabs.ng-isolate-scope.rs-organism-tabs > div > div > div > div > article.ng-scope.ng-isolate-scope.selected > div.player-statistics-main.rs-atom-box > div > div.statistic-group.overview-hero.ng-scope > div:nth-child(2) > div > div > div.hero-stats > div > div > div.stats > p.stat-value.ng-binding')))
		self.scrapePlayerStats()
		self.scrapeOperatorStats()

	
	#ALL THE GETTER FUNCTIONS ARE DOWN HERE

	#PLAYER GETTERS

	def getPlayerRank(self):
		return self.player_stats['Rank']

	#stored as string returned as string
	#not really a stat worth comparing so shouldn't need to convert it to an int or float, just something worth displaying
	def getPlayerTimePlayed(self):
		return self.player_stats['Time Played']

	#stored as a float returned as a float
	def getPlayerHeadshotPercentage(self):
		return self.player_stats['Headshot %']

	#stored as a string returned as a float
	def getPlayerWinLoss(self):
		return self.player_stats['W/L']

	#stored as a string returned as a float
	def getPlayerKillDeath(self):
		return self.player_stats['K/D']

	#stored as a string returned as an int
	def getPlayerMeleeKills(self):
		return self.player_stats['Melee Kills']

	#OPERATOR GETTERS

	#stored as a string returned as a string
	#might be worth considering writing a function to convert the time to an int in minutes and compare those
	def getOperatorTimePlayed(self, operator_name):
		op_name = operator_name.upper()
		try:
			return self.operator_stats[op_name]['Time Played']
		except ValueError:
			print('{} is not a valid operator, maybe you misspelled the name'.format(op_name))

	#stored as a string returned as float
	def getOperatorWinLoss(self, operator_name):
		op_name = operator_name.upper()
		try:
			return self.operator_stats[op_name]['W/L']
		except ValueError:
			print('{} is not a valid operator, maybe you misspelled the name'.format(op_name))

	#stored as a string returned as a float
	def getOperatorKillDeath(self, operator_name):
		op_name = operator_name.upper()
		try:
			return self.operator_stats[op_name]['K/D']
		except ValueError:
			print('{} is not a valid operator, maybe you misspelled the name'.format(op_name))

