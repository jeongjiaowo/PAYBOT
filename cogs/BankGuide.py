import discord
from discord.ext import commands  

class GUIDE(commands.Cog):

    def __init__(self, client):
        self.client = client 

    @commands.command(aliases=["how", "tag"])
    async def 태그(self, ctx, menu=None):

        if menu == None:
            await ctx.send("**-tag [태그]**를 통해 아래에 있는 태그 중 하나를 선택하여 궁금증을 해결하세요.\n이곳에 없거나 또는 궁금증이 그래도 풀리지 않은 경우 문의센터 채널에 따로 문의바랍니다.\n```계좌이체, 계좌, 계좌물품목록, 마인크래프트, 계좌개설, 거래내역, 계좌오류```")
        elif menu == "계좌이체":
            await ctx.send("계좌이체는 **-transfer [계좌 번호] [이체 금액]**을 통해서 계좌이체를 진행할 수 있습니다.\n공공 채널에선 사용하실 수 없으며 봇과의 개인 채널에서만 사용할 수 있습니다\n\n<@756795149794672650>를 클릭하여 계좌이체를 진행하세요. (개인 메세지를 켜놓는걸 추천드립니다)")
        elif menu == "계좌":
            await ctx.send("계좌 잔액을 확인하실려면 **-account**를 통해서 확인하실 수 있습니다.\n단 마인크래프트 인증 및 도스은행 본점에서 계좌를 개설해야 해당 명령어를 사용할 수 있습니다.")
        elif menu == "계좌물품목록":
            await ctx.send("**-account storage**를 통해 account에 storage 옵션을 부여해 물품목록을 확인할 수 있습니다.\n단 마인크래프트 인증 및 도스은행 본점에서 계좌를 개설해야 해당 명령어를 사용할 수 있습니다.")
        elif menu == "마인크래프트":
            await ctx.send("**-minecraft [마인크래프트 닉네임]**을 통해서 마인크래프트 본인 인증할 수 있습니다.")
        elif menu == "계좌개설":
            await ctx.send("도드랑거리에 있는 도스은행 본점을 방문하여 계좌를 개설할 수 있습니다.\n**방문하기 전 설정할 보안 비밀번호를 미리 생각하고 방문해주세요.**")
        elif menu == "거래내역":
            await ctx.send("**-details**를 통해 내 거래내역을 확인할 수 있습니다.")
        elif menu == "계좌오류":
            await ctx.send("-account를 입력해도 나오지 않는다면 프사를 변경하여 해결하세요")
        else:
            await ctx.send("올바르지 않은 태그를 입력하셨습니다. **-tag**를 통해 태그 옵션을 확인해주세요.")

def setup(client):
    client.add_cog(GUIDE(client))