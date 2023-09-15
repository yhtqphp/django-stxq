from stxq.core.proc.BaseProc import BaseProc

class AProc(BaseProc):
    def run(self) -> None:
        print('运行', self.__class__)