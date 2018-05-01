import requests
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO)


Client = discord.Client()
client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
        print("Bot online")


@client.command(pass_context = True)
async def lastgame(message: str, name):
    stat = lastMatchStats(name)
    response = "Stats for " + name + "'s last game \n"+"Place: "+str(stat[4])+"\nKills: "+str(stat[0])+"\nHeadshot kills: "+str(stat[1])+"\nAssists: "+str(stat[2])+"\nDamage Dealt: "+str(stat[3])
    await client.say(response)
        
    

def lastMatchStats(name):
    urlPlayer = "https://api.playbattlegrounds.com/shards/pc-na/players?filter[playerNames]="+name
    header = {
        "Authorization": "PUBG API KEY GOES HERE",
        "Accept": "application/vnd.api+json"
    }

    rPlayer = requests.get(urlPlayer, headers=header)
    matchid = (rPlayer.json().get('data')[0].get('relationships').get('matches').get('data')[0].get('id'))	
    urlMatch = "https://api.playbattlegrounds.com/shards/pc-na/matches/" + matchid
    rMatch = requests.get(urlMatch, headers=header)
    
    rMatchArray = rMatch.json().get('included')
    stat = [0] * 5
    for x in rMatchArray:
        current = x
        if("participant" in current.values()):
            stats = current.get('attributes').get('stats')
            if(name in stats.values()):
                print(stats.get('kills'))
                stat[0] = stats.get('kills')
                stat[1] = stats.get('headshotKills')
                stat[2] = stats.get('assists')
                stat[3] = stats.get('damageDealt')
                stat[4] = stats.get('winPlace')
          
    return stat



client.run("Discord Token here")
