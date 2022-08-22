# NukerBott  

A simple (?) discord Nuker Bot made by Joee. In order to use this, you must know the basics of python, pip, and how to make a discord bot.
This bot is written in python, and depends on the discord.py v2.0.0 or higher library.

### Changelog:
-=-=-=-=-=-=-

v0.1a
###### [+] Basic nuker command made.
- Deletes all channels.
- Creates {nuking-changelog, nuking-reason, dumbasses-complaining} channels.

###### [+] Stop command made.
- Forcibly closes all connections to discord. This means that to re-run the nuke command, you'll need to re-run the main.py.

###### [+] Implemented `commands.is_owner()`.
- This only allows the bot owner to use the nuke and stop command. This means that even if someone else runs the command, the bot will not respond. By bot owner, I do not mean myself, but the person who created the Bot Application at the [Discord Developer Portal- Applications](https://discord.com/developers/applications)
