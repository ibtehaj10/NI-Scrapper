from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests
import json
import time
import os
# Your Slack bot token
token = os.getenv('token')
channel_id = os.getenv('channel_id')
slack_token = token
client = WebClient(token=slack_token)
# token = os.getenv('token')
# channel_id = os.getenv('channel_id')
# The channel ID or name where you want to send the message
# channel_id = ""


def scraping():

    
    url = "http://127.0.0.1:8000/wallet-info/"
    
    payload = json.dumps({
      "wallet_name": "ni",
      "width": 200,
      "sort_by": "VTRUST"
    })
    headers = {
      'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    print(response.text)
    return response


# try:
    # Call the chat.postMessage method using the WebClient
while True:
    scrape = scraping().json()
    print(scrape)
    result = client.chat_postMessage(
        channel=channel_id,
        text="``` \n"+scrape[0]+"\n"+scrape[1]+"\nPowered by Replyτensor 🔥```"
    )
    print(f"Message sent successfully, ts: {result['ts']}")
    time.sleep(3600)
