# -*- coding:utf-8 -*-
import threading
from logUtil.Logger import Logger
__author__ = 'shadowmydx'


class SimpleOutput(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.consumer_queue = None
        self.result_lst = None

    def set_result_lst(self, result_lst):
        self.result_lst = result_lst

    def set_consumer_queue(self, queue):
        self.consumer_queue = queue

    def add_to_result(self, ip_speed):
        self.result_lst.append(ip_speed)

    def run(self):
        while True:
            ip_speed = self.consumer_queue.get()
            # print 'The google ip is ' + ip_speed[0] + ', the speed is ' + ip_speed[1]
            self.add_to_result(ip_speed)
            Logger.log('Got one good ip: ' + ip_speed[0] + ' .')
            self.consumer_queue.task_done()
