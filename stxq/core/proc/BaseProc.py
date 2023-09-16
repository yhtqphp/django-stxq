from multiprocessing import Process
import signal
from signal import SIGINT
from stxq.conf import Conf
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{}.settings'.format(Conf.name))
django.setup()
# 进程基类

class BaseProc(Process):

    def __init__(self, start_event):
        super().__init__()
        self.start_event = start_event

    def sig(self):
        signal.signal(SIGINT, self.sigHandle)

    def sigHandle(self, sig, frame):
        pass

    def status(self):
        return self.start_event.is_set()