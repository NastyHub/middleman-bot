import discord
import os
import json
from discord.ext import commands, tasks
import time
import asyncio

client = commands.Bot(command_prefix = '$')
client.remove_command('help')

##########################################################################

#SERVER INFO
ownerid = 605217750847062049

channel_list = {
    "auction" : 0,
}

category_list = {
    "help" : 0,
    "mm" : 0
}
##########################################################################

#USEFUL FUNCTIONS
def joinlist(thislist):
    x = ""
    for i in thislist:
        x += i
    return x

def formatmoney(money):
    strmoney = str(money)
    storagelist = []

    lengthofmoney = len(strmoney)

    if lengthofmoney < 4:
        return strmoney
    else:
        mok = lengthofmoney//3
        namoji = lengthofmoney%3

        for i in strmoney:
            storagelist.append(i)
        
        bait = 1

        if bait == 0 and mok == 1:
            storagelist.insert(namoji, ",") #first comma insert

            complete = joinlist(storagelist)

            return complete
        else:
            while bait == mok:
                if bait == 0:
                    storagelist.insert(namoji, ",") #first comma insert
                    bait += 1
                else:
                    mok = mok + 4
                    storagelist.insert(mok, ",")
                    bait += 1
            complete = joinlist(storagelist)
            return complete



@client.event
async def on_ready():
    game = discord.Game(name = "판매 돕는 중")
    await client.change_presence(activity = game)

    print("Ready to Run")

##########################################################################
#OWNER ONLY

@client.command(aliases=["경매생성"])
async def postauction(ctx, ):
    print("Hi")


client.run("ODk2MzY4NTk1ODA0NzgyNjQy.YWGGTg.7AUnthC-deNyobLAGf8FjPRwoSk")