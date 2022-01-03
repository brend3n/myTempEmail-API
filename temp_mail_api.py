import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


from bs4 import BeautifulSoup
from web_scraper import get_soup_adv
from time import sleep
import json
import warnings
start_url = "https://mytemp.email/2/"

warnings.filterwarnings("ignore", category=DeprecationWarning) 

def start(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    
    # Remove the warnings
    try:
        driver = webdriver.Chrome(chrome_options=chrome_options)
    except Exception as e:
        pass
    driver.get(url)
    sleep(5)
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

def get_new_email_address(driver):
	data = driver.execute_script("return window.localStorage")
	inbox,hash = clean_email_address_GET(data)
	email_url = f"https://mytemp.email/2/#!/inbox/{inbox}/{hash}"
	print(f"email_url: {email_url}")
	return email_url

def read_XPATH(driver, xpath):
	try:
		WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
	except Exception as e:
		print(f"Caught Exception: {e}")
	data = driver.find_element(By.XPATH, xpath).get_attribute("ng-href");
	# print(f"data: {data}")
	return data

def get_first_message_in_inbox_from_email_address(address, hash):
    inbox = []
    
    start_url = f"https://mytemp.email/2/#!/inbox/{address}/{hash}"
    driver = start(start_url)
    data = read_XPATH(driver, xpath='//*[@id="app"]/div/md-content/div/div/div/md-list/md-list-item[1]/a')
    
    message_url = f"https://mytemp.email/2/{data}"
    # print(f"message_url: {message_url}")
    driver.get(message_url)
    
    sleep(5)
    
    message = driver.find_element(By.XPATH, '//*[@id="eml-part-text"]/pre').get_attribute('innerHTML')
    
    print(f"message: {message}")
    return message

def pop_message_from_inbox(address, hash):
	start_url = f"https://mytemp.email/2/#!/inbox/{address}/{hash}"
	driver = start(start_url)
	data = read_XPATH(driver, xpath='//*[@id="app"]/div/md-content/div/div/div/md-list/md-list-item[1]/a')

	message_address = data[7:].split("/")
	# print(f"message_address: {message_address}")
	delete_url = f"https://api.mytemp.email/1/eml/destroy?eml={message_address[0]}&hash={message_address[1]}"
	# print(f"delete_url: {delete_url}")
	output = requests.get(delete_url)
	# print(f"output: {output}")
	pass

# driver = start(start)
# get_new_email_address(driver)
# read_XPATH(driver, "//*[@id='app']/div/md-content/div/div/div/md-list")
# get_first_message_in_inbox_from_email_address("hesj@hezll.com","41bcb0cb")
pop_message_from_inbox("hesj@hezll.com","41bcb0cb")
