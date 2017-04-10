import urllib.request as req
import urllib.parse   as p
import time
import socket
import re
import hashlib
import uuid
import struct
import threading

global users
global passes
global realname

realname=['1234再来一次1234','橙汁美味','不吃素菜','我准备好了饿','英雄联盟王者无敌','惜城呦','江左梅郎通过弹幕','换取信任','怎么回事ibuq','请你安静点ye']
users=['auto_F3Z8pi0b1G','auto_J7fRnnfxm7','auto_GmQ77715Np','auto_I6HIDW3ER4','auto_QiJGklM5ZB','auto_3pSaH7yJhu',\
'auto_07DRrfFEBG','auto_ilJp9a8nZk','auto_1qrXY7YfC5','auto_HsKQGNCURr','45239882']
passes=['200820e3227815ed1756a6b531e7e0d2','200820e3227815ed1756a6b531e7e0d2',\
'd0dcbf0d12a6b1e7fbfa2ce5848f3eff','200820e3227815ed1756a6b531e7e0d2','200820e3227815ed1756a6b531e7e0d2','d0dcbf0d12a6b1e7fbfa2ce5848f3eff',\
'd0dcbf0d12a6b1e7fbfa2ce5848f3eff','200820e3227815ed1756a6b531e7e0d2','200820e3227815ed1756a6b531e7e0d2','200820e3227815ed1756a6b531e7e0d2']

def GetServer():
    server = dict()
    roomid = input('房间号：')
    url    = 'http://www.douyu.com/' + str(roomid)
    req1   = req.Request(url)
    req1.add_header('User-Agent',"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0")
    res    = req.urlopen(req1)
    html   = res.read().decode('utf-8')
    html   = p.unquote(html)
    a = re.search(r'server_config":".+?","def', html)
    server['ip']   = re.search(r'"ip":".+?"',a.group()).group()[6:-1]
    server['port'] = re.search(r'"port":"\d+?"',a.group()).group()[8:-1]
    server['room_id'] = re.search(r'room_id=\d+"', html).group()[8:-1]
    return server

def dynamicSend(serv):
    sock = []
    uid  = []
    gid  = []
    
    for num in range(len(users)):
        sock.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        sock[num].connect((serv['ip'], int(serv['port'])))
        devid=uuid.uuid1().hex.swapcase()
        rt=str(int(time.time()))
        hashvk = hashlib.md5()
        vk=rt+'7oE9nPEG9xXV69phU31FYCLUagKeYtsF'+devid
        hashvk.update(vk.encode('utf-8'))
        vk = hashvk.hexdigest()
        msg='type@=loginreq'\
        +'/username@='+users[num]\
        +'/ct@=0'\
        +'/password@='+passes[num]\
        +'/roomid@='+serv['room_id']\
        +'/devid@='+devid\
        +'/rt@='+rt\
        +'/vk@='+vk\
        +'/ver@=20150929'\
        +'/\x00'
        send(sock[num], msg)
        recv = sock[num].recv(1024)
        print(num)
        print(recv)
        uid.append(re.search(b'rid@=.*?/', recv).group()[6:-1].decode('utf8'))
        msg1 = 'type@=qrl/'\
                +'rid@=' + serv['room_id']\
                +'/et@=0'\
                + '/\x00';
        send(sock[num],msg1)
        recv = sock[num].recv(1024)
        
        gid.append(re.search(b'gid@=.*?/', recv).group()[5:-1].decode('utf8'))
        msg = 'type@=qtlnq/\x00'
        send(sock[num], msg)
        #print(uid[num])
        msg = 'type@=reqog/'\
              +'uid@=' + uid[num] \
              +'/\x00'
        send(sock[num], msg)
        
    while 1:
        content = input('消息(输入￥重新选择房间)：')
        if content == '￥':
            for num in range(len(users)):
                sock[num].close()
            break
        content = content.encode('utf8').decode('utf8')
        for num in range(len(users)):
            msg = 'type@=chatmessage/' +\
                  'receive@=0/' + \
                  'content@='+ content +\
                  '/scope@=/col@=0/\x00'
            send(sock[num], msg)
        time.sleep(1)
            
def send(sock, msgstr):
    msg = msgstr
    msg = msg.encode('utf8')
    data_length = len(msg)+8
    code=689
    #msgHead=int.to_bytes(data_length,4,'little')+int.to_bytes(data_length,4,'little')+int.to_bytes(code,4,'little')
    msgHead=struct.pack("<l",data_length)+struct.pack("<l",data_length)+struct.pack("<l",code)
    sock.send(msgHead)
    sock.send(msg)
        
if __name__ == '__main__':
    while 1:
        serv = GetServer()
        print(serv)
        rid  = dynamicSend(serv)

    
                
                

















            
