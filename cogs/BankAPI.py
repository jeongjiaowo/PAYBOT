import discord, requests, json 
from discord.ext import commands 
from discord.utils import get 

class API(commands.Cog):

    def __init__(self, client):
        self.client = client 

    @commands.command(aliases=["api"])
    async def 확인(self, ctx, menu, owner):

        role = get(ctx.author.roles, id=768843101656580128)
        if role in ctx.author.roles: 

            if menu == "money": 
                try:
                    ops = json.load(open('./sql/MineCraft.json', 'r', encoding="UTF-8"))
                    uuid = requests.get('https://api.mojang.com/users/profiles/minecraft/' + str(owner)).json()["id"] 

                    for op in ops:
                        if str(op) == str(uuid):

                            await ctx.send("```POST: {}```".format('{:,}'.format(ops[f"{op}"]["account"]["hwape"])))
                            return 

                    await ctx.send('{ "errorcode": "101" }')

                except:
                    await ctx.send('{ "errorcode": "404" }')

            elif menu == "code":
                try:
                    ops = json.load(open('./sql/MineCraft.json', 'r', encoding="UTF-8"))
                    uuid = requests.get('https://api.mojang.com/users/profiles/minecraft/' + str(owner)).json()["id"] 

                    for op in ops:
                        if str(op) == str(uuid):

                            await ctx.send("```POST: {}```".format(ops[f"{op}"]["account/code"]))
                            return 

                    await ctx.send('{ "errorcode": "101" }')

                except:
                    await ctx.send('{ "errorcode": "404" }')

            elif menu == "storage":
                try:
                    ops = json.load(open('./sql/MineCraft.json', 'r', encoding="UTF-8"))
                    uuid = requests.get('https://api.mojang.com/users/profiles/minecraft/' + str(owner)).json()["id"] 
                    title = ""
                    titles = 0

                    for op in ops:
                        if str(op) == str(uuid):
                            for item in ops[f"{op}"]["account"]["storage"]:
                                titles += 1
                                if title == "":
                                    title = "[{}] {} ({}) - {}에 새로 추가되었습니다.".format(titles, item, ops[f"{op}"]["account"]["storage"][f"{item}"]["quantity"], ops[f"{op}"]["account"]["storage"][f"{item}"]["space"])
                                else:
                                    title += "\n[{}] {} ({}) - {}에 새로 추가되었습니다.".format(titles, item, ops[f"{op}"]["account"]["storage"][f"{item}"]["quantity"], ops[f"{op}"]["account"]["storage"][f"{item}"]["space"])

                            if title == "":
                                await ctx.send("```POST: Not Found```")
                            else:
                                await ctx.send("```POST:\n{}```".format(title))
                            return 

                    await ctx.send('{ "errorcode": "101" }')

                except:
                    await ctx.send('{ "errorcode": "404" }') 

def setup(client):
    client.add_cog(API(client))