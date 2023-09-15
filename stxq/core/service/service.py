from stxq.core.service.BaseService import BaseService
from stxq.core.proc.manage import Manage
from stxq.conf import Conf

import importlib


class Service(BaseService):
    def __init__(self):
        BaseService.__init__(self)

        self.man = Manage()
        self.man.submit(self.getClass())
        self.man.start()
        self.man.join()

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