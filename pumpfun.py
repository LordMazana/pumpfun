import discord
import requests
import asyncio
import os

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

latest_ids = set()

async def fetch_new_coins():
    global latest_ids
    while True:
        try:
            response = requests.get("https://pump.fun/board")
            if response.status_code == 200:
                data = response.text
                found = set()
                for line in data.splitlines():
                    if 'pubkey' in line:
                        start = line.find('"pubkey":"') + 10
                        end = line.find('"', start)
                        pubkey = line[start:end]
                        if pubkey:
                            found.add(pubkey)

                new_coins = found - latest_ids
                if new_coins:
                    channel = client.get_channel(CHANNEL_ID)
                    for coin in new_coins:
                        await channel.send(f"?? New Pump.fun token: https://pump.fun/{coin}")
                    latest_ids = found

        except Exception as e:
            print(f"Error: {e}")
        await asyncio.sleep(30)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    client.loop.create_task(fetch_new_coins())

client.run(TOKEN)

