import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states = [
        "user", "help", "show_fsm", "weapon_cate", "weapon_select", "weapon_details",
        "monster", "monster_size", "monster_info", "monster_finish"
    ],
    transitions = [
        {
            "trigger": "advance",
            "source": [
                "weapon_cate", "weapon_select",
                "monster", "monster_size", "monster_info"
            ],
            "dest": "user",
            "conditions": "is_going_back_user",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "show_fsm",
            "conditions": "is_going_to_fsm",
        },
        {
            "trigger": "advance",
            "source": [
                "user", "weapon_cate", "weapon_select", "weapon_details",
                "monster", "monster_size", "monster_info", "monster_finish"
            ],
            "dest": "help",
            "conditions": "is_going_to_help",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "weapon_cate",
            "conditions": "is_going_to_weapon_cate",
        },
        {
            "trigger": "advance",
            "source": "weapon_cate",
            "dest": "weapon_select",
            "conditions": "is_going_to_weapon_select",
        },
        {
            "trigger": "advance",
            "source": "weapon_select",
            "dest": "weapon_details",
            "conditions": "is_going_to_weapon_details",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "weapon_details",
            "conditions": "is_going_direct_weapon_details",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "monster",
            "conditions": "is_going_to_monster",
        },
        {
            "trigger": "advance",
            "source": "monster",
            "dest": "monster_size",
            "conditions": "is_going_to_monster_size",
        },
        {
            "trigger": "advance",
            "source": "monster_size",
            "dest": "monster_info",
            "conditions": "is_going_to_monster_info",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "monster_info",
            "conditions": "is_going_direct_monster_info",
        },
        {
            "trigger": "advance",
            "source": "monster_info",
            "dest": "monster_finish",
            "conditions": "is_going_to_monster_finish",
        },
        {
            "trigger": "go_back",
            "source": [
                "weapon_details", "monster_info", "monster_finish", "help", "show_fsm"
            ],
            "dest": "user"
        }
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "Not Entering any State")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)

