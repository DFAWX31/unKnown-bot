from dis import disco
from multiprocessing.connection import Client
from sqlite3 import connect
from turtle import color, position
import discord
from discord.ext import commands

class AdminCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(help="Ban a member by mention")
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, user :discord.Member, *, reason=None, delete_days=0):
		if ctx.author.top_role < user.top_role:
			return await ctx.send('**You dont have enough permissions**')
		await ctx.guild.ban(user, reason=reason, delete_message_days=delete_days)
		await user.send(f"You have been banned from {ctx.guild} for {reason}")
		await ctx.send(f"{user} has been succesfully banned.")

	@commands.command(help="unban a user by user id")
	@commands.has_permissions(ban_members=True)
	async def unban(self, ctx, id):
		user = await self.bot.fetch_user(id)
		bans = await ctx.guild.bans()
		
		for ban in bans:
			if ban.user == user:
				await ctx.guild.unban(user)
				await ctx.send(f'Unbanned {user.mention}')

	@commands.command(help="purge x amount of messages")
	@commands.has_permissions(manage_roles=True)
	async def purge(self, ctx, number):
		number = int(number) + 1
		await ctx.channel.purge(limit = number)

	@commands.command(help="mute a user")
	@commands.has_permissions(manage_messages=True)
	async def mute(self, ctx, user :discord.Member = None, *, time=1):
		muted = discord.utils.get(ctx.guild.roles, name='Muted')
		if muted == None:
			permissions = discord.Permissions(send_messages=False, add_reactions=False, connect=False, )
			await ctx.guild.create_role(name='Muted', permissions=permissions, color=0xffffff)
			muted = discord.utils.get(ctx.guild.roles, name='Muted')
			rules = {
				muted: discord.PermissionOverwrite(read_messages=False, send_messages=False, connect=False, read_message_history=False, )
			}
			
			for category in ctx.guild.categories:
				print(category.name)
				await category.edit(overwrites=rules)
				for channel in category.channels:
					await channel.edit(overwrites=rules)
			rules = {
				muted: discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True, connect=True)
			}
			for role in ctx.guild.roles:
				print(role.name)
				if role != muted:
					rules.update({role: discord.PermissionOverwrite(read_messages=False, send_messages=False, connect=False, read_message_history=False)})
			category = await ctx.guild.create_category(name="muted", overwrites = rules)
			await category.create_text_channel(name="muted-chat", overwrites = rules)
			await category.create_voice_channel(name="muted-voice", overwrites = rules)

				
		
		pos = {
			muted: 1,
		}

		await ctx.guild.edit_role_positions(positions=pos)
		
		if user.top_role > ctx.author.top_role:
			return await ctx.send('You cannot mute this user')

		if user == None:
			return await ctx.send('Please mention a user')

		await user.add_roles(muted)
		await user.send(f'You were muted for {time} hours')
		await ctx.send(f'{user.display_name}was muted for {time} hours')

	@commands.command(help="unmute user")
	@commands.has_permissions(manage_messages=True)
	async def unmute(self, ctx, user :discord.Member):
		muted = discord.utils.get(ctx.guild.roles, name='Muted')
		if muted in user.roles:
			await user.remove_roles(muted)
		else:
			await ctx.send('Please mute the user before unmuting')
