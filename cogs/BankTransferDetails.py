import discord, json
from discord.ext import commands

def Details(uuid): 

    detailsl = ""
    ops = json.load(open('./sql/MineCraftRound.json', 'r', encoding="UTF-8"))
    for op in ops:
        if str(ops[f"{op}"]["namespace"]) == str(uuid):
            if detailsl == "":
                detailsl = "[{}] {}".format(ops[f"{op}"]["datetime"], ops[f"{op}"]["namedoin"])
            else:
                detailsl += "\n[{}] {}".format(ops[f"{op}"]["datetime"], ops[f"{op}"]["namedoin"])
    return detailsl

class DETAILS(commands.Cog):

    def __init__(self, client):
        self.client = client 

    @commands.command(aliases=["거래내역", "내역"])
    async def details(self, ctx): 

        try:
            uuid = json.load(open('./sql/MineCraftUUID.json', 'r', encoding="UTF-8"))[f"{ctx.author.id}"]
            ops = json.load(open('./sql/MineCraft.json', 'r', encoding="UTF-8"))

            for op in ops:
                if str(op) == str(uuid):
                    details = Details(uuid)
                    if str(details) == "":
                        await ctx.send("최근에 {}님이 진행한 거래내역이 존재하지 않습니다.".format(ctx.author.display_name))
                    else:
                        await ctx.send("```ini\n{}```".format(details))
                    return 

            await ctx.send(f"**{ctx.author.display_name}님의 명의로 된 계좌가 존재하지 않습니다.**\n도드랑거리에 있는 도스은행 본점에 직접 방문하여 계좌를 개설하실 수 있습니다.")

        except KeyError:
            await ctx.send("`-minecraft [(minecraft)name]`를 통해서 본인 인증 후에 해당 서비스를 사용하실 수 있습니다.")

def setup(client):
    client.add_cog(DETAILS(client))