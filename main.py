from dis import dis, disco
from unicodedata import name
import discord
import config
from bot_commands.test import TestCog
from bot_commands.moderation import AdminCog
from bot_commands.currency import CurrencyCog
from bot_commands.reddit.subreddit import SubReddit

from discord.ext import commands
intents = discord.Intents.all()
activity = discord.Activity(name='to commands', type=discord.ActivityType.listening)

BOT = config.BOT_TOKEN
class MyClient(commands.Bot):
	def __init__(self, command_prefix,  intents, activity):
		self.bot = commands.Bot.__init__(self, command_prefix=command_prefix, intents=intents, activity=activity)

	
	async def on_ready(self):
		print('logged in as {0}!'.format(self.user))
		
		
class PingCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def ping(self, ctx):
		await ctx.send(f'Pong {round(self.bot.latency, 1)}')


client = MyClient(command_prefix=config.PREFIX, intents=intents, activity=activity)
client.add_cog(PingCog(client))
client.add_cog(TestCog(client))
client.add_cog(AdminCog(client))
client.add_cog(CurrencyCog(client))
client.add_cog(SubReddit(client))
client.run(BOT)