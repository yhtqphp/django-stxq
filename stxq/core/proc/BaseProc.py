from multiprocessing import Process
# 进程基类

class BaseProc(Process):
    def a(self):
        self.is_alive()
        self.terminate()