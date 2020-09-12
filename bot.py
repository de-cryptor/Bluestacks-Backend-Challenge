import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')
import discord
from googlesearch import search
from LogManager import LogManager
from discord.ext import commands
import time
import datetime

bot = commands.Bot(command_prefix='!')


# Bot Connection Event
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# This function event will send Welcome Message in DM.
@bot.event
async def on_member_join(member):
    print("New Member joined" , member)
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Bluestacks Discord Server !'
    )


# This function will search on google and returns top 5 links 
@bot.command()
async def google(ctx,*args):
    query = " ".join(args)
    await ctx.send("Searching on Google Please wait....")
    timestamp = time.time() + 19800
    
    # Saving Query in MongoDB with timestamp
    document = dict()
    collection = 'Recent'
    document['search'] = query  
    document['author'] = ctx.message.author.name
    document['timestamp'] = timestamp
    # Using Defined LogManager Class
    log = LogManager(collection,document)
    log.save()
    for url in search(query,stop=5):
        await ctx.send(url)
    
    
#This function will return recent searches by the particual author
@bot.command()
async def recent(ctx, *args):
    collection = 'Recent'
    search_keyword = " ".join(args)
    manager = LogManager(collection)
    author = ctx.message.author.name
    await ctx.send("Fetching your recent Search History Please wait....")
    
    #Searching Results Keyword for Author
    documents = manager.get_recent(search_keyword,author)
    for each in documents:
        timestamp = datetime.datetime.fromtimestamp(each['timestamp']).strftime('%Y-%m-%d | %I:%M %p')
        await ctx.send('{} | Seached on : {}'.format(each['search'],timestamp )) 
    
# On Message Event 
@bot.event
async def on_message(message):

    #Condition to remove recursive messages...
    if message.author == bot.user:
        return
    
    # Reply "Hey !! <username>" on "Hi/hi"
    if message.content.lower() == 'hi':
        await message.channel.send('Hey!! .{}'.format(message.author.name))
    
    # Process Bot Commands on Recieving the messages
    await bot.process_commands(message)
    
if __name__ == "__main__":
    bot.run(TOKEN)