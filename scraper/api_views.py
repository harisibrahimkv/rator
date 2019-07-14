from rest_framework import viewsets

from scraper.models import ExchangeRate
from scraper.serializers import ExchangeRateSerializer


class ExchangeRateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Exchange Rates to be viewed.
    """
    serializer_class = ExchangeRateSerializer

    def get_queryset(self):
        queryset = ExchangeRate.objects.all()
        currency = self.request.query_params.get('currency', None)
        if currency:
            queryset = queryset.filter(currency=currency)
        return queryset
