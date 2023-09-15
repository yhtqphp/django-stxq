from multiprocessing import Process
import signal
from signal import SIGINT
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