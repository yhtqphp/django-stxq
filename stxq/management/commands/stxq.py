import os
import sys

from django.core.management.base import BaseCommand, CommandError
from stxq.core.service.service import Service
import importlib

class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        # parser.add_argument('option', default='start', help='start|stop|status|reload')
        parser.add_argument('option', default='start',  help='start|stop|status|reload|test')

    def handle(self, *args, **options):
        if options['option'] =='start':
            self.start()

        if options['option'] =='stop':
            self.stop()

        if options['option'] =='status':
            self.status()

        if options['option'] =='reload':
            self.stop()
            self.start()
        if options['option'] =='test':
            self.start()


    def status(self):
        s = Service()
        if s.status():
            self.stdout.write('runing')
        else:
            self.stdout.write('not runing')

    def start(self):
        s = Service()
        s.test()

    def stop(self):
        s = Service()
        s.stopPid()


