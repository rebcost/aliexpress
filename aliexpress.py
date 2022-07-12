from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep
import os
import sys
import pandas as pd

# Hidden mode
options = Options()
options.headless = True

# Drive Settings
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

PATH = os.path.dirname(sys.executable)

titles = []
prices = []
links = []
data = {'title': titles, 'price': prices, 'link': links}


def clear():
    """Clear console"""
    return os.system('cls') or None


def filename():
    """Returns the final name of the file"""
    clear()
    input_filename = input('\n\nInforme o nome do arquivo: ')
    return os.path.join(PATH, f'{input_filename}.csv')


def access_website():
    """Access Aliexpress website"""
    driver.get('https://pt.aliexpress.com/')


def search_product():
    """ Search for the product informed by the user """
    clear()
    input_name = input('\n\nInforme o produto para pesquisa: ')
    driver.find_element(by='xpath', value='//*[@id="search-key"]').send_keys(input_name)
    driver.find_element(by='xpath', value='//*[@id="form-searchbar"]/div[1]/input').click()


def load_all_product():
    """Run a script that scrolls the page to the end"""
    for i in range(0, 10000, 100):
        driver.execute_script(f"window.scrollTo(0, {i});")
        sleep(0.15)


def extract_product():
    """Get all product information, price and link"""
    load_all_product()
    content = driver.find_element(by='xpath', value='//*[@id="root"]/div/div/div[2]/div[2]/div/div[2]')
    html = content.get_attribute('outerHTML')
    soup = BeautifulSoup(html, 'html.parser')
    products = soup.find_all('div', class_='_3GR-w')
    for product in products:
        # title = product.select('div h1')
        title = product.find('h1', class_='_18_85').get_text()
        price = product.find('div', class_='mGXnE _37W_B').get_text()
        titles.append(title)
        prices.append(price)

    for link in soup.findAll('a', class_='_3t7zg _2f4Ho'):
        links.append('http:' + link.get('href'))


def export_to_csv():
    """Convert the dataframe file to format csv"""
    df = pd.DataFrame(data)
    df.to_csv(path_or_buf=filename(), encoding='UTF-8')


def start():
    access_website()
    search_product()
    extract_product()
    driver.quit()
    export_to_csv()
