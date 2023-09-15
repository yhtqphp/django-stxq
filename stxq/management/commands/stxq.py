from django.core.management.base import BaseCommand, CommandError
from stxq.core.service.service import Service
import importlib

class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument('option', default='start', help='start|stop|status|reload')

    def handle(self, *args, **options):

        if options['option'] =='start':
            self.start()

        if options['option'] =='stop':
            print('结束运行')

        if options['option'] =='status':
            print('运行状态')

        if options['option'] =='reload':
            print('重新运行')

    def start(self):
        s = Service()

