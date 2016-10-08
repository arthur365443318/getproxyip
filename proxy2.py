#!/usr/bin/env python
# -*-coding: utf-8-*-
# AUTHOR ：Arthur
# DATE   ：2016-10-08
# INTRO  ：getProxyIP
# VERSION：0.1


import requests
from time import sleep
from lxml import etree
import logging as log
import json
import os
log.basicConfig(filename='logger.log',level=log.INFO)

class getProxy(object):
    def __init__(self):
        self.url = 'http://www.xicidaili.com/nn/{0}'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.108 Safari/537.36"
        }
        self.json_file = 'proxy.json'
    def get_page(self,page):

        #for page in range(1, page):
        url = self.url.format(page)

        try:
            print(url)
            r = requests.get(url, headers=self.headers).text
            selector = etree.HTML(r)
            sleep(2)
            print('sleppping...{0}'.format(page))

        except Exception as e:
            log.error('get xicidaili page faild....', e)
        return selector
    def analysis(self,selector):
        try:
            proxies=[]
            ip_list = selector.xpath('//table[@id="ip_list"]')[0]
            for each in ip_list[1:]:
                ip =  each.xpath('td[2]/text()')[0]     #getip
                port = each.xpath('td[3]/text()')[0]    #getport
                ip_port = ip+':'+port                   #ip+port
                proxies.append(ip_port)
            log.info('get ip_port...')
            print('get ip_port')
        except Exception as e:
            log.error('analysis xicidaili faild...',e)
        return proxies

    def save(self,page):

        for p in range(1,page):
            selector = self.get_page(p)
            proxies =self.analysis(selector)
            with open(self.json_file, 'a') as f:
                json.dump(proxies, f)
                print('save......')

    def run(self):
        if os.path.isfile(self.json_file):
            os.remove(self.json_file)
            print('remove json_file...')
            self.save(4)
            print('run...')
        else:
            self.save(4)
if __name__=='__main__':
    Proxy = getProxy()
    Proxy.run()