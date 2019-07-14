README
======

## Setting up

1. This project assumes you're on Python3
2. `pip3 install -r requirements.txt`
3. Install and create postgres db + user.
4. Update the `DATABASE` in `settings.py` with the step 3 info.
5. `python manage.py migrate`
6. `python manage.py populate_exchange_rates`
7. `python manage.py runserver`
8. Go to your browser and check http://127.0.0.1:8000/api/rates/ to see the expected output
9. http://127.0.0.1:8000/api/rates/?currency=USD will give filtered output.
10. Run `pytest` to run the tests.
11. As a proper app, we would run celery too as such `celery -A rator worker --loglevel=info`

## What is this about?

This app reads the RSS feeds for each currecy's exchange rate from
https://www.ecb.europa.eu/home/html/rss.en.html, saves it into the database
and exposes it via an API endpoint.

- The database consists of a single table that stores the currency <-> rate mapping
- All rates are equivalent to 1 EURO.
- Contains a single endpoint with filters to fetch the exchange rates.

## Improvements

1. Celerybeat

The feeds are updated at 2.15PM. Need to figure out the timeone
and setup celerybeat to run the task and update the exchange rates
on a daily basis.

2. Redis cache

Since the rates are updated only on a daily basis, setup redis
cache with daily expiry to serve the exchange rates. Would probably
use `redis-py` library to achieve this.

3. urllib mocking

The tests now mock the requests call with the proper HTML response
but mocks the `feedparser.parse` call directly since that was
taking some time to figure out how to mock the correspoding
urllib methods that feedparser uses underneath.
