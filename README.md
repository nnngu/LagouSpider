# 🕷️ 爬取拉勾网职位信息的爬虫！

## 效果预览

![][7]

## 思路

1、首先我们打开拉勾网，并搜索“java”，显示出来的职位信息就是我们的目标。

2、接下来我们需要确定，怎样将信息提取出来。

* 查看网页源代码，这时候发现，网页源代码里面找不到职位相关信息，这证明拉勾网关于职位的信息是异步加载的，这也是一种很常用的技术。

* 异步加载的信息，我们需要借助 chrome 浏览器的开发者工具进行分析，打开开发者工具的方法如下：

![][1]

* 点击Nerwork进入网络分析界面，这时候是一片空白，刷新一下界面就可以看到一系列的网络请求了。

![][2]

* 前面我们说到，拉勾网关于职位的信息是异步加载的，那么在这一系列的网络请求中，必定有某个请求发送给服务器，响应回来的是职位信息。

* 正常情况下，我们可以忽略css，图片等类型的请求，关注点放在XHR这种类型请求上，如图：

![][3]

一共4个XHR类型的请求，我们逐个打开对比，分别点击Preview就能看到它们响应的内容。

发现第一个请求就是我们要找的。如图：

![][4]

点击Headers，查看一下请求参数。如下图：

![][5]

到此，我们可以确定city参数就是城市，pn参数就是页数，kd参数就是搜索关键字。

接下来开始写代码了。

## 代码

代码分成四个部分，便于后期维护。

**1、基本 https 请求`https.py`**

这部分对 requests 包进行了一些封装，部分代码如下：

```python
# -*- coding: utf-8 -*-
from src.setting import IP, UA
import requests, random
import logging


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

		# 这里只展示了一部分代码
		# 完整代码已上传到Github
```

这里只展示了一部分代码，完整代码已上传到[Github](https://github.com/nnngu/LagouSpider)

**2、代码主逻辑部分`main.py`**

这部分的程序逻辑，如下：

* 获取职位信息

```python
def getInfo(url, para):
    """
    获取信息
    """
    generalHttp = Http()
    htmlCode = generalHttp.post(url, para=para, headers=headers, cookies=cookies)
    generalParse = Parse(htmlCode)
    pageCount = generalParse.parsePage()
    info = []
    for i in range(1, 3):
        print('第%s页' % i)
        para['pn'] = str(i)
        htmlCode = generalHttp.post(url, para=para, headers=headers, cookies=cookies)
        generalParse = Parse(htmlCode)
        info = info + getInfoDetail(generalParse)
        time.sleep(2)
    return info
```

* 对信息进行储存

```python
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
```

**3、信息解析部分`parse.py`**

这部分针对服务器返回的职位信息的特点，进行解析，如下：

```python
class Parse:
    '''
    解析网页信息
    '''

    def __init__(self, htmlCode):
        self.htmlCode = htmlCode
        self.json = demjson.decode(htmlCode)
        pass

    def parseTool(self, content):
        '''
        清除html标签
        '''
        if type(content) != str: return content
        sublist = ['<p.*?>', '</p.*?>', '<b.*?>', '</b.*?>', '<div.*?>', '</div.*?>',
                   '</br>', '<br />', '<ul>', '</ul>', '<li>', '</li>', '<strong>',
                   '</strong>', '<table.*?>', '<tr.*?>', '</tr>', '<td.*?>', '</td>',
                   '\r', '\n', '&.*?;', '&', '#.*?;', '<em>', '</em>']
        try:
            for substring in [re.compile(string, re.S) for string in sublist]:
                content = re.sub(substring, "", content).strip()
        except:
            raise Exception('Error ' + str(substring.pattern))
        return content

		# 这里只展示了一部分代码
		# 完整代码已上传到Github
```

这里只展示了一部分代码，完整代码已上传到[Github](https://github.com/nnngu/LagouSpider)

**4、配置部分`setting.py`**

这部分加入 cookies 的原因是为了应对拉勾网的反爬，长期使用需要进行改进，进行动态 cookies 获取

```python
# -*- coding: utf-8 -*-

# headers
headers = {
    'Host': 'www.lagou.com',
    'Connection': 'keep-alive',
    'Content-Length': '23',
    'Origin': 'https://www.lagou.com',
    'X-Anit-Forge-Code': '0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Anit-Forge-Token': 'None',
    'Referer': 'https://www.lagou.com/jobs/list_java?city=%E5%B9%BF%E5%B7%9E&cl=false&fromSearch=true&labelWords=&suginput=',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}
```

## 测试

运行结果：

![][6]

爬取结束后，在src目录下就可以看到爬虫爬取到的数据。

![][7]

到此，拉勾网的职位信息抓取就完成了。完整代码已经上传到[我的Github](https://github.com/nnngu/LagouSpider)


  [1]: https://www.github.com/nnngu/FigureBed/raw/master/2018/2/3/1517604536071.jpg
  [2]: https://www.github.com/nnngu/FigureBed/raw/master/2018/2/3/1517604631241.jpg
  [3]: https://www.github.com/nnngu/FigureBed/raw/master/2018/2/3/1517605038140.jpg
  [4]: https://www.github.com/nnngu/FigureBed/raw/master/2018/2/3/1517605245280.jpg
  [5]: https://www.github.com/nnngu/FigureBed/raw/master/2018/2/3/1517605796162.jpg
  [6]: https://www.github.com/nnngu/FigureBed/raw/master/2018/2/3/1517607653279.jpg
  [7]: https://www.github.com/nnngu/FigureBed/raw/master/2018/2/3/1517607553153.jpg