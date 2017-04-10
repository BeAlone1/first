import requests
import time 
import json
import threading
class basic(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.appID = 'wx18753eacb62ef5ff'
        self.appSecret = '6d4019d46a58376a91f96f3f176e7f64'
        self.__leftime = 0
	
        self.AccessToken = ''
        self.getTokenUrl = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (self.appID, self.appSecret)
        self.AccessTokenUrl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % self.AccessToken
    def run(self):
        while 1:
            if self.__leftime > 10:
                time.sleep(2)
                self.__leftime -= 2
            else:
                self.getToken()
                self.CreatMenu()
    def getToken(self):
        res = requests.get(self.getTokenUrl)
        infor = json.loads(res.text)
        res.close()
        self.__leftime = infor['expires_in']
        self.AccessToken = infor['access_token']
        print(res.text)
    def CreatMenu(self):
        postJson = """
            {
                "button":
                [
                    {
                        "type": "click",
                        "name": "开发指引",
                        "key":  "mpGuide"
                    },
                    {
                        "name": "公众平台",
                        "sub_button":
                        [
                            {
                                "type": "view",
                                "name": "更新公告",
                                "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1418702138&token=&lang=zh_CN"
                            },
                            {
                                "type": "view",
                                "name": "接口权限说明",
                                "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1418702138&token=&lang=zh_CN"
                            },
                            {
                                "type": "view",
                                "name": "返回码说明",
                                "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1433747234&token=&lang=zh_CN"
                            }
                        ]
                    }
                  ]
            }"""
        postData = postJson.encode('utf8')
        res = requests.post(self.AccessTokenUrl, data = postData)
        print(res.text)
        res.close()
if '__main__' == __name__:
    basic().start()
