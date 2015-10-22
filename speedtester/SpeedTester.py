# -*- coding:utf-8 -*-
import threading
import re
import os
__author__ = 'shadowmydx'


class SpeedTester(threading.Thread):

    NO_SPEED = 2000

    def __init__(self):
        threading.Thread.__init__(self)
        self.consumer_queue = None
        self.producer_queue = None
        self.test_num = 5
        # depend on mac ox
        self.speed_reg = re.compile(r'time=(?P<speed>.*?) ms')

    def set_test_num(self, num):
        self.test_num = num

    def set_consumer_queue(self, queue):
        self.consumer_queue = queue

    def set_producer_queue(self, queue):
        self.producer_queue = queue

    def test_ip_speed(self, ip):
        p = os.popen("ping -c " + str(self.test_num) + " " + ip)
        result = p.read()
        avg_speed = self.cac_speed(result)
        if avg_speed < self.NO_SPEED:
            return True, avg_speed
        return False, -1

    def cac_speed(self, result):
        res_lst = [float(key) for key in self.speed_reg.findall(result)]
        while len(res_lst) < self.test_num:
            res_lst.append(self.NO_SPEED)
        return sum(res_lst) / len(res_lst)

    def run(self):
        while True:
            ip, cert = self.consumer_queue.get()
            result = self.test_ip_speed(ip)
            if result[0]:
                self.producer_queue.put((ip, result[1], cert))
            self.consumer_queue.task_done()


if __name__ == '__main__':
    tester = SpeedTester()
    tester.test_ip_speed('www.baidu.com')
