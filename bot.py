# bot.py
import os
import random
import responses
import discord
import subprocess
import time
from dotenv import load_dotenv
from discord.ext import commands
import socket
from contextlib import closing
from discord.ext.commands import has_permissions, CheckFailure
import threading

async def send_message(message, user_message, is_private):
	try:
		response = responses.handle_response(user_message)
		await message.author.send(response) if is_private else await message.channel.send(response)
	except Exception as e:
		print(e)



def run_discord_bot_message():
	load_dotenv()
	TOKEN = os.getenv('DISCORD_TOKEN')
	GUILD = os.getenv('DISCORD_GUILD')
	intents = discord.Intents.default()
	intents.message_content = True
	intents.members = True
	client = discord.Client(intents = intents)

	@client.event
	async def on_ready():
		print(f'{client.user} is now running!')
	
	@client.event
	async def on_message(message):
		if message.author == client.user:
			return
		username = str(message.author)
		user_message = str(message.content)
		channel = str(message.channel)
		print(f"{username} said: '{user_message}' ({channel})")
		if user_message[0] == '?':
			user_message = user_message[1:]
			await send_message(message, user_message, is_private=True)
		else :
			await send_message(message, user_message, is_private=False)
	
	@client.event
	async def on_reaction_add(reaction, user):
		if str(reaction.emoji) == "➡️":
			print("right")
		if str(reaction.emoji) == "⬅️":
			print("left")

	client.run(TOKEN)





def run_discord_bot_command():
	load_dotenv()
	TOKEN = os.getenv('DISCORD_TOKEN')
	GUILD = os.getenv('DISCORD_GUILD')
	intents = discord.Intents.default()
	intents.message_content = True
	intents.members = True
	bot = commands.Bot(command_prefix="!", intents=intents)

	@bot.command(name='spam', help='Spam l''utilisateur spécifié. \nSyntaxe: !spam <utilisateur> <nombre de messages> <message>')
	@has_permissions(administrator=True)
	async def spam(ctx, user:discord.Member, amount=10, *, message="Je suis Dahyun"):
		print("spamming " + str(user) + " with " + message)
		embed = discord.Embed(title=message, color=0xff0000)
		for i in range(amount):
			await user.send(embed=embed)
			time.sleep(0.5)
	
	@bot.command(name='clear', help='Efface les x derniers messages. Sinon, efface le dernier message')
	@has_permissions(manage_messages=True)
	async def clear(ctx, amount=1):
		await ctx.channel.purge(limit=amount+1)

	@bot.command(name='quatuor',help='Choisit un des membres du quatuor au hasard')
	async def quatuor(ctx):
		quatuor = ['Antony','Alex','Romain','Maxime']
		print(quatuor)
		await ctx.channel.send(random.choice(quatuor))

	@bot.command(name='goulag',help='Choisit un membre au hasard')
	async def goulag(ctx):
		users = []
		for guild in bot.guilds:
			for member in guild.members:
				if ((str)(member).find("Dahyun#6588") == -1):
					users.append(member)
		await ctx.channel.send(random.choice(users))

	domainWhiteListed = []
	@bot.command(name='dns-add-w', help="Ajoute un domaine sur la liste blanche\nA utiliser pour débloquer un domaine qui semble bloqué par erreur\nVous pouvez ajouter plusieurs domaines en les séparant d'un espace")
	async def dnsAddW(ctx, *, domain):
		os.system('''ssh root@192.168.42.63 "pihole -w ''' + domain + '''"''')
		domainWhiteListed.append(domain)
		await ctx.send('Domaine(s)' + domain + ' ajouté(s) à la liste blanche')

	@bot.command(name='dns-cancel-w', help="Annule la dernière ittération de dns-add-w")
	async def dnsDelW(ctx):
		if len(domainWhiteListed) > 0:
			os.system('''ssh root@192.168.42.63 "pihole -w -d ''' + domainWhiteListed[-1] + '''"''')
			domainWhiteListed.pop()
			await ctx.send('Domaine(s) retiré(s) de la liste blanche')
		else:
			await ctx.send('Aucun domaine n\'a été ajouté dernièrement')

	@bot.event
	async def on_command_error(ctx, error):
		response = ['T\'as cru t\'étais qui ?', 'Mais pour qui te prends-tu ?', 'Calme toi', 'Calme toi misérable', 'Redescends sale INSOLENT !']
		if isinstance(error, commands.errors.CheckFailure):
			await ctx.send(random.choice(response))

	bot.run(TOKEN)








"""
def check_port(host, port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((host, port)) == 0:
            return True
        else:
            return False

@bot.command(name='terra-restart', help='Démarre ou redémarre les serveurs Terraria')
@commands.has_any_role('hyper', 475077706837655564, 'admin', 'terraria')
async def restartTerraServers(ctx):
	if ctx.channel.name == 'terraria' :
		start = time.time()
		await ctx.send('Ok, c\'est en cours')
		os.system(f'./terraria/runTerrariaServers.sh ENTER')
		while True:
			time.sleep(1)
			if check_port('127.0.0.1',7777) and check_port('127.0.0.1',8888):
				break
		await ctx.send('Serveurs Terraria ouverts en ' + str(round(time.time()-start)) + ' secondes')

@bot.command(name='terra-close', help='Ferme les serveurs Terraria')
@commands.has_any_role('hyper', 475077706837655564, 'admin', 'terraria')
async def closeTerraServers(ctx):
	if ctx.channel.name == 'terraria' :
		await ctx.send('Attends je sauvegarde')
		os.system(f'./terraria/closeTerrariaServers.sh ENTER')
		await ctx.send('C\'est bon')

@bot.command(name='terra-stats', help='Retourne les statistiques des serveurs Terraria')
async def statsTerraServers(ctx):
	if ctx.channel.name == 'terraria' :
		main = ':no_entry:'
		sec = ':no_entry:'
		if check_port('127.0.0.1', 7777):
			main=':white_check_mark:'
		if check_port('127.0.0.1', 8888):
			sec=':white_check_mark:'
		await ctx.send(main + '  Serveur principale\n' + sec + '  Serveur secondaire ')
"""