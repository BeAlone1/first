from tornado import httpclient

class myclient:
    def __init__(self):
        self.head = {
            "Accept-Language":"zh-CN,zh;q=0.8",
            'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
            "Connection":"keep-alive"
        }
        self.postdata = b'evalue=&zjh1=&zjh=%s&fs=&v_yzm=&lx=&mm=%seflag=&dzslh=&tips=' % (zjh.encode(),mm.encode())
    def fetch(self, url, postdata = None):
        if not postdata:
            req = httpclient.HTTPRequest(url, 'GET', self.head)
        else:
            req = httpclient.HTTPRequest(url, 'POST', self.head, postdata)

        res = httpclient.HTTPClient().fetch(req)
        cookie = res.headers.get('Set-Cookie')
        if cookie:
            self.head['Cookie'] = cookie
        return res
zjh = '150809031144'
mm = '250310'
zjh = '140809011223'
mm = '050419'
data = b'evalue=&zjh1=&zjh=%s&fs=&v_yzm=&lx=&mm=%s&eflag=&dzslh=&tips=' % (zjh.encode(),mm.encode())
my = myclient()
res = my.fetch('http://211.82.47.2/loginAction.do', postdata = data)
res = my.fetch('http://211.82.47.2/gradeLnAllAction.do?type=ln&oper=lnjhqk')
del my
ig = res.body.decode('gbk')
print(ig)
"""

head = {
            "Accept-Language":"zh-CN,zh;q=0.8",
            'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
            "Connection":"keep-alive"
        }
data = b'evalue=&zjh1=&zjh=140809011223&fs=&v_yzm=&lx=&mm=050419&eflag=&dzslh=&tips='
client = httpclient.HTTPClient()
req = httpclient.HTTPRequest('http://211.82.47.2/loginAction.do', 'POST', head, data)
res = client.fetch(req)

url = 'http://211.82.47.2/gradeLnAllAction.do?type=ln&oper=fainfo&fajhh=1748'
Cookie = res.headers.get('Set-Cookie')
head['Cookie'] = Cookie

req = httpclient.HTTPRequest(url, headers = head)
res = client.fetch(req)
ig = res.body.decode('gbk')
print(ig)"""
