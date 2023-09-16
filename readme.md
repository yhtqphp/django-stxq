基于django的后台进程组件<br>

1，安装
```
git clone git@gitee.com:yhtqduan/django-stxq.git
cd django-stxq
python setup install
```

使用在 INSTALLED_APPS 中加入 stxq
```
INSTALLED_APPS = [
    '...'
    ,'stxq'
]
```
[settings.py](djg%2Fsettings.py) 文件新增配置
```
S_TXQ = {
    "name": 'djg',
    'pid': BASE_DIR / 'stxq.pid',
    'process': [
        'djg.proc.AProc'
    ]
}
```

使用方法
```
开启
python manage.py stxq start

关闭
python .\manage.py stxq stop
```


2, 配置
```
name ：名称
pid  ： pid文件为准
check_proc_timeout ：轮训检测进程时间
process  ： 进程列表
```

