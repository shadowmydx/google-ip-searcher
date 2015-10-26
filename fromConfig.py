# -*- coding:utf-8 -*-
import ipgen.Generator
import iptester.IpTester
import speedtester.SpeedTester
import ipdealer.OutputStdout
import Queue
import threading
import time
import ipgen.ConfigGenerator
__author__ = 'shadowmydx'


configs = {'threads': 15, 'speed_counts': 5, 'speeders': 3}


def setup_all_speeders():
    limit = configs['speeders']
    speeders = []
    for key in range(limit):
        speeder = speedtester.SpeedTester.SpeedTester()
        speeders.append(speeder)
    return speeders


def setup_all_testers():
    limit = configs['threads']
    testers = []
    for key in range(limit):
        tester = iptester.IpTester.IpTester()
        testers.append(tester)
    return testers


def setup_all_queues(ip_producer, ip_testers, speed_testers, ip_dealer):
    queue_list = []
    to_tester = Queue.Queue()
    queue_list.append(to_tester)
    ip_producer.set_producer_queue(to_tester)
    to_speeder = Queue.Queue()
    queue_list.append(to_speeder)
    for key in ip_testers:
        key.set_consumer_queue(to_tester)
        key.set_producer_queue(to_speeder)
    to_dealer = Queue.Queue()
    queue_list.append(to_dealer)
    for key in speed_testers:
        key.set_consumer_queue(to_speeder)
        key.set_producer_queue(to_dealer)
    ip_dealer.set_consumer_queue(to_dealer)
    return queue_list


def setup_all_condition(ip_producer):
    condition = threading.Condition()
    ip_producer.set_condition(condition)
    return condition


def boost_up(ip_testers, speed_testers, ip_dealer):
    for key in ip_testers:
        key.setDaemon(True)
        key.start()
    for key in speed_testers:
        key.setDaemon(True)
        key.start()
    ip_dealer.setDaemon(True)
    ip_dealer.start()


def write_result_to_file(result_lst):
    if len(result_lst) == 0:
        return
    path = './result' + str(time.time()) + '.log'
    f = open(path, 'w')
    for key in result_lst:
        f.write('The google ip is ' + key[0] + ', the speed is ' + str(key[1]) + ', the cert is ' + str(key[2]) + '\n')
    for key in result_lst:
        f.write(key[0] + '|')
    f.close()


def wait_for_end(queues, result_lst):
    for queue in queues:
        queue.join()
        print 'one finished.'
    print 'all task finished.'
    result_lst.sort(cmp=lambda x, y: int(x[1] - y[1]))
    write_result_to_file(result_lst)


def main():
    result_lst = list()
    ip_producer = ipgen.ConfigGenerator.ConfigIpGenerator()
    ip_producer.set_file_path('./ip_list.txt')
    ip_testers = setup_all_testers()
    ip_dealer = ipdealer.OutputStdout.SimpleOutput()
    ip_dealer.set_result_lst(result_lst)
    speed_testers = setup_all_speeders()
    queues = setup_all_queues(ip_producer, ip_testers, speed_testers, ip_dealer)
    boost_up(ip_testers, speed_testers, ip_dealer)
    ip_producer.run()
    print '1st producer end ...'
    wait_for_end(queues, result_lst)
    print result_lst

if __name__ == '__main__':
    main()
