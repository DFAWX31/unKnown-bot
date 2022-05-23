from dis import disco
from distutils.command.config import config
from locale import currency
from urllib import response
import json
from config import get_response, secret_code
from config import currency as file
import discord
from discord.ext import commands

class CurrencyCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(help="join the game")
	async def join(self, ctx):
		key = False

		datas = {
			"name":  str(ctx.author.id),
			"balance": 0,
			"secret_code": False
		}

		if len(json.loads(get_response(f'name={ctx.author.id}').text)) == 0:
			key = True
			with open(file) as json_file:
				currency = json.load(json_file)
				currency['currency'].append(datas)
				json_file.close()


			with open(file, 'w') as json_data:
				json.dump(currency, json_data)
				json_data.close()
				
		
		json_data = json.loads(get_response(f"name={ctx.author.id}").text)

		balance = json_data[0]['balance']
		if key:
			await ctx.send(f'{ctx.author.mention} has joined with { balance } ucoins')
		else:
			await ctx.send(f'{ctx.author.mention} has {balance} ucoins')

	@commands.command()
	async def secret(self, ctx, *args):
		message = ' '.join(args)
		json_data = json.loads(get_response(f'name={ctx.author.id}').text)
		if json_data[0]['secret_code']:
			return await ctx.send('you have already claimed this reward!!!')
		if message == secret_code:
			await ctx.send('wow')
			with open(file) as json_file:
				currency = json.load(json_file)
				json_file.close()

			for user in currency['currency']:
				if int(user['name']) == ctx.author.id:
					user['balance'] += 300
					user['secret_code'] = True
			
			with open(file, 'w') as json_file:
				json.dump(currency, json_file)
				json_file.close()

			json_data = json.loads(get_response(f"name={ctx.author.id}").text)
			balance = json_data[0]['balance']

			await ctx.send(f'Your new balance is {balance}')
		else:
			await ctx.send('Wrong promo code')

	@commands.command()
	async def give(self, ctx, member: discord.Member, amount: int):
		json_data = json.loads(get_response(f"name={ctx.author.id}").text)
		balance = json_data[0]['balance']

		if balance < amount:
			return ctx.send('insufficient balance')

		with open(file) as json_data:
			currency = json.load(json_data)
			json_data.close()

		users = currency['currency']

		for user in users:
			if int(user['name']) == ctx.author.id:
				user['balance'] -= amount
			if int(user['name']) == member.id:
				user['balance'] += amount
		
		with open(file, 'w') as json_data:
			json.dump(currency, json_data)
			json_data.close()
		
		await ctx.send(f'{amount} transferred from {ctx.author.mention}\'s balance to {member.mention}\'s balance')
		
	@commands.command(help="show your current balance")
	async def balance(self, ctx, memeber: discord.Member = None):
		if memeber == None:
			json_data = json.loads(get_response(f'name={ctx.author.id}').text)
			balance = json_data[0]['balance']
			return await ctx.send(f'Your balance is {balance}')
		json_data = json.loads(get_response(f'name={memeber.id}').text)
		balance = json_data[0]['balance']
		await ctx.send(f'{memeber.name}\'s balance is {balance}')
		

	