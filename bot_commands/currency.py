from urllib import response
from temp import add_data
import json
from config import response
import discord
from discord.ext import commands

json_data = json.loads(response.text)

class CurrencyCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(help="join the game")
	async def join(self, ctx):
		obj = {
			"name": ,
		}