from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import time
import schedule


def parsing_news():
    url = "https://announcements.bybit.com/en-US/?category=&page=1"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        time.sleep(5)

        new_listings = driver.find_element(By.CSS_SELECTOR, '[data-cy="newCrypto"]')
        new_listings.click()

        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        titles = soup.findAll('span', class_='')
        links = soup.findAll('a', class_='no-style')
        dates = soup.findAll('div', class_='article-item-date')
        old_titles = load_titles()
        for link, date, title in zip(links, dates, titles):
            if title.text not in old_titles:
                add_record(title.text, link.get('href'), date.text)

    except Exception as ex:
        print(ex)


    finally:
        driver.close()
        driver.quit()


def add_record(title, link, date):
    with open('news.csv', 'w', newline='', encoding='utf-8') as news_file:
        writer = csv.writer(news_file)
        writer.writerow([title.replace(' ', ''), link, date.replace(' ', '')])


def load_titles():
    with open('news.csv', 'r', encoding='utf-8') as news_file:
        reader = csv.reader(news_file, delimiter=' ')
        titles = []
        for row in reader:
            titles.extend(row)
        titles = set(map(lambda x: x.split(',')[0], titles))
    return titles


schedule.every(1).seconds.do(parsing_news)
while True:
    schedule.run_pending()
