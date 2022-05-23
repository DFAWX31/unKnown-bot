import asyncio
from dataclasses import dataclass
import json
import aiohttp
from async_timeout import timeout
from datetime import datetime, timedelta

BASE_URL = 'https://www.reddit.com'
SUBREDDIT_URL = BASE_URL + '/r/'
REDDITOR_URL = BASE_URL + '/u/'
JSON_URL = '/about.json'

class Client:
	def __init_(self, *, loop=None, session=None):
		self.log_in = None
		self.loop = loop or asyncio.get_event_loop()
		self.session = session or aiohttp.ClientSession(loop=self.loop)

	def error_detected(self, data):
		if "error" in data:
			return data['error']

	async def get_header(self):
		if not self.log_in:
			return {}
		else:
			raise NotImplementedError
	
	async def fetch(self, url):
		try:
			async with timeout(30.0):
				headers = await self.get_header()

				async with self.session.get(url, headers=headers) as resp:
					if resp.status != 200:
						return None

					data = await resp.json()

		except TimeoutError:
			raise TimeoutError(f'Timed out while fetching \'{url}\'')

		if self.error_detected(data):
			return None

		return data

	async def get_posts(self, subreddit, query):
		url = SUBREDDIT_URL + subreddit + '/' + query + '/.json'

		data = await self.fetch(url)

		if data['kind'] != 'Listing':
			return None
		
		posts = Posts(data)

		return posts

	async def fetch_subreddit(self, query):
		url = SUBREDDIT_URL + query + JSON_URL

		data = await self.fetch(url)

		if data['kind'] != 't5':
			return None

		subreddit = Subreddit(data)

		return subreddit

	async def fetch_redditor(self, query):
		url = REDDITOR_URL + query + JSON_URL

		data = await self.fetch(url)

		if data['kind'] != 't2':
			return None

		redditor = Redditor(data)

		return redditor

class Redditor:
	def __init__(self, data):
		data = data['data']
		self.data = data
		self.is_employee = data['is_employee']
		self.name = data['name']
		self.name_prefixed = 'u/' + self.name
		self.link_karma = data['link_karma']
		self.icon_img = data['icon_img']
		self.comment_karma = data['comment_karma']
		self.public_description = data['public_description']
		self.subscribers = data['subscribers']
		self.over18 = data['over18']
		self.description = data['description']
		self.url = BASE_URL + data['url']
		self.created_at = datetime.utcfromtimestamp(data['created_utc'])

	def __str__(self):
		return self.name_prefixed

class Subreddit:
	def __init__(self, data):
		data = data['data']
		self.data = data
		self.display_name = data['display_name']
		self.display_name_prefixed = data['display_name_prefixed']
		self.title = data['title']
		self.header_img = data['header_img']
		self.icon_img = data['icon_img']
		self.subscribers = data['subscribers']
		self.public_description = data['public_description']
		self.over18 = data['over18']
		self.description = data['description']
		self.url = BASE_URL + data['url']
		self.created_at = datetime.utcfromtimestamp(data['created_utc'])

	def __str__(self):
		return self.display_name_prefixed

class Posts:
	def __init__(self, data):
		data = data['data']
		self.posts = []
		for child in data['children']:
			val = child['data']
			if not val['is_video']:
				datas = {
					'post': val['url'],
					'title': val['title'],
					'author': val['author'],
					'link': SUBREDDIT_URL + val['premalink']
				}
				self.posts.append(datas)
