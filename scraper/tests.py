import pytest
import feedparser
import requests_mock
from unittest import mock
from scraper.tasks import parse_rss
from scraper.models import ExchangeRate

from django.urls import reverse
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


class TestExchangeRate(object):
    def test_exchange_rate(self):
        ExchangeRate.objects.create(currency='USD')
        ExchangeRate.objects.create(currency='JPY')
        ExchangeRate.objects.create(currency='BGN')

        client = APIClient()
        response = client.get(reverse('exchange-rate-list'))
        assert response.json() == [
            {'currency': 'USD', 'rate': None},
            {'currency': 'JPY', 'rate': None},
            {'currency': 'BGN', 'rate': None}
        ]

        feedparser.parse = mock.Mock(
            side_effect=[
                {'entries': [{'cb_targetcurrency': 'USD', 'cb_exchangerate': '1.2222'}]},
                {'entries': [{'cb_targetcurrency': 'JPY', 'cb_exchangerate': '121.88'}]},
                {'entries': [{'cb_targetcurrency': 'BGN', 'cb_exchangerate': '1.988'}]},
            ]
        )
        with requests_mock.mock() as m:
            m.get(
                'https://www.ecb.europa.eu/home/html/rss.en.html',
                text="""
                <a class="rss" href="/rss/fxref-usd.html">US dollar (USD)</a>,
                <a class="rss" href="/rss/fxref-jpy.html">Japanese yen (JPY)</a>,
                <a class="rss" href="/rss/fxref-bgn.html">Bulgarian lev (BGN)</a>,
                """
            )
            parse_rss()

        assert ExchangeRate.objects.get(currency='USD').rate == 1.2222
        assert ExchangeRate.objects.get(currency='JPY').rate == 121.88
        assert ExchangeRate.objects.get(currency='BGN').rate == 1.988

        response = client.get(reverse('exchange-rate-list'))
        assert response.json() == [
            {'currency': 'USD', 'rate': 1.2222},
            {'currency': 'JPY', 'rate': 121.88},
            {'currency': 'BGN', 'rate': 1.988}
        ]
