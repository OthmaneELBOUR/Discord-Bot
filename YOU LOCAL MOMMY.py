import discord
from discord.ext import commands
import os
import random
from dotenv import load_dotenv
import time
import asyncio

"""
------------------main code------------------
"""

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix = 'mommy ')

nickname = ["Honey", "Sweetie", "Sweetheart", "Love", "Darling", "Baby"]
comment = ["", "Funny right?"]
your_mom_answers = ["You callled", "Yes"]

#-----------------------------------------------------------------

@bot.event

async def on_ready():
	print("Logged in as '{0.user}'".format(bot))
	while True:
		print("Cleared the file")
		await asyncio.sleep(30)
		with open("spam_detect.txt", "r+") as file:
			file.truncate(0)


#-----------------------------------------------------------------

@bot.event

async def on_message(message):
	username = str(message.author).split('#')[0]
	content = str(message.content)
	channel = str(message.channel.name)
	counter = 0
	print(f"{username} : {content} ({channel})")

	if bot.user == message.author:
		return


	if content.lower()[0:11] == "hello mommy" or ("hi" in content.lower()[0:8] and "mommy" in content.lower()[0:8]):
		await message.channel.send(f"Hey {nickname[random.randint(0,5)]}!")
	
	elif "bye" in content.lower() :
		await message.channel.send(f"Take care {nickname[random.randint(0,5)]}!")
	
	elif content.lower()[:8] == "your mom" or content.lower()[:6] == "ur mom":
		await message.channel.send(f"{your_mom_answers[random.randint(0, 1)]} {nickname[random.randint(0,5)]}?")
		
	elif len(content.lower()) == 3 and content.lower()[1] == 'w':
		await message.channel.send("*pat pat*")
	elif "love you mommy" in content.lower():
		await message.channel.send(f"I love you too {nickname[random.randint(0,5)]}!")
	
#---------Spam detection--------------
	with open("spam_detect.txt", "r+") as file:
		for line in file:
			if line.strip('\n') == str(message.author.id):
				counter += 1
		file.writelines(f"{str(message.author.id)}\n")
		if counter > 5:
			await message.author.add_roles(discord.utils.get(message.author.guild.roles, name="Muted people"))
#-------------------------------------

	await bot.process_commands(message)	#allows command even with on_message

#-------------------------------------------------------------------------------------------------------------

@bot.command(
			help = "Sends 'Pong!' and the latency",
			brief = "Sends your ping back"
			)

async def ping(message):
    await message.channel.send(f'Pong! {round (bot.latency * 1000)}ms ')
    return
    
#-------------------------------------------------------------------------------------------------------------

@bot.command(
			help = "Tells a random joke",
			brief = "Tells a random joke"
			)

async def joke(message):
	f = open("Jokes.txt", "r")
	jokes = f.readlines()
	await message.channel.send(f"{jokes[random.randint(0,10)]}")
	f.close()
	k = random.randint(0,1)
	if k == 1:
		time.sleep(1)
		await message.channel.send(f"{comment[k]}")


#-------------------------------------------------------------------------------------------------------------
#aiko no ai, dakishimete
@bot.command(
			help = "Gives you a hug",
			brief = "Gives love back"
			)
async def hug(message):
	await message.channel.send(f"Aww {nickname[random.randint(0,5)]}!")
	time.sleep(1)
	await message.channel.send("*hug*")

#-------------------------------------------------------------------------------------------------------------
@bot.command(
			help = "Creates a channel",
			brief = "creates a channel"	
 			)
async def vcreate(message, *arg):
	try:
		name = ""
		for i in range(len(arg)):
			name += arg[i] + " "
		await message.guild.create_voice_channel(name[:-1], position = 4)
	except:
		await message.guild.create_voice_channel("Voice Channel", position = 4)
	print(f"{name} channel is created!")

bot.run(token)


