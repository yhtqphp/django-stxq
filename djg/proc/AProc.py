from stxq.core.proc.BaseProc import BaseProc
import time

class AProc(BaseProc):
    def run(self) -> None:
        self.sig()
        for i in range(10):
            if not self.status():
                return
            print('运行', time.strftime('%Y-%m-%d %H:%M:%S'), self.__class__)
            time.sleep(1)