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
'auto_07DRrfFEBG','auto_ilJp9a8nZk','auto_1qrXY7YfC5','auto_HsKQGNCURr']
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

def send(sock, msgstr):
    msg=msgstr
    data_length= len(msg)+8
    code=689
    #msgHead=int.to_bytes(data_length,4,'little')+int.to_bytes(data_length,4,'little')+int.to_bytes(code,4,'little')
    msgHead=struct.pack("<l",data_length)+struct.pack("<l",data_length)+struct.pack("<l",code)
    sock.send(msgHead)
    sent=0
    sock.send(msg.encode())
        
if __name__ == '__main__':
    serv = GetServer()
    
    sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((serv['ip'], int(serv['port'])))
    devid=uuid.uuid1().hex.swapcase()
    rt=str(int(time.time()))
    hashvk = hashlib.md5()
    vk=rt+'7oE9nPEG9xXV69phU31FYCLUagKeYtsF'+devid
    hashvk.update(vk.encode('utf-8'))
    vk = hashvk.hexdigest()
    gid=''
    msg='type@=loginreq'\
    +'/username@='+users[2]\
    +'/ct@=0'\
    +'/password@='+passes[2]\
    +'/roomid@='+serv['room_id']\
    +'/devid@='+devid\
    +'/rt@='+rt\
    +'/vk@='+vk\
    +'/ver@=20150929'\
    +'/\x00'
    send(sock, msg)
    recv = sock.recv(1024)
    print(recv)
    msg1 = 'type@=qrl/'\
           +'rid@=' + serv['room_id']\
           +'/et@=0'\
           + '/\x00';
    send(sock,msg1)
    recv1 = sock.recv(1024)
    uid = recv.split(b'/')[1][8:].decode('utf-8')
    l = recv1.split(b'/')
    for g in range(len(l)):
        if l[g][:5] == b'gid@=':
            serv['gid'] = l[g][5:].decode('utf8')
            break;
    sock.close()
    sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r = sock1.connect(('danmu.douyutv.com', 8601))
    msg = 'type@=loginreq/'\
          +'username@=' + users[0]\
          +'/password@=' + passes[0]\
          +'/roomid@=' + serv['room_id']\
          +'/\x00'
    send(sock1, msg)
    rec = sock1.recv(1024)
    msg = 'type@=joingroup/'\
          +'rid@=' + serv['room_id']\
          +'/gid@=' + serv['gid']\
          +'/\x00'
    send(sock1, msg)
    time.clock()
    sign = 0
    while 1:
        rec = sock1.recv(1024)
        if re.search(b'chatmsg', rec):
            try:
                nn  = re.search(b'nn@=.*?/', rec).group()[4:-1].decode('utf-8')
                txt = re.search(b'txt@=.*?/', rec).group()[5:-1].decode('utf-8')
            except:
                pass
            nnum = 0
            for b in nn:
                if b >= u'\u4e00' and b <= u'\u9fa5':
                    nnum += 1
            try:
                print(nn, ' '*(17-len(nn)-nnum),'：',txt)
            except:
                print('****************\n     解码异常      \n*********************')
            if int(time.clock())/40!=sign :
                sign = int(time.clock())/40
                msg  = 'type@=keeplive/'\
                +'tick@=' + str(int(time.time()))\
                +'/\x00'
                send(sock1,msg)
