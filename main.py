# pip install seleinium

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://quotes.toscrape.com/"
driver.get(url)


def scrape_quotes():
    # Find all quote elements
    quotes = driver.find_elements(By.CLASS_NAME, "text")
    # Extract and print the text of each quote
    for quote in quotes:
        print(quote.text)

scrape_quotes()

for _ in range(1, 11):  # Loop through the first 10 pages
    next_button = driver.find_element(By.XPATH, "/html/body/div/div[2]/div[1]/nav/ul/li/a")
    next_button.click()  # Click the "Next" button
    scrape_quotes()  # Scrape quotes from the new page
    

driver.quit()  # Close the browser


