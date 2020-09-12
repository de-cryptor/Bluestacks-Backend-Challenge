import os
import discord
from config import TOKEN,GUILD
from googlesearch import search
from LogManager import LogManager
from discord.ext import commands
import time
import datetime

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_member_join(member):
    print("New Member joined" , member)
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Bluestacks Discord Server !'
    )

@bot.command()
async def google(ctx,*args):
    query = " ".join(args)
    await ctx.send("Searching on Google Please wait....")
    timestamp = time.time()
    document = dict()
    collection = 'Recent'
    document['search'] = query  
    document['author'] = ctx.message.author.name
    document['timestamp'] = timestamp
    log = LogManager(collection,document)
    log.save()
    for url in search(query,stop=5):
        await ctx.send(url)
    
@bot.command()
async def recent(ctx, *args):
    collection = 'Recent'
    search_keyword = " ".join(args)
    manager = LogManager(collection)
    author = ctx.message.author.name
    await ctx.send("Fetching your recent Search History Please wait....")
    documents = manager.get_recent(search_keyword,author)
    for each in documents:
        timestamp = datetime.datetime.fromtimestamp(each['timestamp']).strftime('%Y-%m-%d | %I:%M %p')
        await ctx.send('{} | Seached on : {}'.format(each['search'],timestamp )) 
    

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return
    
    if message.content.lower() == 'hi':
        await message.channel.send('Hey!! .{}'.format(message.author.name))
    
    await bot.process_commands(message)
    
if __name__ == "__main__":
    bot.run(TOKEN)