from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import time
import schedule

url = "https://announcements.bybit.com/en-US/?category=&page=1"
filename = 'news.csv'


def parsing_news():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)
    new_listings = driver.find_element(By.CSS_SELECTOR, '[data-cy="newCrypto"]')
    new_listings.click()
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(2)
    html = driver.page_source
    driver.close()
    driver.quit()
    soup = BeautifulSoup(html, 'html.parser')
    titles = soup.findAll('span', class_='')
    links = soup.findAll('a', class_='no-style')
    dates = soup.findAll('div', class_='article-item-date')
    old_titles = load_titles()
    for link, date, title in zip(links, dates, titles):
        if title.text not in old_titles:
            add_record(title.text, link.get('href'), date.text)


def add_record(title, link, date):
    with open(filename, 'a', newline='', encoding='utf-8') as news_file:
        writer = csv.writer(news_file, delimiter=';')
        writer.writerow([title, link, date])


def load_titles():
    with open(filename, 'r', encoding='utf-8') as news_file:
        reader = csv.reader(news_file, delimiter=';')
        titles = set()
        for row in reader:
            if row:
                titles.add(row[0])
    return titles


schedule.every(1).seconds.do(parsing_news)
while True:
    schedule.run_pending()
