import discord
import asyncio
from config import Token
import requests
import json
# Bot token
TOKEN = Token
import time 
# Channel ID where you want to send the message
CHANNEL_ID = str('1194010924944740413')

# Message to send


def scraping():
  url = "http://localhost:5000/scrape"

  payload = json.dumps({})
  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  return response



# Create a bot instance
client = discord.Client()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    
    # Get the channel object by ID
    channel = client.get_channel(int(CHANNEL_ID))
    print(channel)
    while True :
      if channel:
          # Send the message
          scr = scraping()
          await channel.send(scr.text)
          print(f'Message sent to {channel.name} in {channel.guild.name}')
      else:
          print(f'Channel with ID {CHANNEL_ID} not found')
      time.sleep(10,800)

# Run the bot
client.run(TOKEN)
