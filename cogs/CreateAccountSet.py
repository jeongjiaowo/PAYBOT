import discord, json, requests, datetime 
from discord.ext import commands  
from discord.utils import get 

class CREATE_ACCOUNT_SET(commands.Cog):

    def __init__(self, client):
        self.client = client 

    @commands.command(aliases=["셋트"])
    async def set(self, ctx, commands, name, money, sour=None):

        role = get(ctx.author.roles, id=768843101656580128)
        if role in ctx.author.roles: 

            if commands == "money" or commands == "잔액": 

                try: 
                    uuid = requests.get('https://api.mojang.com/users/profiles/minecraft/' + str(name)).json()["id"]
                    ops = json.load(open('./sql/MineCraft.json', 'r', encoding="UTF-8"))
                    for op in ops:
                        if str(op) == str(uuid):
                            ops[f"{uuid}"]["account"]["hwape"] = int(ops[f"{uuid}"]["account"]["hwape"]) + int(money)
                            json.dump(ops, open('./sql/MineCraft.json', 'w', encoding="UTF-8"), ensure_ascii=False, indent="\t")
                            await ctx.send("계좌번호(`{}`)에 {}원을 추가하였습니다.".format(ops[f"{op}"]["account/code"], '{:,}'.format(int(money))))
                            await self.client.get_channel(769446046270357506).send("{}님의 계좌 잔액에 {}원이 추가되었습니다".format(name, '{:,}'.format(int(money))))
                            return 

                    await ctx.send('{ "errorcode": "101" }')

                except:
                    await ctx.send('{ "errorcode": "404" }')

            elif commands == "storage" or commands == "스토리지":
                
                try: 
                    uuid = requests.get('https://api.mojang.com/users/profiles/minecraft/' + str(name)).json()["id"]
                    ops = json.load(open('./sql/MineCraft.json', 'r', encoding="UTF-8"))
                    for op in ops:
                        if str(op) == str(uuid):
                            for storages in ops[f"{uuid}"]["account"]["storage"]:
                                if str(storages) == str(money): 
                                    b = int(ops[f"{uuid}"]["account"]["storage"][f"{money}"]["quantity"]) + int(sour)
                                    if int(b) <= 0:
                                        del ops[f"{uuid}"]["account"]["storage"][f"{money}"]
                                    else:
                                        ops[f"{uuid}"]["account"]["storage"][f"{money}"]["quantity"] = int(b)
                                    json.dump(ops, open('./sql/MineCraft.json', 'w', encoding="UTF-8"), ensure_ascii=False, indent="\t")
                                    await ctx.send("계좌번호(`{}`)의 스토리지에 {}을(를) {}개만큼 추가하였습니다.".format(ops[f"{op}"]["account/code"], money, sour))
                                    await self.client.get_channel(769446046270357506).send("{}님의 계좌 물품목록에 {}이(가) {}개만큼 추가되었습니다".format(name, money, sour))
                                    return 

                            ops[f"{uuid}"]["account"]["storage"][f"{money}"] = { "quantity": int(sour), "space": f"{datetime.datetime.now()}" }
                            json.dump(ops, open('./sql/MineCraft.json', 'w', encoding="UTF-8"), ensure_ascii=False, indent="\t")
                            await ctx.send("계좌번호(`{}`)의 스토리지에 {}을(를) {}개만큼 추가하였습니다.".format(ops[f"{op}"]["account/code"], money, sour))
                            await self.client.get_channel(769446046270357506).send("{}님의 계좌 물품목록에 {}이(가) {}개만큼 추가되었습니다".format(name, money, sour))
                            return 

                    await ctx.send('{ "errorcode": "101" }')

                except: 
                    await ctx.send('{ "errorcode": "404" }')

def setup(client):
    client.add_cog(CREATE_ACCOUNT_SET(client))