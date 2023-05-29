from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import requests

def checkword(w):
    url = 'https://www.moedict.tw/uni/' + w
    r = requests.get(url)
    datas = r.json()
    msg = '國字：' + datas['title'] + '\n'
    msg += '部首：' + datas['radical'] + '\n'
    msg += '筆劃：' + str(datas['stroke_count']) + '\n\n'
    for i in range(len(datas['heteronyms'])):
        msg += '注音：' + datas['heteronyms'][i]['bopomofo'] + '\n'
        msg += '拼音：' + datas['heteronyms'][i]['pinyin'] + '\n'    
        for j in range(len(datas['heteronyms'][i]['definitions'])):
            if 'type' in datas['heteronyms'][i]['definitions'][j]:
                msg += '[{}] {}\n'.format(
                    datas['heteronyms'][i]['definitions'][j]['type'],
                    datas['heteronyms'][i]['definitions'][j]['def'])
        msg += '\n'
    return msg

w = input("請輸入要查詢的國字：")
print(checkword(w))

app = Flask(__name__)

line_bot_api = LineBotApi('hVNo5whxVZWXufJ6fZUVIxehhZgaHCI/fLZO6n6XvtROAJ7nd24pZc5dkfBKpoE3gsOvCuCf9O2cWHkyxZ3F/Yypc67sRDQa5LJZzHNj1Jl//hZRrUKw+da3ZfOolfWry+scnGuuIrZ1LF3G9MVsDgdB04t89/1O/w1cDnyilFU=')
handler1 = WebhookHandler('307a3b53c479abc1ff791bf7b09ae3a8')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler1.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler1.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=checkword(event.message.text)))

if __name__ == "__main__":
    app.run()
