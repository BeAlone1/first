import struct
import socket

domain = input()

domain = domain.split('.')
start = '3e3a01000001000000000000'
end = '0000010001'
for item in domain:
    item_len = len(item)
    tmp = '0'+str(item_len) if item_len < 10 else str(item_len)
    start = start + tmp
    for i in range(item_len):
        start += hex(ord(item[i]))[2:]
start = start + end

hex_list = [start[i:i+2] for i in range(0, len(start), 2)]

all_strs = b''
for cur_item in hex_list:
    all_strs += struct.pack('B', int(cur_item, 16))
dns = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

dns.sendto(all_strs, ('202.99.192.66', 53))

ret = dns.recvfrom(1024)[0]

print(ret)

print(str(ret[-4]) + '.' + str(ret[-3])+ '.' +str(ret[-2])+ '.' +str(ret[-1]))
