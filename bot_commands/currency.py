from urllib import response
import json
from config import get_response
import discord
from discord.ext import commands

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


	def add_data(self, datas, file):
		replacement = self.find_replacement(datas)
		text = "\t\t}\n"
		with open(file, 'r') as f:
			filedata = f.read()
			f.close()
		
		filedata = filedata.replace(text, replacement)

		with open(file, 'w') as f:
			f.write(filedata)
			f.close()			

	@commands.command(help="join the game")
	async def join(self, ctx):
		key = False

		datas = {
			"name": "\"" + str(ctx.author.id) +"\"",
			"balance": 0,
			"room": "false"
		}
		if json.loads(get_response(f'name={ctx.author.id}').text) == []:
			key = True
			file = 'db.json'

			self.add_data(datas, file)

		json_data = json.loads(get_response(f"name={ctx.author.id}").text)

		balance = json_data[0]['balance']
		if key:
			await ctx.send(f'{ctx.author.mention} has joined with { balance } ucoins')
		else:
			await ctx.send(f'{ctx.author.mention} has {balance} ucoins')

