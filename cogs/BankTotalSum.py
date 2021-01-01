import discord, asyncio, datetime, json 
from discord.ext import commands

class TOTALSUM(commands.Cog):

    def __init__(self, client):
        self.client = client 

    @commands.command(aliases=["총액"])
    async def totalsum(self, ctx): 
        
        totalsum = 0
        ops = json.load(open('./sql/MineCraft.json', 'r', encoding="UTF-8"))       
        for op in ops:
            totalsum += int(ops[f"{op}"]["account"]["hwape"])

        await ctx.send("도스은행에 누적된 총액은 총 **{}**원입니다.".format('{:,}'.format(int(totalsum))))

def setup(client):
    client.add_cog(TOTALSUM(client))