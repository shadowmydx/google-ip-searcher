# -*- coding:utf-8 -*-
import socket
import threading
import ssl
import struct
import httplib
__author__ = 'shadowmydx'

TIME_OUT = 6
hostname = 'goagent.appspot.com'


class IpTester(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.consumer_queue = None
        self.producer_queue = None

    @staticmethod
    def test_simple_ip(ip):
        try:
            connection = socket.socket()
            connection.settimeout(TIME_OUT)
            connection.connect((ip, 443))
            connection.send('get')
            connection.close()
            return True
        except:
            return False

    @staticmethod
    def test_ssl_ip(ip):
        try:
            connection = socket.socket()
            connection.settimeout(TIME_OUT)
            ssl_connection = ssl.wrap_socket(connection, cert_reqs=ssl.CERT_REQUIRED, ca_certs='cacert.pem')
            ssl_connection.settimeout(TIME_OUT * 4)
            ssl_connection.connect((ip, 443))
            cert = ssl_connection.getpeercert()
            print cert
            flag, subject = IpTester.judge_cert(cert)
            ssl_connection.close()
            connection.close()
            return flag, subject
        except:
            return False, None

    @staticmethod
    def judge_cert(cert):
        try:
            subject = cert['subject']
            subject = [item for item in subject if item[0][0] == 'commonName'][0]
            return subject[0][1].find("google") != -1, subject[0][1]
        except IndexError:
            return False, None

    @staticmethod
    def test_goagent_ip(ip):
        sock = None
        ssl_sock = None
        ipaddr = (ip, 443)
        try:
            sock = socket.socket(socket.AF_INET)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 32 * 1024)
            sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, True)
            sock.settimeout(TIME_OUT)
            ssl_sock = ssl.wrap_socket(sock, ssl_version=3, ciphers='ECDHE-RSA-AES128-SHA',
                                       do_handshake_on_connect=False)
            ssl_sock.settimeout(TIME_OUT)
            ssl_sock.connect(ipaddr)
            ssl_sock.do_handshake()
            ssl_sock.sock = sock
            ssl_sock.settimeout(TIME_OUT)
            ssl_sock.send('HEAD /favicon.ico HTTP/1.1\r\nHost: %s\r\n\r\n' % hostname)
            response = httplib.HTTPResponse(ssl_sock, buffering=True)
            try:
                response.begin()
                if hostname.endswith('.appspot.com') and 'Google' not in response.getheader('server', ''):
                    raise socket.timeout('timed out')
            except:
                ssl_sock.close()
                raise socket.timeout('timed out')
            finally:
                print response.getheader('server', '')
                response.close()
            return True
        except (socket.error, ssl.SSLError, OSError):
            if ssl_sock:
                ssl_sock.close()
            if sock:
                sock.close()
            return False

    def set_consumer_queue(self, queue):
        self.consumer_queue = queue

    def set_producer_queue(self, queue):
        self.producer_queue = queue

    def run(self):
        while True:
            ip = self.consumer_queue.get()
            if self.test_simple_ip(ip):
                flag, cert = self.test_ssl_ip(ip)
                if flag:
                    flag = self.test_goagent_ip(ip)
                    if flag:
                        self.producer_queue.put((ip, cert))
                else:
                    print ip + ' is a broken ip.'
            else:
                print ip + ' is a broken ip.'
            self.consumer_queue.task_done()

if __name__ == '__main__':
    ip = '64.233.162.81'
    if IpTester.test_simple_ip(ip):
        print 'pass one.'
        if IpTester.test_ssl_ip(ip)[0]:
            print 'pass two.'
            if IpTester.test_goagent_ip(ip):
                print 'pass three'
    print IpTester.test_goagent_ip('64.233.162.85')
