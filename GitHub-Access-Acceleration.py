from __future__ import print_function
import requests
from requests.adapters import HTTPAdapter
import time
import os
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED
from bs4 import BeautifulSoup
import ctypes
import sys

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.3'
}

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=5))
s.mount('https://', HTTPAdapter(max_retries=5))

hosts = [
    'github.global.ssl.fastly.net',
    'assets-cdn.github.com',
    'documentcloud.github.com',
    'github.com',
    'gist.github.com',
    'help.github.com',
    'nodeload.github.com',
    'raw.github.com',
    'status.github.com',
    'training.github.com',
    'www.github.com',
    'avatars0.githubusercontent.com',
    'avatars1.githubusercontent.com',
    'avatars2.githubusercontent.com',
    'avatars3.githubusercontent.com',
    'avatars4.githubusercontent.com',
    'avatars5.githubusercontent.com',
    'avatars6.githubusercontent.com',
    'avatars7.githubusercontent.com',
    'avatars8.githubusercontent.com',
    'codeload.github.com',
    'camo.githubusercontent.com',
    'cloud.githubusercontent.com',
    'raw.githubusercontent.com'
]
ips = {}


def getIP(host):
    # print('Getting. url:','https://www.ip.cn/ip/'+host+'.html')
    try:
        s = requests.get('https://www.ip.cn/ip/'+host+'.html', headers=headers)
    except requests.exceptions.RequestException as e:
        print(host, 'ip acquisition failed.')
        return
    s.encoding = 'UTF-8'
    soup = BeautifulSoup(s.text, "html.parser")
    ip = soup.select('.layui-card-body .layui-table tr th div')[0].get_text()
    ips[host] = ip
    print('Host:', host, 'ip:', ip)


def main():
    print('Loaded.')
    print('Hosts: ')
    for i in hosts:
        print(i)
    print('-'*100)
    print('Multithreading preparing.')
    print('max_workers=10')
    executor = ThreadPoolExecutor(max_workers=10)
    time.sleep(2)
    print('-'*100)
    print('Get IP from ip.cn.')
    all_task = [executor.submit(getIP, (host)) for host in hosts]
    wait(all_task, return_when=ALL_COMPLETED)
    print('Writting to C:\\Windows\\System32\\drivers\\etc\\hosts')
    with open('C:\\Windows\\System32\\drivers\\etc\\hosts', 'w') as f:
        f.write('''
# Copyright (c) 2017-2020, googlehosts members.
# https://github.com/googlehosts/hosts
# Last updated: 2020-06-19

# This work is licensed under a modified HOSTS License.
# https://github.com/googlehosts/hosts/raw/master/LICENSE

# Modified Hosts Start

# Localhost (DO NOT REMOVE) Start
127.0.0.1	localhost
# Localhost (DO NOT REMOVE) End

# GitHub Start

''')
        for i in ips:
            f.write(i+' '+ips[i]+'\n')
        f.write('''
# GitHub End

# Modified Hosts End
        ''')
    print('Refreshing DNS cache.')
    os.system('ipconfig /flushdns')
    print('GitHub acceleration completed.')
    
    os.system('pause')


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == '__main__':
    # main()
    # '''
    if is_admin():
        main()
    else:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1)
    # '''
