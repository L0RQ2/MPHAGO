from flask import Flask, request, jsonify
import sys
import json #meal/menu.json 파일 열기
import html #unescape
import datetime
import time
import requests, re


dustURL="http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureSidoLIst?serviceKey=A3wH%2Bbz48EN8bviBZePBIBRD8qMir%2BWsBTnjdg14Hi4zmPfpuaOCwp9pkQeMFYnuDO5n1hTQI8ft%2FDKMfaRt3g%3D%3D&numOfRows=1&pageNo=25&sidoName=%EC%84%9C%EC%9A%B8&searchCondition=HOUR&_returnType=json"

app = Flask(__name__)

@app.route('/haksa', methods=['POST'])
def haksa():
    f = open("haksa/haksa", 'r')
    haksadata = f.read()
    dataSend = {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "carousel": {
                    "type" : "basicCard",
                    "items": [
                            {
                            "title" : "",
                            "description" : str(haksadata)
                            }
                        ]
                    }
                }
            ]
        }
    }
    del(f)
    del(haksadata)
    return jsonify(dataSend)

@app.route('/meal', methods=['POST'])
def meal():
    content = request.get_json()
    content = content['userRequest']
    content = content['utterance']
    with open('menu/menu.json') as json_file:
        json_data = json.load(json_file)
    n=time.localtime().tm_mday
    menu=str(json_data[str(n)])
    menu=html.unescape(menu)
    menu=menu.replace("[", "")
    menu=menu.replace("]", "")
    menu=menu.replace("'", "")
    menu=menu.replace(",", "\n")
    menu=menu.replace(u"중식", u"\n중식")
    menu=menu.replace(u"석식", u"\n석식")
    dataSend = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "carousel": {
                        "type" : "basicCard",
                        "items": [
                            {
                                "title" : "",
                                "description" : str(menu)
                            }
                        ]
                    }
                }
            ]
        }
    }
    del(n)
    del(menu)
    return jsonify(dataSend)

@app.route('/dust', methods=['POST'])
def dust():
    response = requests.get(dustURL).text
    j=json.loads(response)
    j=j['list']
    j=str(j)
    dust = re.search("'pm10Value'.+?[0-9]'", j, re.I|re.S)
    dust=dust.group(0)
    dust = re.sub("'pm10Value': '", '', dust, 0, re.I|re.S)
    dust = dust.replace("'", "")
    answer=u"현재 미세먼지 농도 : " + str(dust)
    if(int(dust)<=30): moreanswer=u"미세먼지 농도가 '좋음' 입니다. \n좋아용용용"
    elif(int(dust)<=80): moreanswer=u"미세먼지 농도가 '보통' 입니다. \n그냥 그렇네용용용"
    elif(int(dust)<=150): moreanswer=u"미세먼지 농도가 '나쁨' 입니다. \n마스크 챙기세용용용"
    else: moreanswer=u"미세먼지 농도가 '매우나쁨' 입니다. \n마스크를 챙기시고 외부활동도 삼가해주세용용용"
    dataSend = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "carousel": {
                        "type" : "basicCard",
                        "items": [
                            {
                                "title" : "",
                                "description" : str(answer + "\n\n" + moreanswer)
                            }
                        ]
                    }
                }
            ]
        }
    }
    return jsonify(dataSend)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
