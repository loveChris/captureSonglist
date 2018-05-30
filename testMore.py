# coding:utf-8

import MySQLdb
import requests,re
from urllib import urlencode

def songlist(n,sort):
    db = MySQLdb.connect("localhost", "root", "123456", "songlist",charset="utf8")
    cursor = db.cursor()
    sorting = {"cat": sort}
    sorting = urlencode(sorting)
    # sql = "select songlist_id from songlist_name;"
    # cursor.execute(sql)
    # ids = cursor.fetchall()
    for i in range(n):
        d = i * 35
        url = "http://music.163.com/discover/playlist/?order=hot&%s&limit=35&offset=%d" % (sorting,d)
        kv = {"User-Agent": "Mozilla/5.0",
              "Host": "music.163.com",
              "Referer": "http://music.163.com/",
              "Upgrade-Insecure-Requests": "1",
              "Accept": "text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8",
              "Accept - Encoding": "gzip, deflate",
              "Accept - Language": "zh - CN, zh;q = 0.9",
              "Connection": "keep - alive"
              }
        r = requests.get(url, headers=kv)
        response = r.text
        # with open("html.txt", "w")as f:
        #     f.write(response.encode("utf-8"))

        names = re.findall(r'(?<=title=).*?(?=class="msk")', response)
        # print len(names)
        # for i in range(len(names)):
        #     print names[i].encode("utf-8")
        # listnames = []
        # ids = []
        for j in range(len(names)):
            listname = re.findall(r'(?<=").*?(?=" href)', names[j])
            # listname =  listname[0].encode("utf-8")
            # print listname
            # listnames.append(listname[0])
            id = re.findall(r'(?<=href="/playlist\?id=).*?(?=")', names[j])
            # print id[0]
            # sql = "select songlist_id from songlist_name;"
            # cursor.execute(sql)
            # ids = cursor.fetchall()
            # x = 0
            # for m in range(len(ids)):
            #     if long(id[0]) == ids[m][0]:
            #         # print ids[m][0]
            #         x = 1
            #         break
            #     else:
            #         x = 0
            # if x == 1:
            #     continue
            # print "AAA"

            sql = """INSERT INTO songlist_name(songlist_id,songlist_name,sorting,create_date)
                     VALUES ('%s', '%s', "%s", CURDATE())
                     ON DUPLICATE KEY UPDATE songlist_name='%s',sorting='%s',update_date=now(); 
            """ % (id[0],MySQLdb.escape_string(listname[0]),MySQLdb.escape_string(sort),MySQLdb.escape_string(listname[0]),MySQLdb.escape_string(sort))
            cursor.execute(sql)
            # songlist = cursor.fetchone()
            db.commit()
    cursor.close()
    db.close()


def getN(sort):
    sorting = {"cat": sort}
    sorting = urlencode(sorting)

    url = "http://music.163.com/discover/playlist/?order=hot&%s&limit=35&offset=0" % sorting
    kv = {"User-Agent": "Mozilla/5.0",
          "Host": "music.163.com",
          "Referer": "http://music.163.com/",
          "Upgrade-Insecure-Requests": "1",
          "Accept": "text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8",
          "Accept - Encoding": "gzip, deflate",
          "Accept - Language": "zh - CN, zh;q = 0.9",
          "Connection": "keep - alive"
          }
    r = requests.get(url, headers=kv)
    response = r.text
    with open("html.txt", "w")as f:
        f.write(response.encode("utf-8"))

    n = re.findall(r'(?<=class="zpgi">).*?(?=</a>)', response)
    return n[-1]

def getSort():
    db = MySQLdb.connect("localhost", "root", "123456", "songlist", charset="utf8")
    cursor = db.cursor()
    sql = "select sortingname from songlist_type;"
    cursor.execute(sql)
    sorting = cursor.fetchall()
    db.close()
    return sorting





if __name__ == '__main__':
    # songlist(1,"华语")
    sorting = getSort()
    # print type(len(sorting))
    for i in range(len(sorting)):
        sort = str(sorting[i][0])
        n = int(getN(sort))
        # print type(n)
        songlist(n,sort)


































