import discord, os
from discord.ext import commands

class ready(commands.Cog):

    def __init__(self, client):
        self.client = client 

    @commands.Cog.listener()
    async def on_ready(self):

        for Cogs in os.listdir('./cogs'):
            if Cogs.endswith('.py'): 
                self.client.load_extension('cogs.{}'.format(Cogs[:-3]))

        await self.client.change_presence(activity=discord.Streaming(name="(╯°□°）╯︵ ┻━┻", url="https://www.twitch.tv/ctel21"))

def setup(client):
    client.add_cog(ready(client))