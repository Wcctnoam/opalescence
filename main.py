import discord
from discord.ext import commands
import asyncio
from os import listdir
from os.path import isfile, join
import sys
sys.path.append('..')
from config import *
import traceback
from datetime import datetime

cogs_dir = "cogs"

bot = commands.Bot(command_prefix='?')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    bot.loop.create_task(status_task())

@bot.command()
@commands.has_any_role('Cool Squad','Admin','Mods')
async def load(extension_name : str):
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("{} loaded.".format(extension_name))

@bot.command()
@commands.has_any_role('Cool Squad','Admin','Mods')
async def unload(extension_name : str):
    module = bot.extensions.get(extension_name)
    if module is None:
        await bot.say("```py\n"+"ModuleNotFoundError: No module named '"+extension_name+"'\n```")
        return
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    await bot.say("{} unloaded.".format(extension_name))
    
@bot.command()
@commands.has_any_role('Cool Squad','Admin','Mods')
async def reload(extension_name : str):
    module = bot.extensions.get(extension_name)
    if module is None:
        await bot.say("```py\n"+"ModuleNotFoundError: No module named '"+extension_name+"'\n```")
        return
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    #await bot.say("{} unloaded.".format(extension_name))
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("{} reloaded.".format(extension_name))

async def status_task():
    while True:
        count = bot.get_server('98609319519453184').member_count
        status1 = discord.Game(name='with '+str(count)+' ponies',type=1)
        await bot.change_presence(game=status1)
        await asyncio.sleep(10)
    
    
async def connect():
    #print('Logging in...')
    while not bot.is_closed:
        try:
            await bot.start(token)
            bootTime = str(datetime.utcnow()).split('.')[0]+' UTC'
            await self.bot.send_message(self.bot.get_channel('350179664112779276'), "```Restarted Opalescence at "+bootTime+"```")
        except:
            traceback.print_exc()
            await asyncio.sleep(5)
            print("\n---Restarting bot...\n")
    
if __name__ == "__main__":
    extensionss = []
    for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
        extensionss.append(extension)
        if extension in ignoredmodules:
            extensionss.pop()
            continue
        else:
            try:
                bot.load_extension(cogs_dir + "." + extension)
            except Exception as e:
                print('Failed to load extension {extension}.'.format(extension))
                traceback.print_exc()
    print("Loaded: "+(' '.join(extensionss)))
    
    bot.loop.run_until_complete(connect())
    
