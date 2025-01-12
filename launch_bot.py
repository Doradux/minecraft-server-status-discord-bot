import discord
from discord import Status
from discord.ext import tasks
from discord import CustomActivity
from mcstatus import JavaServer
import os

#discord bot token
DISCORD_TOKEN = ""
#minecraft server ip
MINECRAFT_HOST = ""

#discord client
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# getting the minecraft server status
def get_minecraft_status():
    try:
        server = JavaServer.lookup(MINECRAFT_HOST)
        status = server.status()
        return {
            "online": True,
            "players_online": status.players.online,
        }
    except Exception:
        return {"online": False}


@client.event
async def on_ready():
    print(f"Bot conectado como {client.user}")
    update_status.start()

#update the bot status every minute
@tasks.loop(minutes=1)
async def update_status():
    status = get_minecraft_status()
    #if the server is online
    if status["online"]:
        #update the bot status to online
        await client.change_presence(activity = CustomActivity(name="Online ✅", emoji="✅"), status=Status.online)
    #if the server is offline
    else:
        #update the bot status to offline
        await client.change_presence(activity = CustomActivity(name="Offline ❌", emoji="❌"), status=Status.dnd)

#run the bot
client.run(DISCORD_TOKEN)
