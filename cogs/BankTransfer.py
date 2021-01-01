import discord, asyncio, datetime, json 
from discord.ext import commands

CodeDependency = []

def CodeDependencyTest(Code):

    ops = json.load(open('./sql/MineCraft.json', 'r', encoding="UTF-8"))
    for op in ops:
        if str(ops[f"{op}"]["account/code"]) == str(Code):
            return "true"

    return "false"

def CodeOps(Code):

    ops = json.load(open('./sql/MineCraft.json', 'r', encoding="UTF-8"))
    for op in ops:
        if str(ops[f"{op}"]["account/code"]) == str(Code):
            return op

def CodeName(Code):

    ops = json.load(open('./sql/MineCraft.json', 'r', encoding="UTF-8"))
    for op in ops:
        if str(ops[f"{op}"]["account/code"]) == str(Code):
            return ops[f"{op}"]["account/owner"] 

class TRANSFER(commands.Cog):

    def __init__(self, client):
        self.client = client 

    @commands.command(aliases=["이체", "계좌이체"])
    async def transfer(self, ctx, code, money): 
 
        try:
            uuid = json.load(open('./sql/MineCraftUUID.json', 'r', encoding="UTF-8"))[f"{ctx.author.id}"]
            ops = json.load(open('./sql/MineCraft.json', 'r', encoding="UTF-8"))

            if not ctx.author.dm_channel: 
                await ctx.send("이 명령어는 공공 채널에서 사용하실 수 없습니다.")
            else:
                for op in ops:
                    if str(op) == str(uuid):
                        if int(ops[f"{op}"]["account"]["hwape"]) >= int(money):

                            for Developer in CodeDependency:
                                if str(Developer) == str(ctx.author.id):
                                    await ctx.send("현재 계좌이체를 진행하는 중입니다. 해당 과정을 먼저 종료해주세요")
                                    return

                            if str(ops[f"{op}"]["account/code"]) == str(code):
                                await ctx.send("자기 자신(본인)의 명의로 되어있는 계좌에 이체할 수 없습니다.")
                            elif int(money) < 1000:
                                await ctx.send("최소 **1,000**원부터 해당 계좌번호로 이체할 수 있습니다.")
                            else:  
                                CodeDependency.append(ctx.author.id)
                                test = CodeDependencyTest(code)
                                if test == "false":
                                    await ctx.send("해당 계좌번호와 일치하는 계좌를 찾을 수 없습니다.\n없는 계좌거나 또는 계좌번호를 잘못 입력하였는지 다시 확인해주세요.")
                                    CodeDependency.remove(ctx.author.id)
                                else:
                                    ms = await ctx.send("정말로 해당 계좌번호로 계좌이체를 진행하시겠습니까?\n이 과정을 진행할 경우 해당 돈은 계좌번호로 전송되며 다시 돌려받을 수 없습니다.")
                                    await ms.add_reaction('📪')

                                    def check(reaction, user):
                                        return reaction.emoji == '📪' and reaction.message.id == ms.id and user.id == ctx.author.id
                                    
                                    def check1(m):
                                        return m.channel.id == ctx.channel.id and m.author.id == ctx.author.id 

                                    try:
                                        reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=10)
                                        if user.id == ctx.author.id and reaction.emoji == '📪': 

                                            await ctx.send("계좌이체를 최종적으로 진행하기 전 보안 비밀번호를 입력해주세요!")
                                            
                                            try:
                                                user = await self.client.wait_for('message', check=check1, timeout=20)
                                                if str(user.content) == str(ops[f"{op}"]["account/password"]): 
                                                    
                                                    test1 = CodeOps(code)
                                                    plugin = json.load(open('./sql/MineCraft.json', 'r', encoding="UTF-8"))
                                                    plugin[f"{uuid}"]["account"]["hwape"] = int(plugin[f"{uuid}"]["account"]["hwape"]) - int(money)
                                                    plugin[f"{test1}"]["account"]["hwape"] = int(plugin[f"{test1}"]["account"]["hwape"]) + int(money)
                                                    json.dump(plugin, open('./sql/MineCraft.json', 'w', encoding="UTF-8"), ensure_ascii=False, indent="\t")
                                                    await ctx.send("성공적으로 해당 계좌번호로 **{}**원을 이체하였습니다.\n해당 이체내역은 개인 거래내역(-details)에서 확인하실 수 있습니다.".format('{:,}'.format(int(money))))
                                                    CodeDependency.remove(ctx.author.id)

                                                    rounds = json.load(open('./sql/MineCraftRound.json', 'r', encoding="UTF-8"))
                                                    rounds[f"{int(len(rounds)) + 1}"] = { "namespace": f"{uuid}", "namedoin": "해당 계좌번호({})로 {}원을 이체하였습니다".format(code, '{:,}'.format(int(money))), "datetime": f"{datetime.datetime.now()}" }
                                                    json.dump(rounds, open('./sql/MineCraftRound.json', 'w', encoding="UTF-8"), ensure_ascii=False, indent="\t")

                                                    await self.client.get_channel(769451041162657792).send("{}님이 {}님의 계좌로 {}원을 이체하였습니다".format(ctx.author.name, CodeName(code), '{:,}'.format(int(money))))

                                                else:
                                                    await ctx.send("올바르지 않은 보안 비밀번호를 입력하셨습니다.\n이전 명령어를 통해 해당 과정을 다시 재시도하실 수 있습니다.")
                                                    CodeDependency.remove(ctx.author.id)

                                            except asyncio.TimeoutError:
                                                await ctx.send("보안 비밀번호를 입력하지 않아 해당 단계(과정)가 취소되었습니다.")
                                                CodeDependency.remove(ctx.author.id)

                                    except asyncio.TimeoutError:
                                        await ctx.send("이모지를 누르지 않아 해당 단계(과정)가 취소되었습니다.")
                                        CodeDependency.remove(ctx.author.id)
                        
                        else:
                            await ctx.send("이체할 금액이 부족하여 해당 과정을 진행할 수 없습니다.")

                        return 

                await ctx.send(f"**{ctx.author.display_name}님의 명의로 된 계좌가 존재하지 않습니다.**\n도드랑거리에 있는 도스은행 본점에 직접 방문하여 계좌를 개설하실 수 있습니다.")

        except KeyError:
            await ctx.send("`-minecraft [(minecraft)name]`를 통해서 본인 인증 후에 해당 서비스를 사용하실 수 있습니다.")

def setup(client):
    client.add_cog(TRANSFER(client))