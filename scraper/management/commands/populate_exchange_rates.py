from django.core.management.base import BaseCommand

from scraper.tasks import parse_rss


class Command(BaseCommand):
    help = 'Populate the currencies with their corresponding Exchange Rates'

    def handle(self, *args, **options):
        print('Populating exchange rates...')
        parse_rss()
        print('Done populating.')
