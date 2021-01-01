import discord, datetime, json, io, os, turtle
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from discord.ext import commands  

# open sources <start>

def mask_circle_solid(pil_img, background_color, blur_radius, offset=0):

    background = Image.new(pil_img.mode, pil_img.size, background_color)

    offset = blur_radius * 2 + offset
    mask = Image.new("L", pil_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((offset, offset, pil_img.size[0] - offset, pil_img.size[1] - offset), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

    return Image.composite(pil_img, background, mask)

# open sources <finish>

class ACCOUNT(commands.Cog):

    def __init__(self, client):
        self.client = client 

    @commands.command(aliases=["account"])
    async def 계좌(self, ctx, menu=None):

        if menu == None:  
            try: 
                uuid = json.load(open('./sql/MineCraftUUID.json', 'r', encoding="UTF-8"))[f"{ctx.author.id}"]
                ops = json.load(open('./sql/MineCraft.json', 'r', encoding="UTF-8"))

                for op in ops:
                    if str(op) == str(uuid):

                        asset = ctx.author.avatar_url 
                        authors = io.BytesIO(await asset.read())
                        authors = Image.open(authors)
                        authors = authors.resize((180, 180), Image.ANTIALIAS)
                        authors = mask_circle_solid(authors, (0, 0, 0), 4) 

                        main = Image.open('./images/main.png')
                        main.paste(authors, (60, 60))
                        main.save('./images/main(push).png')

                        main = Image.open('./images/main(push).png')
                        mainDraw = ImageDraw.Draw(main)

                        SelectFont = ImageFont.truetype('./fonts/main2.ttf', 105)
                        SelectFont2 = ImageFont.truetype('./fonts/main.ttf', 15)
                        mainDraw.text((300, 85), '{}'.format('{:,}'.format(int(ops[f"{op}"]["account"]["hwape"]))), font=SelectFont)
                        mainDraw.text((260, 70), '{}'.format(ops[f"{op}"]["account/code"]), font=SelectFont2)
                        main.save('./images/main(push).png')

                        await ctx.send(file=discord.File(fp='./images/main(push).png'))
                        return 

                await ctx.send(f"**{ctx.author.display_name}님의 명의로 된 계좌가 존재하지 않습니다.**\n도드랑거리에 있는 도스은행 본점에 직접 방문하여 계좌를 개설하실 수 있습니다.")

            except KeyError:
                await ctx.send("`-minecraft [(minecraft)name]`를 통해서 본인 인증 후에 해당 서비스를 사용하실 수 있습니다.")

        elif menu == "storage" or menu == "스토리지":
            try:
                uuid = json.load(open('./sql/MineCraftUUID.json', 'r', encoding="UTF-8"))[f"{ctx.author.id}"]
                ops = json.load(open('./sql/MineCraft.json', 'r', encoding="UTF-8"))

                for op in ops:
                    if str(op) == str(uuid):

                        items = ""
                        for item in ops[f"{op}"]["account"]["storage"]:
                            if items == "":
                                items = "💫  {} **({})** - 해당 물품은 {}에 새로 추가되었습니다.".format(item, ops[f"{op}"]["account"]["storage"][f"{item}"]["quantity"], ops[f"{op}"]["account"]["storage"][f"{item}"]["space"])
                            else:
                                items += "\n💫  {} **({})** - 해당 물품은 {}에 새로 추가되었습니다.".format(item, ops[f"{op}"]["account"]["storage"][f"{item}"]["quantity"], ops[f"{op}"]["account"]["storage"][f"{item}"]["space"])

                        if items == "":
                            await ctx.send("{}님의 스토리지에서 보관된 물품을 찾을 수 없습니다.\n은행에 맡긴 물품이 있음에도 불구하고 없다고 나온다면 은행원을 반드시 호출해주세요".format(ctx.author.display_name))
                        else:
                            await ctx.send(items)
                        return 

                await ctx.send(f"**{ctx.author.display_name}님의 명의로 된 계좌가 존재하지 않습니다.**\n도드랑거리에 있는 도스은행 본점에 직접 방문하여 계좌를 개설하실 수 있습니다.")

            except KeyError:
                await ctx.send("`-minecraft [(minecraft)name]`를 통해서 본인 인증 후에 해당 서비스를 사용하실 수 있습니다.")

def setup(client):
    client.add_cog(ACCOUNT(client))