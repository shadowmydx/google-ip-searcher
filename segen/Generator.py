# -*- coding:utf-8 -*-
import os
import re
__author__ = 'shadowmydx'


class SegGenerator:

    def __init__(self):
        self.google_reg = re.compile(r'v=spf1 (?P<all_seg>.*?) ~all')
        self.cmd = r'nslookup -q=TXT _netblocks.google.com 8.8.8.8'

    def get_google_seg(self):
        p = os.popen(self.cmd)
        all_seg = p.read()
        seg_list = [key.strip() for key in self.google_reg.findall(all_seg)[0].split('ip4:') if len(key.split()) != 0]
        return seg_list


if __name__ == '__main__':
    gen = SegGenerator()
    gen.get_google_seg()
