from threading import Thread, Lock
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Event
from stxq.conf import Conf
import signal
from signal import SIGINT, SIGTERM

import time

class Manage(object):
    def __init__(self):

        self.threaPool = ThreadPoolExecutor()
        self.__lock = Lock()
        self.__procSubmit = []
        self.__runProcs = []
        self.__EXIT = False
        self.status_event = Event()

        self.t1 = Thread(target=self.runSubmit, daemon=True)
        self.t2 = Thread(target=self.checkProc, daemon=True)
        self.setSig()
    
    def setSig(self):
        # signal.signal(SIGINT, self.sigHander)
        signal.signal(SIGTERM, self.sigHander)

    def sigHander(self, sig, frame):
        print(sig)
        self.stop()

    def submit(self, procList: list):
        self.__procSubmit.extend(procList)

    # 运行提交的进程
    def runSubmit(self):
        while self.status():
            with self.__lock:
                try:
                    for i in self.__procSubmit:
                        p = i(self.status_event)
                        p.start()
                        self.__runProcs.append(p)
                        self.__procSubmit.remove(i)
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                finally:
                    time.sleep(Conf.checkProcTimeout)

    # 检查进程是否存活
    def checkProc(self):
        while self.status():

            with self.__lock:
                for i in self.__runProcs:
                    try:
                        if i.is_alive():
                            continue
                        i.terminate()

                        if not i.is_alive():
                            p = i.__class__
                            pS = p(self.status_event)
                            pS.start()
                            self.__runProcs.remove(i)
                            self.__runProcs.append(pS)
                    except Exception as e:
                        import traceback
                        traceback.print_exc()
                    finally:
                        time.sleep(Conf.checkProcTimeout)

    def start(self):
        self.__EXIT = False
        self.status_event.set()
        self.t1.start()
        self.t2.start()

    def exit(self):
        return self.status_event.is_set()

    def status(self):
        return self.status_event.is_set()

    def stop(self):
        self.__EXIT = True
        self.status_event.clear()

    def join(self):
        self.t1.join()
        self.t2.join()