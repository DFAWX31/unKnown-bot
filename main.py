from dis import dis
from unicodedata import name
import discord
import config
from bot_commands.test import TestCog
from bot_commands.moderation import *

from discord.ext import commands

BOT = config.BOT_TOKEN
class MyClient(commands.Bot):
	def __init__(self, command_prefix, help_command):
		self.bot = commands.Bot.__init__(self, command_prefix=command_prefix, help_command=help_command)

	def role_embed(self):
		embed = discord.Embed(title="Role Assign", desription="Get yourself a role", color= 0xFCBA03)
		
		roles = ["🐴","🐒","🦍","🤺"]
		descs = ["Denchu", "Monke", "Benene", "Muh Rica"]

		for i in range(len(roles)):
			embed.add_field(name=roles[i],value=descs[i], inline=False)

		return embed

	async def reaction_menu(self, msg):
		roles = ["🐴","🐒","🦍","🤺"]
		for i in range(len(roles)):
			await msg.add_reaction(roles[i])

	async def on_ready(self):
		channel = self.get_channel(976118948292620308)
		print('logged in as {0}!'.format(self.user))
		await self.change_presence(activity=discord.Activity(name=f"commands {config.PREFIX}", type=2))
		msg = await channel.send(embed = self.role_embed())
		await self.reaction_menu(msg)

	async def on_reaction_add(self, reaction, user):
		channel = self.get_channel(976118948292620308)
		if reaction.message.channel.id != channel.id:
			return
		
		switcher = {
			"🐴": "Donkey",
			"🐒": "Monkey",
			"🦍": "Gorilla",
			"🤺": "Human"
		}
		role = discord.utils.get(user.guild.roles , name=switcher.get(str(reaction.emoji)))

		if role in user.roles:
			await user.remove_roles(role)
		else:
			await user.add_roles(role)

		
class PingCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def ping(self, ctx):
		await ctx.send(f'Pong {round(self.bot.latency, 1)}')


client = MyClient(command_prefix=config.PREFIX, help_command=None)
client.add_cog(PingCog(client))
client.add_cog(TestCog(client))
client.add_cog(AdminCog(client))
client.run(BOT)