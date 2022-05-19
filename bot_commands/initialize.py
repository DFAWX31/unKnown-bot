from dis import disco
from turtle import title
import discord
from discord.ext import commands

class Initialize(commands.Cog):
	def __init__(self,bot):
		self.bot = bot

	setups = {
		"1️⃣": "set-up roles message channel",
		"2️⃣": "set-up welcome channel and message",
		"3️⃣": "setup roles"
	}

	def initEmbed(self):
		embed = discord.Embed(title="Initialization", description="Set bot defaults", color=0xebb434)
		
			

	# async def init(self):
