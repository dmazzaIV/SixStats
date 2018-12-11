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

	iframe = driver.find_element_by_tag_name('iframe')
	driver.switch_to.frame(iframe)
	login_email = driver.find_element_by_id('AuthEmail')
	login_email.send_keys(login_info[0])
	login_pwd = driver.find_element_by_id('AuthPassword')
	login_pwd.send_keys(login_info[1])
	submit_button = driver.find_element_by_id('LogInButton')
	submit_button.click()

	driver.switch_to_default_content()

login()