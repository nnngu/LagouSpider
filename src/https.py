# -*- coding: utf-8 -*-
from src.setting import IP, UA
import requests, random
import logging

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s Process%(process)d:%(thread)d %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='diary.log',
                    filemode='a')


class Http:
    '''
    http请求相关的操作
    '''

    def __init__(self):
        pass

    def get(self, url, headers=None, cookies=None, proxy=None, timeOut=5, timeOutRetry=5):
        '''
        获取网页源码
        url: 网页链接
        headers: headers
        cookies: cookies
        proxy: 代理
        timeOut: 请求超时时间
        timeOutRetry: 超时重试次数
        return: 源码
        '''
        if not url:
            logging.error('GetError url not exit')
            return 'None'
        logging.error('Get %s' % url)
        try:
            if not headers: headers = {'User-Agent': UA[random.randint(0, len(UA) - 1)]}
            # if not proxy: proxy = {'http':"http://"+IP[random.randint(0, len(IP)-1)]}
            response = requests.get(url, headers=headers, cookies=cookies, proxies=proxy, timeout=timeOut)
            if response.status_code == 200 or response.status_code == 302:
                htmlCode = response.text
            else:
                htmlCode = 'None'
            logging.error('Get %s %s' % (str(response.status_code), url))
        except Exception as e:
            logging.error('GetExcept %s' % str(e))
            if timeOutRetry > 0:
                htmlCode = self.get(url=url, timeOutRetry=(timeOutRetry - 1))
            else:
                logging.error('GetTimeOut %s' % url)
                htmlCode = 'None'
        return htmlCode

    def post(self, url, para, headers=None, cookies=None, proxy=None, timeOut=5, timeOutRetry=5):
        '''
        post获取响应
        url: 目标链接
        para: 参数
        headers: headers
        cookies: cookies
        proxy: 代理
        timeOut: 请求超时时间
        timeOutRetry: 超时重试次数
        return: 响应
        '''
        if not url or not para:
            logging.error('PostError url or para not exit')
            return None
        logging.error('Post %s' % url)
        try:
            if not headers:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3'}
            response = requests.post(url, data=para, headers=headers, cookies=cookies, proxies=proxy, timeout=timeOut)
            if response.status_code == 200 or response.status_code == 302:
                htmlCode = response.text
            else:
                htmlCode = None
            logging.error('Post %s %s' % (str(response.status_code), url))
        except Exception as e:
            logging.error('PostExcept %s' % str(e))
            if timeOutRetry > 0:
                htmlCode = self.post(url=url, para=para, timeOutRetry=(timeOutRetry - 1))
            else:
                logging.error('PostTimeOut %s' % url)
                htmlCode = None
        return htmlCode

    def confirm(self, htmlCode, url, headers, cookies, proxy, catch_retry=5):
        '''
        反爬，验证页面
        htmlCode:网页源码
        return:网页源码
        '''
        # 获取网页title判断是否被ban
        return htmlCode

    def urlprocess(self, items):
        # +    URL 中+号表示空格               %2B
        # 空格 URL中的空格可以用+号或者编码    %20
        # /    分隔目录和子目录                %2F
        # ?    分隔实际的URL和参数             %3F
        # %    指定特殊字符                    %25
        # #    表示书签                        %23
        # &    URL 中指定的参数间的分隔符      %26
        # =    URL 中指定参数的值              %3D
        content = items.replace('&#047;', '%2F').replace('&#061;', '%3D').replace('+', '%2B').replace( \
            ' ', '%20').replace('/', '%2F').replace('?', '%3F').replace('=', '%3D')
        return content
