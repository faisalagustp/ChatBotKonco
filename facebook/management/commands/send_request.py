# -*- coding: utf-8 -*-
from django.core.management import BaseCommand

class Command(BaseCommand):
    # Show this when the user types help

    def handle(self, *args, **options):
        pass