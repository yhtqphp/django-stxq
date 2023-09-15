from threading import Thread, Lock
from concurrent.futures import ThreadPoolExecutor
from stxq.conf import Conf
import signal
from signal import SIGINT, SIGBREAK

import time

class Manage(object):
    def __init__(self):

        self.threaPool = ThreadPoolExecutor()
        self.__lock = Lock()
        self.__procSubmit = []
        self.__runProcs = []
        self.__EXIT = False
        self.t1 = Thread(target=self.runSubmit, daemon=False)
        self.t2 = Thread(target=self.checkProc, daemon=False)
        self.setSig()

    def setSig(self):
        signal.signal(SIGINT, self.sigHander)

    def sigHander(self, sig, frame):
        print(sig)
        self.stop()

    def submit(self, procList: list):
        self.__procSubmit.extend(procList)

    # 运行提交的进程
    def runSubmit(self):
        while not self.__EXIT:
            with self.__lock:
                try:
                    for i in self.__procSubmit:
                        p = i()
                        p.start()
                        self.__runProcs.append(p)
                        self.__procSubmit.remove(i)
                except Exception as e:
                    pass
                finally:
                    time.sleep(Conf.checkProcTimeout)

    # 检查进程是否存活
    def checkProc(self):
        st = time.time()

        while not self.__EXIT:
            if (time.time() - st) > 5:
                print('定时结束')
                self.stop()
            with self.__lock:
                for i in self.__runProcs:
                    try:
                        if i.is_alive():
                            continue
                        i.terminate()

                        if not i.is_alive():
                            p = i.__class__
                            pS = p()
                            pS.start()
                            self.__runProcs.remove(i)
                            self.__runProcs.append(pS)
                    except Exception as e:
                        pass
                    finally:
                        time.sleep(Conf.checkProcTimeout)
    def start(self):
        self.__EXIT = False
        self.t1.start()
        self.t2.start()

    def stop(self):
        self.__EXIT = True

    def join(self):
        while not self.__EXIT:
            try:
                self.setSig()
                time.sleep(0.1)
            except Exception as e:
                import traceback
                traceback.print_exc()
                break