import discord
from discord.ext import commands
from AnilistPython import Anilist
anilist = Anilist()
from config import reactions

class AnimeCommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def is_integer(self,string):
		try:
			int(string)
			return True
		except ValueError:
			return False

	@commands.command(name="animesearch",help="get anime by name or id")
	async def _animesearch(self, ctx, *args):
		command = ' '.join(args)
		if self.is_integer(command):
			anime_dict = anilist.get_anime_with_id(command)
		else:
			anime_dict = anilist.get_anime(command)
		message = await ctx.send(anime_dict)

		reaction_list = reactions(4)

		for reaction in reaction_list:
			await message.add_reaction(reaction)

		



