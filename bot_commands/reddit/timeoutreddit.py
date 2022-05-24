import discord

class Send_again:
	def reddit_embed(self, post):
		user = post['author']
		url = post['link']
		content = post['content']
		if content != '':
			embed = discord.Embed(title=f'post by {user}', url = url, description=content, color=0xff4500)
		else:
			embed = discord.Embed(title=f'post by {user}', url = url, color=0xff45000)
		if post['post'] != '':
			embed.set_image(url=post['post'])
		embed.set_footer('next update in 30 mins')

	async def timeinterval(self, posts, channel :int, server :int):
		try:
			guild = self.bot.get_guild(str(server))
			channel = self.bot.get_channel(str(channel))
		except:
			return print('channel/ guild not found')
		if guild == None:
			return print('guild not found')
		if channel == None:
			return print('channel not found')
		if channel not in guild.channels:
			return print('specified channel is not in guild')
		for post in posts:
			await channel.send(embed=self.reddit_embed(post))