from dis import disco
import discord
from discord.ext import commands
from bot_commands.reddit.redditfetcher import RedditClient
from config import get_reddit_user,reddit
import json
reddit_fetcher = RedditClient()


class RedditUser(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(help='link reddit account')
	async def user(self, ctx, reddit_username :str = None, user :discord.Member = None):
		if not reddit_username and not user:
			user = ctx.author
		if not reddit_username:
			try:
				json_data = json.loads(get_reddit_user(f'id={user.id}').text)
				if not len(json_data):
					return await ctx.send('reddit is not linked')
				user_data = json_data[0]
			except:
				return await ctx.send('failed to get user data')
		else:
			reddit_name = reddit_fetcher.fetch_redditor(reddit_username)
			if not reddit_name:
				return await ctx.send(f'failed to find user {reddit_username}')
			with open(reddit) as json_file:
				user_details = json.load(json_file)
				json_file.close()

			datas = {
				'id' : str(ctx.author.id),
				'data': reddit_name.url,
				'name': reddit_name.name,
				'icon': reddit_name.icon_img
			}
			user_details['user-data'].append(datas)

			with open(reddit, 'w') as json_file:
				json.dump(user_details, json_file)
				json_file.close()

			
			try:
				json_data = json.loads(get_reddit_user(f'id={user.id}').text)
				if not len(json_data):
					return await ctx.send('reddit is not linked')
				user_data = json_data[0]
			except:
				return await ctx.send('failed to get user data')

			await ctx.send(str(user_data['data']), str(user_data['name']))

		
