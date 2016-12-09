import requests
from urllib import parse
from bs4 import BeautifulSoup

s = requests.Session()
zjh = '140809011224'
mm= '286333'
postdata = {
    'evalue' : '',
    'zjh1' :'',
    'zjh' : zjh,
    'fs' : '',
    'v_yzm' : '',
    'lx' : '',
    'mm' : mm,
    'eflag' : '',
    'dzslh' : '',
    'tips' : ''
    }
head = {
            "Accept-Language":"zh-CN,zh;q=0.8",
            'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
            "Connection":"keep-alive",
            'Referer': "http://211.82.47.2/"
            }
one = s.post('http://211.82.47.2/loginAction.do', data = postdata, headers=head)
"""
boom = s.get('http://211.82.47.2/jxpgXsAction.do?oper=listWj', headers = head)
soup = BeautifulSoup(boom.text)

head['Content-Type'] = 'application/x-www-form-urlencoded'
head['Referer'] = 'http://211.82.47.2/jxpgXsAction.do'
head['Accept-Language'] = 'zh-CN'
head['Cache-Control'] = 'no-cache'
head['Accept'] = 'image/gif, image/jpeg, image/pjpeg, application/x-ms-application, application/xaml+xml, application/x-ms-xbap, */*'
head['Accept-Encoding'] = 'gzip, deflate'
head['User-Agent'] = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)'

for link in soup.find_all('img')[0:-5]:
    if link.get('title') == '查看':
        continue
    name = link.get('name')
    param = name.split('#@')
    wj = {
        'bpr': param[1],
        'bprm': param[2],
        'wjmc': param[3],
        'wjbz': 'null',
        'wjbm': param[0],
        'pgnrm': param[4],
        'pgnr': param[5],
        'pageSize': '20',
        'pageNo': '',
        'page': '1',
        'oper': 'wjShow',
        'currentPage': '1'
        }
    wj = parse.urlencode(wj, encoding='gb2312').encode()
    two = s.post('http://211.82.47.2/jxpgXsAction.do', data = wj, headers=head)
    
    data1 = {
       '0000000002': '5_1',
       '0000000003': '5_1',
       '0000000011': '6_1',
       '0000000012': '6_1',
       '0000000013': '6_1',
       '0000000014': '6_1',
       '0000000021': '6_1',
       '0000000022': '6_1',
       '0000000023': '6_1',
       '0000000024': '6_1',
       '0000000031': '6_1',
       '0000000032': '6_1',
       '0000000033': '6_1',
       '0000000034': '6_1',
       '0000000041': '6_1',
       '0000000042': '6_1',
       '0000000043': '6_1',
       'bpr': param[1],
       'pgnr': param[5],
       'wjbm': param[0],
       'wjbz': 'null',
       'xumanyzg': 'zg',
       'zgpj': '有教学经验'
    }
    data1 = parse.urlencode(data1, encoding='gbk').encode()
    three = s.post('http://211.82.47.2/jxpgXsAction.do?oper=wjpg', data=data1, headers = head)
    print(three.text)
"""
