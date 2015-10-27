# -*- coding:utf-8 -*-
import threading
from logUtil.Logger import Logger
__author__ = 'shadowmydx'


class ConfigIpGenerator(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.producer_queue = None
        self.file_path = None
        self.condition = None

    def set_condition(self, condition):
        self.condition = condition

    def set_file_path(self, file_path):
        self.file_path = file_path

    def set_producer_queue(self, queue):
        self.producer_queue = queue

    def run(self):
        first_ip = self.gen_ip_by_path(self.file_path)
        while True:
            try:
                ip = next(first_ip)
                self.producer_queue.put(ip)
            except StopIteration:
                break
        Logger.log('1st producer out.')

    @staticmethod
    def gen_ip_by_path(path):
        file_seg = open(path, 'r')
        seg = file_seg.read()
        seg_list = [item.strip() for item in seg.split('|')]
        for key in seg_list:
            yield key
        file_seg.close()


if __name__ == '__main__':
    test = ConfigIpGenerator()
    test.set_file_path('../ip_list.txt')
    test.run()





