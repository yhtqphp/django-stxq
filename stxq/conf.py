from django.conf import settings


class Conf:
    conf = settings.S_TXQ
    # pid路径
    pid = conf.get('pid', None)
    # 检测进程时间, 单位秒
    checkProcTimeout = conf.get('check_proc_timeout', 1)
    process = conf.get('process', [])
