# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# code by jax

import argparse
import socket
import requests
import time
import threading
import queue
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def add_http(url_host):
    try:
        if '443' in str(url_host):
            if 'http://' in str(url_host):
                final_url = str(url_host).replace('http://', 'https://')
            else:
                final_url = 'https://' + str(url_host)
        else:
            if 'http://' in str(url_host):
                final_url = str(url_host)
            else:
                final_url = 'http://' + str(url_host)
        #print(final_url)
        get_title(final_url)
    except:
        pass

def save_result(filename,url):
    with open(filename,'a+', encoding="utf-8") as f:
        f.write(str(url)+'\n')

def get_title(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
        res = requests.get(url,headers=headers,timeout=3,verify=False)
        res.encoding = res.apparent_encoding #apparent_encoding比encoding更加准确，防止中文乱码
        response = res.text
        soup = BeautifulSoup(response,'lxml')
        span = soup.title.string
        print(url+"\ttitle:"+span+"\033[0m")
        url_title = "%-27s %-30s\n" % (url,span)
        save_result(result,url_title)
    except Exception as e:
        pass

def worker():
    while not q_ueue.empty():
        url_host = q_ueue.get()
        try:
            add_http(url_host)
        finally:
            q_ueue.task_done()


def thread(threads):
    thread_list = []
    for t in range(threads):
        t = threading.Thread(target = worker,args = ())
        thread_list.append(t)

    for t in thread_list:
        t.start()

    for t in thread_list:
        t.join()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="== Extract IP PORT form xml ==")
    parser.add_argument('-f', '--file', type=str, help="url file path")
    parser.add_argument('-r', '--result', type=str, help="result")
    parser.add_argument('-t', '--threads', type=int, help="threads")
    args = parser.parse_args()

    if args.file == 0 or args.result == 0:
        print("[-]wrong！请输入-f url文件和-r 结果存储文件位置！")
    if args.file and args.result:
        if not args.threads:
            args.threads = 10 #缺省值为10
        t_ime = time.time()
        q_ueue = queue.Queue()
        file = args.file
        threads = args.threads
        result = args.result
        with open(file,'r') as f:
            for line in f.readlines():
                url_host = line.strip()
                q_ueue.put(url_host)
        thread(threads)
        q_ueue.join()
        print("end time:",time.time()-t_ime)
    else:
        print("[-]wrong！For example:\n >> python3 title_get.py -f url.txt -r result.txt -t 10\n")