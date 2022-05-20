from urllib import response
import json
from config import response
import discord
from discord.ext import commands
import pymongo

json_data = json.loads(response.text)

class CurrencyCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def find_replacement(self, args):
		keys = args.keys()
		replacement = "\t\t},\n\t\t{\n"
		
		for key in keys:
			replacement += "\t\t\t\"" + str(key) + "\": "
			replacement += str(args.get(key)) + ",\n"
		
		l = len(replacement)
		replacement = replacement[:l - 2]
		replacement += "\n\t\t}\n"

		return replacement


	def add_data(self, datas):
		replacement = self.find_replacement(datas)
		text = "\t\t}\n"
		with open('db.json', 'r') as f:
			filedata = f.read()
			f.close()
		
		filedata = filedata.replace(text, replacement)

		with open('db.json', 'w') as f:
			f.write(filedata)
			f.close()			

	@commands.command(help="join the game")
	async def join(self, ctx):
		datas = {
			"name": "\"" +ctx.author.name+"#"+ctx.author.discriminator +"\"",
			"amount": 0,
			"room": "false"
		}

		self.add_data(datas)

		with open('db.json') as f:
			print(f.readlines())

		await ctx.send('help me pls')
