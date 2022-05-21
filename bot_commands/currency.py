from distutils.command.config import config
from urllib import response
import json
from config import get_response, secret_code
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

	def add_coins(self, num: int, id :int, bal: int, file: str, trigger :bool):

		textf = "\t\t\t\"name\": \"" + str(id) + "\",\n\t\t\t\"balance\": " + str(bal) + ",\n\t\t\t\"secret_code\": false"
		textt = "\t\t\t\"name\": \"" + str(id) + "\",\n\t\t\t\"balance\": " + str(bal) + ",\n"

		replacementf = "\t\t\t\"name\": \"" + str(id) + "\",\n\t\t\t\"balance\": " + str(bal+num) + ",\n\t\t\t\"secret_code\": true"
		replacementt = "\t\t\t\"name\": \"" + str(id) + "\",\n\t\t\t\"balance\": " + str(bal+num) + ",\n"


		with open(file, 'r') as f:
			filedata = f.read()
			f.close()

		if trigger:
			filedata = filedata.replace(textf, replacementf)
		else:
			filedata = filedata.replace(textt, replacementt)

		with open(file, 'w') as f:
			f.write(filedata)
			f.close()

	@commands.command(help="join the game")
	async def join(self, ctx):
		key = False

		datas = {
			"name": "\"" + str(ctx.author.id) +"\"",
			"balance": 0,
			"secret_code": "false"
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

	@commands.command()
	async def secret(self, ctx, *args):
		message = ' '.join(args)
		json_data = json.loads(get_response(f"name={ctx.author.id}").text)
		redeemed = json_data[0]['secret_code']
		if redeemed:
			return await ctx.send('You have already redeemed this secret code')
		if message.lower() == secret_code:
			await ctx.send("wow")
			json_data = json.loads(get_response(f"name={ctx.author.id}").text)
			balance = json_data[0]['balance']
			self.add_coins(300, ctx.author.id, balance, 'db.json', True)
			json_data = json.loads(get_response(f"name={ctx.author.id}").text)
			balance = json_data[0]['balance']
			await ctx.send(f'{ctx.author.mention} has {balance} ucoins')
		else:
			await ctx.send('wrong code')
			json_data = json.loads(get_response(f"name={ctx.author.id}").text)
			balance = json_data[0]['balance']
			await ctx.send(f'{ctx.author.mention} has {balance} ucoins')

	@commands.command()
	async def give(self, ctx, user: discord.Member, amount: int):
		json_data = json.loads(get_response(f"name={ctx.author.id}").text)
		balance = json_data[0]['balance']
		if balance < amount:
			return await ctx.send(f'insufficient funds {balance}')
		json_data = json.loads(get_response(f"name={user.id}").text)
		if json_data == []:
			return await ctx.send(f'{user.mention} has to join first')
		balance_given = json_data[0]['balance']
		json_data = json.loads(get_response(f"name={ctx.author.id}").text)
		balance_taken = json_data[0]['balance']
		self.add_coins(-amount, ctx.author.id, balance_taken, 'db.json', False)
		self.add_coins(amount, user.id, balance_given, 'db.json', False)
		await ctx.send(f'now {ctx.author.mention} has {balance_taken - amount} ucoins and {user.mention} has {balance_given + amount}')
		
	@commands.command(help="show your current balance")
	async def balance(self, ctx):
		json_data = json.loads(get_response(f'name={ctx.author.id}').text)
		balance = json_data[0]['balance']
		await ctx.send(f'Your balance is {balance}')

	