from stxq.core.service.BaseService import BaseService
from stxq.core.proc.manage import Manage

from stxq.conf import Conf
import signal, psutil
from signal import SIGINT, SIGTERM
import atexit
import time, os, sys
import importlib


class Service(BaseService):
    __EXIT = False
    def __init__(self):
        BaseService.__init__(self)

        self.man = Manage()
        self.man.submit(self.getClass())


    def startLinux(self):
        if  os.path.isfile(Conf.pid):
            print('runing...')
            exit(0)
        pid = os.fork()
        if pid:
            exit(0)
        os.chdir('/')
        os.umask(0)
        os.setsid()
        pid = os.fork()
        if pid:
            exit(0)
        sys.stdout.flush()
        sys.stderr.flush()

        with open('/dev/null') as read_null, open(Conf.stdout, 'w') as write_null, open(Conf.stderr, 'w') as errwrite_null:
            os.dup2(read_null.fileno(), sys.stdin.fileno())
            os.dup2(write_null.fileno(), sys.stdout.fileno())
            os.dup2(errwrite_null.fileno(), sys.stderr.fileno())

        # 写入pid文件
        if Conf.pid:
            with open( Conf.pid, 'w+') as f:
                f.write(str(os.getpid()))
            # 注册退出函数，进程异常退出时移除pid文件
            atexit.register(os.remove,  Conf.pid)

        self.__EXIT = False
        self.man.start()
        self.join()

    def start(self):
        if Conf.isLinux:
            return self.startLinux()
        self.__EXIT = False
        self.man.start()
        self.join()

    def stop(self):

        self.__EXIT = True
        self.man.stop()
        print('结束运行')

    def stopPid(self):
        if not Conf.isLinux:
            return self.stop()
        if not os.path.isfile(Conf.pid):
            print('not runing')
            exit(0)

        with open(Conf.pid, 'r') as fp:
            pid = int(fp.read())
            while True:
                try:
                    os.kill(pid, SIGINT)
                except OSError as e:
                    print('退出成功  pid:{}'.format(pid))
                    exit(0)
                finally:
                    time.sleep(0.2)

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

    def status(self):
         return os.path.isfile(Conf.pid)
