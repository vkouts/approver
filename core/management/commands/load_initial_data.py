# -*- coding: utf-8 -*-
from django.core.management import BaseCommand

from Bank.initial_data import load_data as bank_init_data



class Command(BaseCommand):

    def handle(self, *args, **options):
        bank_init_data()
