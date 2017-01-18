# coding: utf-8

import sys
import cyclone.web

from front.urls import apiurls
# from front.urls import url_patterns
from front.settings import settings
from front.storage import DatabaseMixin

from twisted.python import log
import logging
import time

handlers = [(u[0], u[1]) for u in apiurls]
class Application(cyclone.web.Application):
    def __init__(self):

        # Set up database connections
        DatabaseMixin.setup(settings)

        cyclone.web.Application.__init__(self, handlers, **settings)

def main():
    from twisted.internet import reactor

    mytime = time.strftime("%Y_%m_%d_%H_%I",time.localtime(time.time()))
    filenameUrl = "/tmp/acg_pay_zone_%s.log"%(mytime)
    # 配置日志信息
    logging.basicConfig(level=logging.WARNING,
        format='%(message)s',
        datefmt='%m-%d %H:%M',
        filename=filenameUrl,
        filemode='w')
    # 定义一个Handler打印INFO及以上级别的日志到sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    # 设置日志打印格式
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    # 将定义好的console日志handler添加到root logger
    logging.getLogger('').addHandler(console)

    log.startLogging(sys.stdout)
    # reactor.listenTCP(8800, Application())
    reactor.listenTCP(8800, Application())
    reactor.run()

if __name__ == "__main__":
    main()

