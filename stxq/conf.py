from django.conf import settings
import platform

class Conf:
    conf = settings.S_TXQ
    name=conf.get('name', '')
    # pid路径
    pid = conf.get('pid', settings.BASE_DIR / 'stxq.pid')
    stderr = conf.get('stderr', '/dev/null')
    stdout = conf.get('stdout', '/dev/null')
    # 检测进程时间, 单位秒
    checkProcTimeout = conf.get('check_proc_timeout', 1)
    process = conf.get('process', [])

    isLinux = True if platform.system().lower() == 'linux' else False