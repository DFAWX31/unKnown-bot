from socket import timeout
import discord
from discord.ext import commands, tasks
from config import reactions, reddit, get_reddit_server, get_reddit_user, get_prev_data
import json
from bot_commands.reddit.redditfetcher import RedditClient
from bot_commands.reddit.timeoutreddit import Send_again
send_red = Send_again()

reddit_fetcher = RedditClient()


class SubReddit(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def get_subred(self,ctx, check):
		content = await self.bot.wait_for('message', check=check, timeout=10.0)
		
		sub = await reddit_fetcher.fetch_subreddit(str(content.content))
		
		if not sub:
			await ctx.send('Please enter a valid subreddit name')
			
			content = await self.get_subred(ctx, check)

		return content
		

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

		try:
			sub = await self.get_subred(ctx, check)
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

		postObj = await reddit_fetcher.get_posts(sub.content, type)
		posts = postObj.posts

		prev = {
			'server': str(ctx.guild.id),
			'channel': str(ctx.channel.id),
			'posts': posts,
			'sub': sub.content,
			'type': type
		}
		
		with open(reddit) as json_file:
			red = json.load(json_file)
			red['prev-data'].append(prev)
			json_file.close()
		
		with open(reddit, 'w') as json_file:
			json.dump(red, json_file)
			json_file.close()

		await send_red.timeinterval(prev['posts'], channel, ctx.guild)

		self.repeated.start(ctx.guild, channel, str(sub.content), str(type))
	

	@tasks.loop(minutes=30.0)
	async def repeated(self, server, channel, sub, type):
		json_data = json.loads(get_prev_data(f'server={server.id}&channel={channel.id}').text)
		new_posts = []

		postObj = await reddit_fetcher.get_posts(sub, type)
		posts = postObj.posts

		for post in json_data[0]['posts']:
			if posts[0] != post:
				if post in posts:
					break
			new_posts.append(post)

		with open(reddit) as json_file:
			red = json.load(json_file)
		
		for data in red['prev-data']:
			if data['channel'] == str(channel.id) and data['server'] == str(server.id):
				changer = data
				break
		
		changer['posts'] = new_posts
		json_file.close()
		
		with open(reddit, 'w') as json_file:
			json.dump(red, json_file)
			json_file.close()

		await send_red.timeinterval(posts, channel, server)
