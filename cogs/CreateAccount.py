import discord, datetime, requests, random, json 
from discord.ext import commands 
from discord.utils import get  

def AccountCodeRandom():

    while True:
        code1 = random.randrange(100, 9999)
        code2 = random.randrange(100, 777)
        code3 = random.randrange(100, 999)
        code4 = random.randrange(100, 1555)
        code = f"{code1}-{code2}-{code3}-{code4}"

        ops = json.load(open('./sql/MineCraft.json', 'r', encoding="UTF-8"))
        for op in ops:
            if str(ops[f"{op}"]["account/code"]) == str(code):
                pass 

        return code 

class CREATE_ACCOUNT(commands.Cog):

    def __init__(self, client):
        self.client = client 

    @commands.command(aliases=["create"])
    async def 생성(self, ctx, owner, password): 

        role = get(ctx.author.roles, id=768843101656580128)
        if role in ctx.author.roles: 

            ops = json.load(open('./sql/MineCraft.json', 'r', encoding="UTF-8"))
            for op in ops:
                if str(ops[f"{op}"]["account/owner"]) == str(owner):
                    await ctx.send('{ "errorcode": "302" }')
                    return 

            try:
                uuid = requests.get('https://api.mojang.com/users/profiles/minecraft/' + str(owner)).json()["id"] 
            except:
                await ctx.send('{ "errorcode": "404" }')
                return 

            code = AccountCodeRandom()
            ops[f"{uuid}"] = { "account/code": f"{code}", "account/password": f"{password}", "account/owner": f"{owner}", "account": { "hwape": 0, "storage": { } } }
            json.dump(ops, open('./sql/MineCraft.json', 'w', encoding="UTF-8"), ensure_ascii=False, indent="\t")
            await ctx.send("성공적으로 해당 마인크래프트 이름 명의로 계좌가 개설되었습니다.\n부여된 계좌번호는 **{}**로 설정되었습니다.".format(code))

def setup(client):
    client.add_cog(CREATE_ACCOUNT(client))