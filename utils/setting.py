MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
      # 自定义中间件添加在最后
    'lib.log_middleware.RequestLogMiddleware'
]

LOGGING = {
    # 版本
    'version': 1,
    # 是否禁止默认配置的记录器
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '{"time": "%(asctime)s", "level": "%(levelname)s", "method": "%(method)s", "username": "%(username)s", "sip": "%(sip)s", "dip": "%(dip)s", "path": "%(path)s", "status_code": "%(status_code)s", "reason_phrase": "%(reason_phrase)s", "func": "%(module)s.%(funcName)s:%(lineno)d",  "message": "%(message)s"}',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    # 过滤器
    'filters': {
        'request_info': {'()': 'lib.log_middleware.RequestLogFilter'},
    },
    'handlers': {
        # 标准输出
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        # 自定义 handlers，输出到文件
        'restful_api': {
            'level': 'DEBUG',
            # 时间滚动切分
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'web-log.log'),
            'formatter': 'standard',
            # 调用过滤器
            'filters': ['request_info'],
            # 每天凌晨切分
            'when': 'MIDNIGHT',
            # 保存 30 天
            'backupCount': 30,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False
        },
        'web.log': {
            'handlers': ['restful_api'],
            'level': 'INFO',
            # 此记录器处理过的消息就不再让 django 记录器再次处理了
            'propagate': False
        },
    }
}