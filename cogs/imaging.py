import discord, random
from discord.ext import commands
import json
import os
import subprocess
import asyncio
from io import StringIO
import sys
import aiohttp
import io



class imaging(commands.Cog, name='imaging'):
	def __init__(self, bot):
		self.bot = bot
	@commands.command()
	async def triggered(self,ctx, member: discord.Member=None):
			if not member: # if no member is mentioned
					member = ctx.author # the user who ran the command will be the member
			async with aiohttp.ClientSession() as wastedSession:
					async with wastedSession.get(f'https://some-random-api.ml/canvas/triggered?avatar={member.avatar_url_as(format="png", size=1024)}') as wastedImage: # get users avatar as png with 1024 size
							imageData = io.BytesIO(await wastedImage.read()) # read the image/bytes
							
							await wastedSession.close() # closing the session and;
							
							await ctx.reply(file=discord.File(imageData, 'triggered.gif')) # sending the file
	@commands.command()
	async def gay(self,ctx, member: discord.Member=None):
			if not member: # if no member is mentioned
					member = ctx.author # the user who ran the command will be the member
					
			async with aiohttp.ClientSession() as wastedSession:
					async with wastedSession.get(f'https://some-random-api.ml/canvas/gay?avatar={member.avatar_url_as(format="png", size=1024)}') as wastedImage: # get users avatar as png with 1024 size
							imageData = io.BytesIO(await wastedImage.read()) # read the image/bytes
							
							await wastedSession.close() # closing the session and;
							
							await ctx.reply(file=discord.File(imageData, 'gay.png')) # sending the file
	@commands.command()
	async def glass(self,ctx, member: discord.Member=None):
			if not member: # if no member is mentioned
					member = ctx.author # the user who ran the command will be the member
					
			async with aiohttp.ClientSession() as wastedSession:
					async with wastedSession.get(f'https://some-random-api.ml/canvas/glass?avatar={member.avatar_url_as(format="png", size=1024)}') as wastedImage: # get users avatar as png with 1024 size
							imageData = io.BytesIO(await wastedImage.read()) # read the image/bytes
							
							await wastedSession.close() # closing the session and;
							
							await ctx.reply(file=discord.File(imageData, 'glass.png')) # sending the file
	@commands.command()
	async def pixelate(self,ctx, member: discord.Member=None):
			if not member: # if no member is mentioned
					member = ctx.author # the user who ran the command will be the member
					
			async with aiohttp.ClientSession() as wastedSession:
					async with wastedSession.get(f'https://some-random-api.ml/canvas/pixelate?avatar={member.avatar_url_as(format="png", size=1024)}') as wastedImage: # get users avatar as png with 1024 size
							imageData = io.BytesIO(await wastedImage.read()) # read the image/bytes
							
							await wastedSession.close() # closing the session and;
							
							await ctx.reply(file=discord.File(imageData, 'pixel.png')) # sending the file
	@commands.command()
	async def color(self,ctx, hex):
					
			async with aiohttp.ClientSession() as wastedSession:
					async with wastedSession.get(f'https://some-random-api.ml/canvas/colorviewer?hex={hex}') as wastedImage: # get users avatar as png with 1024 size
							imageData = io.BytesIO(await wastedImage.read()) # read the image/bytes
							
							await wastedSession.close() # closing the session and;
							
							await ctx.reply(file=discord.File(imageData, 'color.png')) # sending the file
	@commands.command()
	async def greyscale(self,ctx, member: discord.Member=None):
			if not member: # if no member is mentioned
					member = ctx.author # the user who ran the command will be the member
					
			async with aiohttp.ClientSession() as wastedSession:
					async with wastedSession.get(f'https://some-random-api.ml/canvas/greyscale?avatar={member.avatar_url_as(format="png", size=1024)}') as wastedImage: # get users avatar as png with 1024 size
							imageData = io.BytesIO(await wastedImage.read()) # read the image/bytes
							
							await wastedSession.close() # closing the session and;
							
							await ctx.reply(file=discord.File(imageData, 'grey.png')) # sending the file
	@commands.command()
	async def invert(self,ctx, member: discord.Member=None):
			if not member: # if no member is mentioned
					member = ctx.author # the user who ran the command will be the member
					
			async with aiohttp.ClientSession() as wastedSession:
					async with wastedSession.get(f'https://some-random-api.ml/canvas/invert?avatar={member.avatar_url_as(format="png", size=1024)}') as wastedImage: # get users avatar as png with 1024 size
							imageData = io.BytesIO(await wastedImage.read()) # read the image/bytes
							
							await wastedSession.close() # closing the session and;
							
							await ctx.reply(file=discord.File(imageData, 'invert.png')) # sending the file
def setup(bot):
    bot.add_cog(imaging(bot))
