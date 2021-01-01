import discord
from discord.ext import commands

class Client(commands.Bot):

    def __init__(self):
        super().__init__ (
            command_prefix = "-" 
        )
        self.load_extension('events.ready')

Client().run('token')