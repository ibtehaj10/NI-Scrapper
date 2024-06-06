from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests
import json
import time
# Your Slack bot token
slack_token = ""
client = WebClient(token=slack_token)

# The channel ID or name where you want to send the message
channel_id = ""


def scraping():
    url = "http://135.181.63.160:5088/scrape"

    payload = json.dumps({})
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response

# try:
    # Call the chat.postMessage method using the WebClient
while True:
    scrape = scraping().text
    print(scrape)
    result = client.chat_postMessage(
        channel=channel_id,
        text=scrape
    )
    print(f"Message sent successfully, ts: {result['ts']}")
    time.sleep(3600)