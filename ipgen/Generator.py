# -*- coding:utf-8 -*-

import socket
import struct
import threading
import random
__author__ = 'shadowmydx'


class IpGenerator(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.producer_queue = None
        self.seg_list = None
        self.condition = None

    def set_condition(self, condition):
        self.condition = condition

    def set_seg_list(self, seg_list):
        self.seg_list = seg_list

    def set_producer_queue(self, queue):
        self.producer_queue = queue

    def run(self):
        # self.condition.acquire()
        # print 'thread acquire after.'
        while len(self.seg_list) != 0:
            seg = random.choice(self.seg_list)
            self.seg_list.remove(seg)
            first_ip = self.gen_ip_by_seg(seg)
            while True:
                try:
                    ip = next(first_ip)
                    self.producer_queue.put(ip)
                except StopIteration:
                    break
        # self.condition.notifyAll()
        # self.condition.release()
        print '1st producer out.'

    @staticmethod
    def gen_ip_by_seg(seg):
        seg_lst = seg.split('/')
        ip = seg_lst[0]
        ip_range = 32 - int(seg_lst[1])
        start = socket.ntohl(struct.unpack("I", socket.inet_aton(str(ip)))[0])
        for key in range(1 << ip_range):
            yield socket.inet_ntoa(struct.pack('I', socket.htonl(start + key)))


# if __name__ == '__main__':
#     first_ip = IpGenerator.gen_ip_by_seg('64.18.0.0/20')
#     tester = iptester.IpTester.IpTester
#     while True:
#         try:
#             ip = next(first_ip)
#             if tester.test_ip(ip):
#                 print ip
#         except StopIteration:
#             break
#     print 'finished.'




