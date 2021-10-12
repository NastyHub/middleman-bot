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
##########################################################################
#Auction-Related
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

def checkifauctionexists(auctionid):
    supportbridge = "database/auction/ongoing/"
    bidid = str(auctionid)

    if os.path.isfile(supportbridge+f"{bidid}.json"):
        return True
    else:
        return False

##########################################################################
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
            jsondata["auctionchannel"] = auctionchannel.id

            with open(jsonpath+f"{currentid}.json", "w", encoding='UTF8') as f:
                json.dump(jsondata, f, indent=2)
                f.close()

            await targetchannel.send("@everyone")
            embed = discord.Embed(
                title = f"새로운 경매 | **{itemtosell}**",
                description = f"새로운 경매가 나왔습니다\n```아이템: {itemtosell}\n시작가격: {convertedprice}\n경매아이디: {currentid}```\n경매참여: `$경매참여 경매아이디 가격`\n경매정보: `$경매정보 경매아이디`",
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
            await ctx.send(embed=embed)

#경매차단 명령어 테스트 바람
@client.command(aliases=["경매차단"])
async def blacklistauction(ctx, target:discord.Member = None):
    if target != None:
        if checkowner(ctx.author.id):
            path = "database/auction/blacklist/blacklist.json"

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
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title = f"에러 | 양식오류",
            description = f"`$경매차단 @유저멘션`",
            color = discord.Color.from_rgb(255, 255, 0)
        )
        embed.set_footer(text=f"NastyCore, The Next Innovation")
        await ctx.send(embed=embed)      


#입찰삭제 명령어 테스트 바람
@client.command(aliases=["최고가설정"])
async def sethighest(ctx, auctionid=None, target:discord.Member=None, price=None):
    if checkowner(ctx.author.id):
        if auctionid != None and target != None and price != None:
            decidedpath = f"database/auction/ongoing/{auctionid}.json"

            with open(decidedpath, encoding='UTF8') as f:
                r = json.load(f)
                f.close()
            
            historylist = r["history"]
            highestbid = r["best_bet"]

            if checkifauctionexists(int(auctionid)):
                highestbid["userid"] = target.id
                highestbid["price"] = int(price)

                await ctx.send("ok")

                with open(decidedpath, "w") as f:
                    json.dump(r, f, indent=2)
                    f.close()

            else:
                embed = discord.Embed(
                    title = f"에러 | 찾지못함",
                    description = f"해당 입찰아이디를 찾지 못했습니다",
                    color = discord.Color.from_rgb(255, 255, 0)
                )
                embed.set_footer(text=f"NastyCore, The Next Innovation")
                await ctx.send(embed=embed)     


        else:
            embed = discord.Embed(
                title = f"에러 | 양식오류",
                description = f"`$최고가설정 경매아이디 @유저 가격`",
                color = discord.Color.from_rgb(255, 255, 0)
            )
            embed.set_footer(text=f"NastyCore, The Next Innovation")
            await ctx.send(embed=embed)

    else:
        embed = discord.Embed(
            title = f"에러 | 주인 전용 명령어",
            description = f"경매생성 명령어는 주인만 사용 가능한 명령어입니다.",
            color = discord.Color.from_rgb(255, 0, 0)
        )
        embed.set_footer(text=f"NastyCore, The Next Innovation")
        await ctx.send(embed=embed)

#경매종료 명령어 테스트 바람
@client.command(aliases=["경매종료"])
async def endauction(ctx, auctionid=None):
    if checkowner(ctx.author.id):
        if auctionid != None:
            if checkifauctionexists(auctionid):
                path = f"database/auction/ongoing/{auctionid}.json"

                with open(path) as f:
                    r = json.load(f)
                    f.close()
                
                itemname = r["itemname"]
                startingprice = r["startingprice"]
                auctionid = auctionid
                auctionchannel = r["auctionchannel"]

                best_bet_dict = r["best_bet"]
                history_list = r["history"]
                winner_dict = r["winner"]

                #winner info
                winner_id = best_bet_dict["userid"]
                winner_price = best_bet_dict["price"]
                winner_id = best_bet_dict["bidid"]


                targetchannel = discord.utils.get(client.get_all_channels(), id = auctionchannel)

                altuserid = r["best_bet"]["userid"]
                targetuser = await client.fetch_user(int(altuserid))

                targetuserdisplayname = targetuser.display_name

                startingprice = formatmoney(startingprice)
                finalprice = formatmoney(winner_price)

                #transfer to winner_dict
                winner_dict["userid"] = winner_id
                winner_dict["price"] = winner_price
                winner_dict["bidid"] = winner_id

                await targetchannel.send("@everyone")
                embed = discord.Embed(
                    title = f"경매 종료 | **{targetuserdisplayname}**🎉",
                    description = f"경매 정보:\n```판매 제품: {itemname}\n시작가격: {startingprice}\n낙찰가: {finalprice}\n입찰참여총횟수: {len(history_list)-1}```\n우승을 축하드립니다:\n```유저: {targetuser}\n유저아이디: {altuserid}```",
                    color = discord.Color.from_rgb(0, 255, 0)
                )
                embed.set_footer(text=f"NastyCore, The Next Innovation")
                await targetchannel.send(embed=embed)

                os.remove(path)


            else:
                embed = discord.Embed(
                    title = f"에러 | 존재하지 않는 경매 아이디",
                    description = f"해당 경매 아이디는 존재하지 않습니다",
                    color = discord.Color.from_rgb(255, 255, 0)
                )
                embed.set_footer(text=f"NastyCore, The Next Innovation")
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title = f"에러 | 양식오류",
                description = f"$경매종료 경매아이디",
                color = discord.Color.from_rgb(255, 255, 0)
            )
            embed.set_footer(text=f"NastyCore, The Next Innovation")
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title = f"에러 | 주인 전용 명령어",
            description = f"경매생성 명령어는 주인만 사용 가능한 명령어입니다.",
            color = discord.Color.from_rgb(255, 0, 0)
        )
        embed.set_footer(text=f"NastyCore, The Next Innovation")
        await ctx.send(embed=embed)
##########################################################################
#FOR EVERYONE

@client.command(aliases=["경매정보"])
async def auctioninfo(ctx, auctionid=None):
    if auctionid != None:
        if checkifauctionexists(auctionid):
            path = f"database/auction/ongoing/{auctionid}.json"

            with open(path) as f:
                r = json.load(f)
                f.close()
            
            itemname = r["itemname"]
            startingprice = r["startingprice"]
            bestpriceid = r["best_bet"]["userid"]
            bestpriceprice = r["best_bet"]["price"]

            startingprice = formatmoney(startingprice)
            bestpriceprice = formatmoney(bestpriceprice)

            targetuser = await client.fetch_user(int(bestpriceid))

            embed = discord.Embed(
                title = f"경매 정보",
                description = f"판매 제품: {itemname}\n시작가: {startingprice}\n\n현재최고가: {targetuser}, {bestpriceprice}",
                color = discord.Color.from_rgb(0, 255, 0)
            )
            embed.set_footer(text=f"NastyCore, The Next Innovation")
            await ctx.send(embed=embed)


        else:
            embed = discord.Embed(
                title = f"에러 | 존재하지 않는 경매 아이디",
                description = f"해당 경매 아이디는 존재하지 않습니다",
                color = discord.Color.from_rgb(255, 255, 0)
            )
            embed.set_footer(text=f"NastyCore, The Next Innovation")
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title = f"에러 | 양식오류",
            description = f"`$경매정보 경매아이디`",
            color = discord.Color.from_rgb(255, 255, 0)
        )
        embed.set_footer(text=f"NastyCore, The Next Innovation")
        await ctx.send(embed=embed)

@client.command(aliases=["경매참여"])
async def enterauction(ctx, auctionid=None, price=None):
    if auctionid != None and price != None:

        with open("database/auction/blacklist/blacklist.json") as f:
            jsondata = json.load(f)
            f.close()
        
        if ctx.author.id not in jsondata:
            if checkifauctionexists(auctionid):
                price = int(price)
                formatprice = formatmoney(price)
                path = f"database/auction/ongoing/{auctionid}.json"

                with open(path) as f:
                    r = json.load(f)
                    f.close()

                bestpriceprice = r["best_bet"]["price"]

                history_list = r["history"]
                currentbidid = r["bidid"]
                targetchannel = r["auctionchannel"]
                targetchannel = discord.utils.get(client.get_all_channels(), id = int(targetchannel))

                newbidid = currentbidid + 1

                r["bidid"] = newbidid

                bestformatprice = formatmoney(bestpriceprice)
                
                if int(bestpriceprice) >= int(price):
                    embed = discord.Embed(
                        title = f"에러 | 최고가보다 낮음",
                        description = f"현재 최고가({bestformatprice})보다 높게 설정해 주세요.",
                        color = discord.Color.from_rgb(255, 255, 0)
                    )
                    embed.set_footer(text=f"NastyCore, The Next Innovation")
                    await ctx.send(embed=embed)
                else:
                    format_dict = {
                        "userid": ctx.author.id,
                        "price": int(price),
                        "bidid": newbidid
                    }

                    history_list.append(format_dict)

                    r["best_bet"]["price"] = int(price)
                    r["best_bet"]["userid"] = ctx.author.id
                    r["best_bet"]["bidid"] = currentbidid

                    with open(path, "w") as f:
                        json.dump(r, f, indent=2)
                        f.close()

                    embed = discord.Embed(
                        title = f"새로운 경매 최고가",
                        description = f"{ctx.author.mention}님: {formatprice}\n입찰아이디: {newbidid}",
                        color = discord.Color.from_rgb(0, 255, 0)
                    )
                    embed.set_footer(text=f"NastyCore, The Next Innovation")
                    await targetchannel.send(embed=embed)

                    await ctx.send("ㅇㅋ")


            else:
                embed = discord.Embed(
                    title = f"에러 | 존재하지 않는 경매 아이디",
                    description = f"해당 경매 아이디는 존재하지 않습니다",
                    color = discord.Color.from_rgb(255, 255, 0)
                )
                embed.set_footer(text=f"NastyCore, The Next Innovation")
                await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title = f"에러 | 양식오류",
            description = f"`$경매참여 경매아이디 가격`",
            color = discord.Color.from_rgb(255, 255, 0)
        )
        embed.set_footer(text=f"NastyCore, The Next Innovation")
        await ctx.send(embed=embed)















client.run("ODk2MzY4NTk1ODA0NzgyNjQy.YWGGTg.7AUnthC-deNyobLAGf8FjPRwoSk")