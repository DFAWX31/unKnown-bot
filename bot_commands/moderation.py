from multiprocessing.connection import Client
import discord
from discord.ext import commands

class AdminCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, user :discord.Member, *, reason=None, delete_days=0):
		if ctx.author.top_role < user.top_role:
			return await ctx.send('**You dont have enough permissions**')
		await ctx.guild.ban(user, reason=reason, delete_message_days=delete_days)
		await user.send(f"You have been banned from {ctx.guild} for {reason}")
		await ctx.send(f"{user} has been succesfully banned.")


	@commands.command()
	@commands.has_permissions(ban_members=True)
	async def unban(self, ctx, id):
		user = await self.bot.fetch_user(id)
		bans = await ctx.guild.bans()
		
		for ban in bans:
			if ban.user == user:
				await ctx.guild.unban(user)
				await ctx.send(f'Unbanned {user.mention}')


	@commands.command()
	@commands.has_permissions(manage_roles=True)
	async def clear(self, ctx, number):
		number = int(number) + 1
		counter = 0
		await ctx.channel.purge(limit = number)