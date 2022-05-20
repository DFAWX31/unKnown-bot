import discord
from discord.ext import commands


class TestCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def test(self, ctx, *args):
		await ctx.send('{} arguments: {}'.format(len(args), ' '.join(args)))
		await ctx.author.send('{} arguments: {}'.format(len(args), ''.join(args)))
		print(ctx.author.name + "#" + ctx.author.discriminator)
		