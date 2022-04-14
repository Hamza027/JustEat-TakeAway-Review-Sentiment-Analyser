from selenium import webdriver
from curses.ascii import BEL
from email import header
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import re
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




def extract():
    headers = {"USer:Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"}
    url = f"https://www.just-eat.co.uk/restaurants-pindi-express-lower-earley/reviews"
    
    #r = requests.get(url,headers)
    driver.get(url)
    driver.implicitly_wait(4)
    driver.find_element_by_css_selector('.Button_o-btn--fullWidth_1xkfh').click()
    
    
    
    page_num = 0

    while True:
        try:
            time.sleep(2)
            driver.find_element_by_css_selector('.o-btn').click()
            page_num += 1
            print("getting page number "+str(page_num))
            #time.sleep(1)
        except:
            break
        
    
    r = driver.find_element_by_class_name("c-megaModal-document")
    soup = BeautifulSoup(r.get_attribute("innerHTML"),'html.parser')
    #print({"R status code":r.status_code})
    #print(soup)

    transform(soup)
    
def transform(soup):
    Name = []
    Date = []
    Reviews = []
    
    table = soup.findAll('div',attrs={"data-test-id":"review-container"})
    for x in table:
        
        Name.append(x.find('h3', attrs={"data-test-id":"review-author"}).text.strip())
        Date.append(x.find('p', attrs={"data-test-id":"review-date"}).text.strip())
        if x.find('p', attrs={"data-test-id":"review-text"}) == None:
            Reviews.append("None")
        else:
            Reviews.append(x.find('p', attrs={"data-test-id":"review-text"}).text.strip())

            
 
    load(Name,Date,Reviews)
    #print(Name,Date,Reviews)
    


def load(Name,Date,Reviews):
    df = pd.DataFrame({"Customer_Name":Name,"Date":Date,"Review_Text":Reviews})
    df.to_csv("Review.csv", mode='a', header=True, index=False)
    print("Data Extraction Successfull :) ")


driver = webdriver.Chrome("./chromedriver")

extract()

driver.quit()