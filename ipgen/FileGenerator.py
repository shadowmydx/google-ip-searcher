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
            first_ip = self.gen_ip_by_range(seg)
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
    def gen_ip_by_range(seg):
        seg_lst = seg.split('-')
        ip_start = seg_lst[0].strip()
        ip_end = seg_lst[1].strip()
        start = socket.ntohl(struct.unpack("I", socket.inet_aton(str(ip_start)))[0])
        end = socket.ntohl(struct.unpack("I", socket.inet_aton(str(ip_end)))[0])
        for key in xrange(end - start + 1):
            yield socket.inet_ntoa(struct.pack('I', socket.htonl(start + key)))

if __name__ == '__main__':
	gen = IpGenerator.gen_ip_by_range('46.16.9.0-46.16.9.255')
	while True:
		try:
			ip = next(gen)
			print ip
		except StopIteration:
			break