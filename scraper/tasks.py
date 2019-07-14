import re
import requests
import feedparser

from bs4 import BeautifulSoup

from rator.celery import app
from scraper.models import ExchangeRate


BASE_URL = 'https://www.ecb.europa.eu/'


def fetch_exchange_rate_urls():
    """ Fetches all the currency RSS urls """
    exchange_rate_urls = []

    url = BASE_URL + 'home/html/rss.en.html'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'lxml')
    a_tags = soup.find_all("a", href=re.compile(r"fxref-"))
    for a_tag in a_tags:
        exchange_rate_urls.append(BASE_URL + a_tag.attrs['href'])

    return exchange_rate_urls


@app.task
def parse_rss():
    """ Parses each currency's RSS feed and saves the data into the db """
    exchange_rate_urls = fetch_exchange_rate_urls()
    for url in exchange_rate_urls:
        resp = feedparser.parse(url)
        currency = resp['entries'][0]['cb_targetcurrency']
        rate = resp['entries'][0]['cb_exchangerate'].split('\n')[0]
        ExchangeRate.objects.filter(currency=currency).update(rate=rate)
