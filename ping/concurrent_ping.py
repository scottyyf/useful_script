#!/usr/bin/env python
# coding=utf-8
   
# 这个程序用来找出新开机的服务器的ip
# 这里使用了concurrent 的线程池进行加速
   
   
from subprocess import Popen, PIPE
from tqdm import tqdm
import time
import concurrent.futures
   
   
def pingable(ips):
    if isinstance(ips, str):
        return ping_single(ips)
   
    elif isinstance(ips, list):
        ret = []
        for ip in ips:
            ip_list = ping_single(ip)
            if ip_list:
                ret.extend(ip_list)

    return ret


def ping_single(ip):
    p = Popen(["ping", "-c", "1", ip, "-w", "1"], stdout=PIPE)
    data, err = p.communicate()
    if p.returncode == 0:
        return [ip]
    else:
        return []


executor = concurrent.futures.ThreadPoolExecutor(max_workers=256)


def main(data):
    pbar = tqdm(data, colour='yellow', leave=True, unit='B')
    ret1 = []
    for x in pbar:
        pbar.set_description('Processing' + str(x))
        ret = executor.submit(pingable, x)
        ret1.append(ret)
    d = []
    for ret in ret1:
        d.extend(ret.result())

    return d


if __name__ == "__main__":
    start_time = time.monotonic()
    data = ["192.168.4." + str(a) for a in range(1, 255)]
    data1 = main(data)
    end_time = time.monotonic()
    #input('time to wait for human action: ')
    #data2 = main(data)
    print(data1)
    print(end_time - start_time)
    #print(set(data2) - set(data1))
