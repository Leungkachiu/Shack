from slack_sdk import WebClient
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

client = WebClient(token=os.environ['SLACK_TOKEN'])

app = Flask(__name__)
print(os.environ['SIGNING_SECRET'])
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],"/slack/events",app)
BOT_ID = client.api_call("auth.test")['user_id']

@slack_event_adapter.on("message")
def message(payload):
    print("payload")
    print(payload)
    event = payload.get("event",{})
    channel = event.get("channel")
    text = event.get("text")
    user_id = event.get("user")
    if BOT_ID != user_id:
        client.chat_postMessage(channel=channel, text=text)
# client.chat_postMessage(channel="#test", text="Hello World!")

if __name__  == "__main__":
    app.run(debug=True)