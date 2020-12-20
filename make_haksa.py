import requests, re, json, sys
import datetime
now=datetime.datetime.now()
URL="http://mmhs.hs.kr/66333/subMenu.do?srhSchdulYear="+str(now.year)+"&srhSchdulMonth="+str(now.month)

response = requests.get(URL).text

data = response[response.find("<tbody>"):response.find("</tbody>")]

data= re.sub('<.+?>', '', data, 0, re.I|re.S)
data=re.sub('&nbsp;|\t|\r|\n', '', data)
data_split=data.split()
day=1;
for i in range(0, len(data_split)):
    if(str(data_split[i])==str(day)):
        data_split[i]="\n"+data_split[i]
        day+=1
data=" ".join(data_split)
print(data)
f = open("/workspace/MMBOT/haksa/haksa", 'w')
f.write(data)
