from flask import Flask, request, jsonify
import sys
import json #meal/menu.json 파일 열기
import html #unescape
import datetime
import time

with open('menu/menu.json') as json_file:
    json_data = json.load(json_file)

f = open("haksa/haksa", 'r')
haksadata = f.read()

app = Flask(__name__)

@app.route('/haksa', methods=['POST'])
def haksa():    
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
    return jsonify(dataSend)

@app.route('/meal', methods=['POST'])
def meal():
    n=time.localtime().tm_mday
    content = request.get_json()
    content = content['userRequest']
    content = content['utterance']
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
    return jsonify(dataSend)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
