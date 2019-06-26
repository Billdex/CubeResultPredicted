import requests
from bs4 import BeautifulSoup
import re
import bs4
import json

def getHtmlText(url, code='UTF-8'):
    trytime = 5
    while trytime > 0:
        try:
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6726.400 QQBrowser/10.2.2265.400',
            }
            r = requests.get(url, headers=header, timeout=3)
            r.raise_for_status()
            r.encoding = code
            return r.text
        except:
            print("get获取失败,尝试重连")
            trytime -= 1
    print('重连失败')

# 获取个人的特定项目的成绩数据，max表示该成绩不能超过某值
def getPersonalResult(wcaid, event, max):
    url = 'http://www.cubingchina.com/results/person/' + wcaid
    html = getHtmlText(url, 'utf-8')
    eventhref = '<a href=\"/results/rankings\?event={}&amp;type=average&amp;region=China\">'.format(event)
    td = re.findall(eventhref+'(.*?)</a>', html)
    try:
        if len(td) != 0 and float(td[0]) < max:
            return td[0]
    except:
        return None


# 获取成绩数据
# event1表示基础项目成绩
# event2表示预测项目成绩
# max1表示基础项目成绩的最大值
# max2表示预测项目成绩的最大值
def getResult(event1, event2, max1, max2):
    url = 'https://cubingchina.com/results/rankings?region=China&event={}&gender=all&type=average&page={}'.format(event1, 1)
    html = getHtmlText(url, 'utf-8')
    maxpage = re.findall(r'page=(.*?)\">末页', html)
    results = []
    with open('./data.json', 'r') as f:
        results = json.load(f)
    if len(maxpage) != 0:
        for i in range(43, int(maxpage[0])):
            url = 'https://cubingchina.com/results/rankings?region=China&event={}&gender=all&type=average&page={}'.format(event1, i+1)
            html = getHtmlText(url, 'utf-8')
            wcaid = re.findall(r'data-id=\"(.*?)\"', html)
            soup = BeautifulSoup(html, "html.parser")
            result1 = []
            result2 = []
            for tr in soup.find('tbody').children:
                if isinstance(tr, bs4.element.Tag):
                    tds = tr('td')
                    result = tds[4].string
                    result1.append(result)
            for i in range(len(wcaid)):
                if float(result1[i]) < max1:
                    result = getPersonalResult(wcaid[i], event2, max2)
                    if result == None:
                        print('{}的{}成绩不符合要求'.format(wcaid[i], event2))
                    else:
                        print('{}\t{}'.format(result1[i], result))
                        results.append([result1[i], result])
                else:
                    return
            with open('./data.json', 'w') as f:
                f.write(json.dumps(results, ensure_ascii=False))
    else:
        url = 'https://cubingchina.com/results/rankings?region=China&event={}&gender=all&type=average'.format(event1)
        html = getHtmlText(url, 'utf-8')
        wcaid = re.findall(r'data-id=\"(.*?)\"', html)
        print(wcaid)





def main():
    # print(getPersonalResult('2016ZHAN45', '333oh', 40))
    getResult('333', '333oh', 20, 50)
main()
