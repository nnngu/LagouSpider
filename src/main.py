# -*- coding: utf-8 -*-
from src.https import Http
from src.parse import Parse
from src.setting import headers
from src.setting import cookies
import time
import logging
import codecs

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s Process%(process)d:%(thread)d %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='diary.log',
                    filemode='a')


def getInfo(url, para):
    """
    获取信息
    """
    generalHttp = Http()
    htmlCode = generalHttp.post(url, para=para, headers=headers, cookies=cookies)
    generalParse = Parse(htmlCode)
    pageCount = generalParse.parsePage()
    info = []
    for i in range(1, pageCount + 1):
        print('第%s页' % i)
        para['pn'] = str(i)
        htmlCode = generalHttp.post(url, para=para, headers=headers, cookies=cookies)
        generalParse = Parse(htmlCode)
        info = info + getInfoDetail(generalParse)
        time.sleep(2)
    return info


def getInfoDetail(generalParse):
    """
    信息解析
    """
    info = generalParse.parseInfo()
    return info


def processInfo(info, para):
    """
    信息存储
    """
    logging.error('Process start')
    try:
        title = '公司名称\t公司类型\t融资阶段\t标签\t公司规模\t公司所在地\t职位类型\t学历要求\t福利\t薪资\t工作经验\n'
        file = codecs.open('%s职位.xls' % para['city'], 'w', 'utf-8')
        file.write(title)
        for p in info:
            line = str(p['companyName']) + '\t' + str(p['companyType']) + '\t' + str(p['companyStage']) + '\t' + \
                   str(p['companyLabel']) + '\t' + str(p['companySize']) + '\t' + str(p['companyDistrict']) + '\t' + \
                   str(p['positionType']) + '\t' + str(p['positionEducation']) + '\t' + str(
                p['positionAdvantage']) + '\t' + \
                   str(p['positionSalary']) + '\t' + str(p['positionWorkYear']) + '\n'
            file.write(line)
        file.close()
        return True
    except Exception as e:
        print(e)
        return None


def main(url, para):
    """
    主函数逻辑
    """
    logging.error('Main start')
    if url:
        info = getInfo(url, para)  # 获取信息
        flag = processInfo(info, para)  # 信息储存
        return flag
    else:
        return None


if __name__ == '__main__':
    kdList = [u'java']
    cityList = [u'广州', u'深圳']
    url = 'https://www.lagou.com/jobs/positionAjax.json'
    for city in cityList:
        print('爬取%s' % city)
        para = {'first': 'true', 'pn': '1', 'kd': kdList[0], 'city': city}
        flag = main(url, para)
        if flag:
            print('%s爬取成功' % city)
        else:
            print('%s爬取失败' % city)
