from rest_framework import serializers

from scraper.models import ExchangeRate


class ExchangeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRate
        fields = ('currency', 'rate')
