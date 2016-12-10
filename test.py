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
http://211.82.47.2/jxpgXsAction.do

Referer: http://211.82.47.2/jxpgXsAction.do?oper=listWj

bpr: 0199134
bprm: %B7%AE%B4%E4%CF%E3
currentPage: 1
oper: wjResultShow
page: 1
pageNo: 
pageSize: 20
pgnr: Gb11011105
pgnrm: %C3%AB%D4%F3%B6%AB%CB%BC%CF%EB%BA%CD%D6%D0%B9%FA%CC%D8%C9%AB%C9%E7%BB%E1%D6%F7%D2%E5%C0%ED%C2%DB%CC%E5%CF%B5%B8%C5%C2%DB2
wjbm: 0000000012
wjbz: 
wjmc: %D1%A7%C9%FA%C6%C0%BD%CC
"""
