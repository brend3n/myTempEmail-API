import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# from bs4 import BeautifulSoup
# from web_scraper import get_soup_adv
from time import sleep
import json
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 



class TempMail():
	start_url = "https://mytemp.email/2/"
	def __init__(self):
		self.start(self.start_url)
	
	def start(self, url):
		chrome_options = Options()
		# chrome_options.add_argument("--headless")
		
		# Remove the warnings
		try:
			self.driver = webdriver.Chrome(chrome_options=chrome_options)
		except Exception as e:
			pass
		self.driver.get(url)
		sleep(5)

	def clean_email_address_GET(self, data):
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

	def get_email_address(self):
		data = self.driver.execute_script("return window.localStorage")
		self.inbox, self.hash = self.clean_email_address_GET(data)
		self.email_url = f"https://mytemp.email/2/#!/inbox/{self.inbox}/{self.hash}"
		print(f"email_url: {self.email_url}")
		return self.email_url, self.inbox, self.hash

	def read_XPATH(self,xpath):
		try:
			WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
		except Exception as e:
			print(f"Caught Exception: {e}")
		data = self.driver.find_element(By.XPATH, xpath).get_attribute("ng-href");
		return data

	def get_message(self):
		inbox = [] 
		data = self.read_XPATH(xpath='//*[@id="app"]/div/md-content/div/div/div/md-list/md-list-item[1]/a')
		message_url = f"https://mytemp.email/2/{data}"
		self.driver.get(message_url)
		sleep(5)
		message = self.driver.find_element(By.XPATH, '//*[@id="eml-part-text"]/pre').get_attribute('innerHTML')
		print(f"message: {message}")
  
		return message

	def get_messages(self):
		pass

	def delete_message(self):
		self.driver.get(self.email_url)
		data = self.read_XPATH(xpath='//*[@id="app"]/div/md-content/div/div/div/md-list/md-list-item[1]/a')
		message_address = data[7:].split("/")
		print(f"message_address: {message_address}")
		delete_url = f"https://api.mytemp.email/1/eml/destroy?eml={message_address[0]}&hash={message_address[1]}"
		print(f"delete_url: {delete_url}")
		output = requests.get(delete_url)
		print(f"Request status: {output}")

def main():
    mail = TempMail()
    mail.get_email_address()
    mail.get_message()
    mail.delete_message()
if __name__ == '__main__':
    	main()
