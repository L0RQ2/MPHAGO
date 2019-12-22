import requests, re, json, sys
import datetime

now=datetime.datetime.now()
URL="https://stu.sen.go.kr/sts_sci_md00_001.do?schulCode=B100000430&schulCrseScCode=4&schYmd="+str(now.year)+"."+str(now.month)+"."+str(now.day)

response = requests.get(URL).text

data = response[response.find("<tbody>"):response.find("</tbody>")]

#정규표현식으로 데이터 가공
regex = re.compile(r'[\n\r\t]')
data=regex.sub('',data)
rex = re.compile(r'<div>(.*?)</div>', re.S|re.M)
data=rex.findall(data)

file_json={}
for dat in data:
    date=re.findall(r"[0-3][0-9]",dat[0:2])
    menu=dat[dat.find("[조식]<br />"):]
    if not date:
        date=dat[0:1]
        if date == "" or date == " ":
            continue
    if type(date) == list:
        date=date[0]
    menu = menu.split("<br />")
    file_json.update({date : menu})
##Json 생성
for i in range(1, len(file_json)+1):
    if(len(file_json[str(i)])==1):
        file_json[str(i)]=u"오늘의 급식정보가 존재하지 않습니다."
with open('menu/menu.json', 'w', encoding='utf-8') as outfile:
       json.dump(file_json, outfile, sort_keys = False, indent=4, ensure_ascii=0)

    
