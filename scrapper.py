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



url = "http://localhost:5000/scrape"

payload = json.dumps({})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)


MESSAGE = response.text
# Create a bot instance
client = discord.Client()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    
    # Get the channel object by ID
    channel = client.get_channel(int(CHANNEL_ID))
    print(channel)
    
    if channel:
        # Send the message
        await channel.send(MESSAGE)
        print(f'Message sent to {channel.name} in {channel.guild.name}')
    else:
        print(f'Channel with ID {CHANNEL_ID} not found')

# Run the bot
client.run(TOKEN)
