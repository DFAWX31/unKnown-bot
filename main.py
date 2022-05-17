from unicodedata import name
import discord
import config

from discord.ext import commands

bot = commands.Bot(command_prefix=config.PREFIX)

BOT = config.BOT_TOKEN

class MyClient(discord.Client):
	async def on_ready(self):
		print('logged in as {0}!'.format(self.user))
		await self.change_presence(activity=discord.Activity(name=f"commands {config.PREFIX}", type=2))

	async def on_message(self, message):
		if message.author.bot:
			return

		print('Message from {0.author}: {0.content}'.format(message))
		channel = message.channel
		await channel.send('{0.author.mention}: `{0.content}` in {0.channel.mention}'.format(message))


client = MyClient()

client.run(BOT)