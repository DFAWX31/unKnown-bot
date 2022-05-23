from tabnanny import check
import discord
from discord.ext import commands
from config import reactions, reddit, get_reddit_server, get_reddit_user
import json
import bot_commands.reddit.redditfetcher as reddit_fetcher

class SubReddit(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(name="reddit", help="initialize subreddit to a channel")
	@commands.has_permissions(manage_messages=True)
	async def _reddit(self, ctx, channel : discord.channel = None):
		if channel == None:
			channel = ctx.channel
		
		datas = {
			"server": ctx.guild.id,
			"subreddit": "",
			"channel": channel.id,
			"category": ""
		}

		await ctx.send('Enter the name of the subreddit:')

		def check(ct):
			return ct.author == ctx.author and ct.channel == ctx.channel

		sub = None

		try:
			sub = await self.bot.wait_for('message', check=check, timeout=10.0)
		except:
			return await ctx.send('Message timed out(10s)')
		datas['subreddit'] = str(sub.content)

		msg = await ctx.send('Enter how you want to sort the content')

		reactions = ['🆕', '🔥', '🔝', '💹']

		for reaction in reactions:
			await msg.add_reaction(reaction)

		def check(react, user):
			return user == ctx.author and str(react.emoji) in reactions 

		try:
			reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout = 25.0)
		except:
			return await ctx.send('timed out(25s)')

		switcher ={
			'🆕': 'new',
			'🔥': 'hot',
			'🔝': 'top',
			'💹': 'rising'
		}

		type = switcher[str(reaction.emoji)]

		datas['category'] = type

		with open(reddit) as json_file:
			server_data = json.load(json_file)
			server_data['server-data'].append(datas)
			json_file.close()

		with open(reddit, 'w') as json_file:
			json.dump(server_data, json_file)
			json_file.close()

		await ctx.send(f'You have chosen to send r/{sub.content}\'s {type} channel\'s data to {ctx.channel.mention}')

