import discord

class Send_again:
	def reddit_embed(self, post):
		user = post['author']
		url = post['link']
		content = post['content']
		if content != '':
			embed = discord.Embed(title=f'post by {user}', url = url, description=content, color=discord.Color.from_rgb(255,69,0))
		else:
			embed = discord.Embed(title=f'post by {user}', url = url, color=discord.Color.from_rgb(255,69,0))
		if post['post'] != '':
			embed.set_image(url=post['post'])
		embed.set_footer(text='next update in 30 mins')

		return embed

	async def timeinterval(self, posts, channel, server):
		if not server:
			return print('guild not found')
		if not channel:
			return print('channel not found')
		if channel not in server.channels:
			return print('specified channel is not in guild')
		for post in posts:
			await channel.send(embed=self.reddit_embed(post))