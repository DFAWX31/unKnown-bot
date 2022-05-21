from dis import dis
from unicodedata import name
import discord
import config
from bot_commands.test import TestCog
from bot_commands.moderation import AdminCog
from bot_commands.currency import CurrencyCog
from bot_commands.anime import AnimeCommands

from discord.ext import commands
intents = discord.Intents.all()

BOT = config.BOT_TOKEN
class MyClient(commands.Bot):
	def __init__(self, command_prefix,  intents):
		self.bot = commands.Bot.__init__(self, command_prefix=command_prefix, intents=intents)

	
	async def on_ready(self):
		print('logged in as {0}!'.format(self.user))
		
	

		
class PingCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def ping(self, ctx):
		await ctx.send(f'Pong {round(self.bot.latency, 1)}')


client = MyClient(command_prefix=config.PREFIX, intents=intents)
client.add_cog(PingCog(client))
client.add_cog(TestCog(client))
client.add_cog(AdminCog(client))
client.add_cog(CurrencyCog(client))
client.add_cog(AnimeCommands(client))
client.run(BOT)