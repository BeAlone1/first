import requests
from urllib import parse
from bs4 import BeautifulSoup

s = requests.Session()
zjh = '140809011237'
mm= '207430'
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

s.headers["Accept-Language"]="zh-CN,zh;q=0.8"
s.headers['Accept']="text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
s.headers["User-Agent"]="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"
s.headers["Connection"]="keep-alive"
#s.headers['Referer']= "http://211.82.47.2/"

one = s.post('http://211.82.47.2/loginAction.do', data = postdata)
print('1')
aa = s.get('http://211.82.47.2/xkAction.do')
print('2')

#s.headers['Referer']  = 'http://211.82.47.2/xkAction.do'
s.get('http://211.82.47.2/xkAction.do?actionType=3&pageNumber=-1')
print('3')

wj = {
    'actionType': '9',
    'kcId': 'Gw00551203_01',
    'preActionType': '3'
    }
s.headers['Referer'] = 'http://211.82.47.2/xkAction.do?actionType=3&pageNumber=-1'
s.headers['Content-Type'] = 'application/x-www-form-urlencoded'
wj = parse.urlencode(wj, encoding='gb2312').encode()
res = s.post('http://211.82.47.2/xkAction.do', data = wj)
print('4')
print(res.text)

