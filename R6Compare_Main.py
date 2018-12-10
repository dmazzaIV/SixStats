from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

login_info= []

def getLoginInfo():
	email = input('Email: ')
	pwd = input('Password: ')
	login_info.append(email)
	login_info.append(pwd)

def login():
	getLoginInfo()

	driver = webdriver.Chrome()
	driver.get('https://game-rainbow6.ubi.com/en-us/home')

	login_button = driver.find_element_by_class_name('rs-atom-button')
	driver.execute_script('arguments[0].click();', login_button)

	login_email = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,'AuthEmail')))
	login_email.send_keys(login_info[0])

login()