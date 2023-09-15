from stxq.core.service.BaseService import BaseService
from stxq.core.proc.manage import Manage

from stxq.conf import Conf
import signal, psutil
from signal import SIGINT
import atexit
import time, os
import importlib

class Service(BaseService):
    __EXIT = False
    def __init__(self):
        BaseService.__init__(self)

        self.man = Manage()
        self.man.submit(self.getClass())

    def start(self):
        self.__EXIT = False
        self.man.start()
        self.join()

    def stop(self):
        self.__EXIT = True
        self.man.stop()
        atexit.register(os.remove,'')
        print('结束运行')

    def getClass(self):
        tem = []
        for i in Conf.process:
            pack = importlib.import_module(i)
            name = i.split('.')[-1]
            className = getattr(pack, name, None)
            if className is None:
                continue
            tem.append(className)
        return tem

    def sigHander(self, sig, frame):
        self.stop()

    def setSig(self):
        signal.signal(SIGINT, self.sigHander)

    def join(self):
        while not self.__EXIT:
            try:
                self.setSig()
                time.sleep(0.1)
            except Exception as e:
                import traceback
                traceback.print_exc()
                break