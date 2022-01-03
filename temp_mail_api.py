from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
from web_scraper import get_soup_adv
from time import sleep
import json
GET_url = "https://mytemp.email/2/"


def start():
    driver = webdriver.Chrome()
    driver.get(GET_url)
    sleep(3)
    return driver

def clean_email_address_GET(data):
	data = str(data)[97:]
	data = data[:data.index("',") + 1].strip()
	data = data.replace(':{"',':"').replace("}}", "}")
	data = list(data[data.index(":"):])
	data[0] = "{"
	data = "".join(data)[:-1]
	
	data = json.loads(data)
	inbox = data["inbox"]
	hash = data["hash"]
	return inbox, hash

def get_email_address(driver):
	data = driver.execute_script("return window.localStorage")
	inbox,hash = clean_email_address_GET(data)
	# print(f"data[inbox]: {inbox}")
	# print(f"data[hash]: {hash}")
	email_url = f"https://mytemp.email/2/#!/inbox/{inbox}/{hash}"
	print(f"email_url: {email_url}")
	return email_url

driver = start()
get_email_address(driver)
