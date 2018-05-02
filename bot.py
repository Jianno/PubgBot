import requests
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import logging
import time
import json

logging.basicConfig(level=logging.INFO)


Client = discord.Client()
client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
        print("Bot online")


@client.command()
async def lastgame(name: str):
    stat = lastMatchStats(name)
    response = "Stats for " + name + "'s last game \n"+"Place: "+str(stat[4])+"\nKills: "+str(stat[0])+"\nHeadshot kills: "+str(stat[1])+"\nAssists: "+str(stat[2])+"\nDamage Dealt: "+str(stat[3])
    await client.say(response)

@client.command()
async def seasonstats(name: str, game: str):
    playerStats = seasonStats(name, game)
    response = "Season stats for " + name + " in " + game + "-fpp:" + "\nWins: " + str(playerStats[0]) + "\nTop 10's: " + str(playerStats[1]) +"\nKills: " + str(playerStats[2]) + "\nHeadshot Kills: " + str(playerStats[3]) + "\nDamage Dealt: " + str(playerStats[4]) + "\nHighest Kill Game: " + str(playerStats[5])          
    await client.say(response)

def seasonStats(name, gametype):
    seasonId = "division.bro.official.2018-04"
    idMap = {}
    stats = [0] * 6
    idMapFile = "idMap.json"
    playerId = 0
    header = {
        "Authorization": "PUBG API KEY HERE",
        "Accept": "application/vnd.api+json"
        } 
    
    with open(idMapFile) as f:
        idMap = json.load(f)

    if name in idMap:
        playerId = idMap.get(name)
    else:
        urlPlayer = "https://api.playbattlegrounds.com/shards/pc-na/players?filter[playerNames]="+name  
        rPlayer = requests.get(urlPlayer, headers=header)
        playerId = rPlayer.json().get('data')[0].get('id')
        idMap[name] = playerId
        with open(idMapFile, 'w') as f:
            json.dump(idMap, f)

    statsURL = "https://api.playbattlegrounds.com/shards/pc-na/players/"+playerId+"/seasons/division.bro.official.2018-04"
    rStats = requests.get(statsURL, headers=header)
    jsonStats = rStats.json().get('data').get("attributes").get("gameModeStats").get(gametype+"-fpp")
    stats[0] = jsonStats.get('wins')
    stats[1] = jsonStats.get('top10s')
    stats[2] = jsonStats.get('kills')
    stats[3] = jsonStats.get('headshotKills')
    stats[4] = jsonStats.get('damageDealt')
    stats[5] = jsonStats.get('roundMostKills')    
           
    return stats
        
    
        
        

def lastMatchStats(name): 
    urlPlayer = "https://api.playbattlegrounds.com/shards/pc-na/players?filter[playerNames]="+name
    header = {
        "Authorization": "PUBG API KEY HERE",
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



client.run("DISCORD TOKEN HERE")
