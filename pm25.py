import asyncio
import time
import aiohttp
import urllib.parse as parse
import pymysql as sql
import json
import requests
from lxml import etree

def getNow():
    header = {'Connection':'keep-alive',
              'Content-Type':'application/x-www-form-urlencoded',
              'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    }
    ret = requests.get('http://datacenter.mep.gov.cn:8099/ths-report/report!list.action?xmlname=1462261004631', headers = header)
    html = etree.HTML(ret.text)
    json_data = html.xpath('//*[@id="gisDataJson"]')[0].get('value')
    load = json.loads(json_data)
    ret_time =  load[0]['OPER_DATE']
    return ret_time[:ret_time.index(':')]

async def getdata(num, pm_data):
    header = {'Connection':'keep-alive',
              'Content-Type':'application/x-www-form-urlencoded',
              'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    }
    postdata = {'page.pageNo': num,
                'xmlname':'1462261004631'
    }
    
    async with aiohttp.post('http://datacenter.mep.gov.cn:8099/ths-report/report!list.action', \
                            data = parse.urlencode(postdata, encoding='utf8').encode(), headers = header) as r:
        pm_data.append(await r.text())

def main(pm_data):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [getdata(i,  pm_data) for i in range(1, 14)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

if "__main__" == __name__:
    pm_data = []
    db = sql.connect(host='127.0.0.1', user='root', password='root', port=3306, database='pm2_5', charset='utf8')
    cur = db.cursor()
    while 1:
        exe = cur.execute('SELECT date_format(time, "%c/%e/%Y %k") FROM allcity where id = (SELECT max(id) FROM allcity)')
        if exe != 0:
            exe_time = cur.fetchone()[0]
            while 1:
                try:
                    ret_time = getNow()
                except:
                    print("getNow except")
                    time.sleep(500)
                    
                    cur.execute('select * from allcity where id = 1')
                else:
                    break
        if exe==0 or exe_time != ret_time:
            if exe != 0:
                print('exe_time: \"' + exe_time + '\"  ret_time: \"' + ret_time + '\"')
                if exe_time.split(' ')[0] != ret_time.split(' ')[0]:
                    cur.execute('TRUNCATE allcity;')
                    db.commit()
            pm_data.clear()
            main(pm_data)
            for i in range(len(pm_data)):
                html = etree.HTML(pm_data[i])
                json_data = html.xpath('//*[@id="gisDataJson"]')[0].get('value')
                load = json.loads(json_data)
                for j in range(len(load)):
                    cur.execute('insert into allcity values(null, "%s", "%s", "%s", str_to_date("%s","%%m/%%d/%%Y %%H:%%i:%%s"))' % (load[j]['CITY'], load[j]['AQI'], load[j]['STATUS'], load[j]['OPER_DATE']))
            db.commit()
            print('seccess!')
        print('time to sleep!')
        time.sleep(200)
        

        
