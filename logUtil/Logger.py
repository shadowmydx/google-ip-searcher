# -*- coding:utf-8 -*-
import threading
import Queue
import time
import datetime
__author__ = 'shadowmydx'


class Logger(threading.Thread):

    logger_instance = None

    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = Queue.Queue()

    def run(self):
        while True:
            output = self.queue.get()
            result = '[Info]'
            result += '[' + datetime.datetime.today().strftime('%H:%m:%S') + ']: '
            result += str(output)
            print result
            self.queue.task_done()

    def put_item(self, item):
        self.queue.put(item)

    @staticmethod
    def log(output):
        if Logger.logger_instance is None:
            Logger.logger_instance = Logger()
            Logger.logger_instance.setDaemon(True)
            Logger.logger_instance.start()
        Logger.logger_instance.put_item(output)

    @staticmethod
    def finish():
        Logger.logger_instance.queue.join()


if __name__ == '__main__':
    for i in range(10):
        Logger.log(i)
    Logger.finish()

