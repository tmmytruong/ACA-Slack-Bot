import logging 
from dotenv import load_dotenv 
from slack_bolt import App 
from slack_bolt.adapter.socket_mode import SocketModeHandler 

logging.basicConfig(level=logging.INFO)
load_dotenv()

SLACK_BOT_TOKEN = "xoxb-3869766030389-3885369170321-eC7mF9dAWN0teKJ2s8DSaGot"
SLACK_APP_TOKEN = "xapp-1-A03RKNLKMFF-3866110875814-f8a1b5f55ca66318ea584eedfca056c2158aa14c15f296af66f3e2f5f05199b8"

app = App(token=SLACK_BOT_TOKEN)

@app.event("app_mention")
def mention_handler(body, context, payload, options, say, event):
    say("Hello World!")

@app.event("message")
def message_handler(body, context, payload, options, say, event):
    pass

if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()