import discord, json, requests, datetime 
from discord.ext import commands  

class MINECRAFT(commands.Cog):

    def __init__(self, client):
        self.client = client 

    @commands.command(aliases=["certified", "minecraft"])
    async def 인증(self, ctx, name=None):

        if name == None:
            await ctx.send("본인 인증할 마인크래프트 닉네임을 입력해주세요")
        else: 
            try:
                uuid = json.load(open('./sql/MineCraftUUID.json', 'r', encoding="UTF-8"))[f"{ctx.author.id}"]
                await ctx.send("**이미 {}님의 마인크래프트 본인 인증은 완료된 상태입니다.**\n재인증을 원하실 경우에는 은행원에게 요청하여 변경하세요".format(ctx.author.display_name))
            except: 
                try: 
                    uuid = requests.get('https://api.mojang.com/users/profiles/minecraft/' + str(name)).json()["id"]
                    uuiddata = json.load(open('./sql/MineCraftUUID.json', 'r', encoding="UTF-8"))
                    uuiddata[f"{ctx.author.id}"] = "{}".format(uuid)
                    json.dump(uuiddata, open('./sql/MineCraftUUID.json', 'w', encoding="UTF-8"), ensure_ascii=False, indent="\t")
                    await ctx.message.add_reaction('🚀')
                except:
                    await ctx.send("플레이어 이름을 올바르게 입력하셨는지 다시 한번 더 확인해주세요")

def setup(client):
    client.add_cog(MINECRAFT(client))