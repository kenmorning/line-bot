from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('qk3MN1yXSP6vHQlcVuQX62Ip5dakDemCwTWMlQnnuAQMWTWxCWZrIJ6Q8615nSSkq+QBxczS1Xd+F4VA8L0U1w3jjP+GDs9fuIrRrEPbDALBTU7EWaVTT1XZApheDC+KEdUuCyMnChDNIYpZD1AHaAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f4710932e68162cff0686d4dfbe5c966')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text 
    r = '很抱歉，你說什麼'
    
    if '給我貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='2',
            sticker_id='23'
        )

        line_bot_api.reply_message(
            event.reply_token,
            sticker_message)
        return # 回傳空值，不執行下面

    if msg in ['hi', 'Hi']: # 用清單檢查
        r = '嗨'
    elif msg == '你吃飯了嗎':
        r = '還沒'
    elif msg == '你是誰':
        r = '我是機器人'
    elif '訂位' in msg: # 訂位出現在訊息中的話
        r = '您想訂位，是嗎？'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()