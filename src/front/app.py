# coding: utf-8

import sys
import cyclone.web

from front.urls import apiurls
# from front.urls import url_patterns
from front.settings import settings
from front.storage import DatabaseMixin

from twisted.python import log
import logging


handlers = [(u[0], u[1]) for u in apiurls]
class Application(cyclone.web.Application):
    def __init__(self):

        # Set up database connections
        DatabaseMixin.setup(settings)

        cyclone.web.Application.__init__(self, handlers, **settings)

def main():
    from twisted.internet import reactor

    # 配置日志信息
    logging.basicConfig(level=logging.DEBUG,
        format='%(message)s',
        datefmt='%m-%d %H:%M',
        filename='/tmp/acg_pay_zone.log',
        filemode='w')
    # 定义一个Handler打印INFO及以上级别的日志到sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # 设置日志打印格式
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    # 将定义好的console日志handler添加到root logger
    logging.getLogger('').addHandler(console)

    log.startLogging(sys.stdout)
    # reactor.listenTCP(8800, Application())
    reactor.listenTCP(80, Application())
    reactor.run()

if __name__ == "__main__":
    main()

