import logging
import logging.handlers

# 日志打印到 /var/log/burn/csk5 路径下就会被 logtail 自动采集上传
LOG_FILE = '/home/yhzhu/work/prj/csk5/python/log/tst1.log'

handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5) # 实例化handler
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(levelno)s %(levelname)s %(pathname)s %(module)s %(funcName)s %(created)f %(thread)d %(threadName)s %(process)d %(name)s - %(message)s'
formatter = logging.Formatter(fmt)   # 实例化formatter。
handler.setFormatter(formatter)      # 为handler添加formatter。
logger = logging.getLogger('tst')    # 获取名为tst的logger。
logger.addHandler(handler)           # 为logger添加handler。
logger.setLevel(logging.DEBUG)

import time

while True:
    time.sleep(5)
    logger.info('first info message')
    logger.debug('first debug message')
