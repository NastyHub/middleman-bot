import discord
import os
import json
from discord.ext import commands, tasks
import time
import asyncio

client = commands.Bot(command_prefix = '$')
client.remove_command('help')

##########################################################################
#generalrole = discord.utils.get(ctx.guild.roles, id=661454256251076613)
#logchannel = discord.utils.get(client.get_all_channels(), id = 753619980548833401)

#SERVER INFO
ownerid = 605217750847062049
botownerid = 631441731350691850

category_list = {
    "help" : 896390484908470292,
    "mm" : 896374909897420831,
    "complete": 896375184834064404
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
        
        bait = 0

        if bait == 0 and mok == 1:
            storagelist.insert(namoji, ",") #first comma insert
        elif namoji == 0:
            jumpdistance = 3
            mok = mok - 2
            while bait <= mok:
                storagelist.insert(jumpdistance, ",")
                jumpdistance += 4
                bait += 1
        else:
            bait = 1
            newmok = 0
            while bait <= mok:
                if bait == 1:
                    storagelist.insert(namoji, ",")
                    bait += 1
                else:
                    if newmok == 0:
                        newmok = namoji + 4
                    else:
                        newmok += 4
                    storagelist.insert(newmok, ",")
                    bait += 1

        complete = joinlist(storagelist)
        return complete

def checkowner(enterownerid):
    if enterownerid == ownerid or enterownerid == botownerid:
        return True
    else:
        return False


@client.event
async def on_ready():
    game = discord.Game(name = "판매 돕는 중")
    await client.change_presence(activity = game)

    print("Ready to Run")

##########################################################################
#OWNER ONLY

@client.command(aliases=["경매생성"])
async def postauction(ctx, auctionchannel:discord.TextChannel = None, startingprice = None, *, itemtosell = None):

    jsonpath = "database/auction/ongoing/"

    if checkowner(ctx.author.id):
        if auctionchannel == None or startingprice == None or itemtosell == None:
            embed = discord.Embed(
                title = f"에러 | 양식 오류",
                description = f"`$경매생성 #채널 시작가격 판매하는물건`",
                color = discord.Color.from_rgb(255, 255, 0)
            )
            embed.set_footer(text=f"NastyCore, The Next Innovation")
            await ctx.send(embed=embed)
        else:
            convertedprice = formatmoney(int(startingprice))
            targetchannel = discord.utils.get(client.get_all_channels(), id = auctionchannel.id)

            with open(jsonpath+"newauction.json", encoding='UTF8') as f:
                jsondata = json.load(f)
                f.close()
            
            currentid = jsondata["auctionid"]
            currentid += 1
            jsondata["auctionid"] = currentid

            with open(jsonpath+"newauction.json", "w", encoding='UTF8') as f:
                json.dump(jsondata, f, indent=2)
                f.close()
            
            jsondata["itemname"] = itemtosell
            jsondata["startingprice"] = startingprice
            jsondata["best_bet"]["userid"] = ctx.author.id
            jsondata["best_bet"]["price"] = startingprice

            with open(jsonpath+f"{currentid}.json", "w", encoding='UTF8') as f:
                json.dump(jsondata, f, indent=2)
                f.close()

            await targetchannel.send("@everyone")
            embed = discord.Embed(
                title = f"새로운 경매 | {itemtosell}",
                description = f"새로운 경매가 나왔습니다\n```아이템: {itemtosell}\n시작가격: {convertedprice}\n경매아이디: {currentid}```\n경매참여: `$경매참여 경매아이디 가격`\n경매정보: `$경매확인 경매아이디`",
                color = discord.Color.from_rgb(0, 255, 0)
            )
            embed.set_footer(text=f"NastyCore, The Next Innovation")
            await targetchannel.send(embed=embed)


    else:
            embed = discord.Embed(
                title = f"에러 | 주인 전용 명령어",
                description = f"경매생성 명령어는 주인만 사용 가능한 명령어입니다.",
                color = discord.Color.from_rgb(255, 0, 0)
            )
            embed.set_footer(text=f"NastyCore, The Next Innovation")

@client.command(aliases=["경매차단"])
async def blacklistauction(ctx, target:discord.Member = None):

    if checkowner(ctx.author.id):
        path = "database/auction/blacklist.blacklist.json"

        with open(path) as f:
            r = json.load(f)
            f.close()
        
        if target.id in r:
            r.remove(target.id)

            embed = discord.Embed(
                title = f"블랙리스트 해제",
                description = f"{target.mention}님은 다시 경매 명령어를 사용할 수 있습니다.",
                color = discord.Color.from_rgb(0, 255, 0)
            )
            embed.set_footer(text=f"NastyCore, The Next Innovation")
            await ctx.send(embed=embed)
        else:
            r.append(target.id)

            embed = discord.Embed(
                title = f"블랙리스트 추가",
                description = f"{target.mention}님은 이제 경매 명령어를 사용할 수 없습니다.",
                color = discord.Color.from_rgb(0, 255, 0)
            )
            embed.set_footer(text=f"NastyCore, The Next Innovation")
            await ctx.send(embed=embed)

        with open(path, "w") as f:
            json.dump(r, f, indent=2)
            f.close()
    else:
        embed = discord.Embed(
            title = f"에러 | 주인 전용 명령어",
            description = f"경매생성 명령어는 주인만 사용 가능한 명령어입니다.",
            color = discord.Color.from_rgb(255, 0, 0)
        )
        embed.set_footer(text=f"NastyCore, The Next Innovation")

        
















client.run("ODk2MzY4NTk1ODA0NzgyNjQy.YWGGTg.7AUnthC-deNyobLAGf8FjPRwoSk")