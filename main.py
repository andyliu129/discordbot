import discord
from discord.ext import commands

#import all of the cogs
from help_cog import help_cog   
from music_cog import music_cog


#this is the prefix for the bot, it is used to call the commands, for example "=help"
bot = commands.Bot(command_prefix='=')

#command to change the prefix
@commands.command(name="prefix", aliases=["pre","pf"], help="Changes the prefix for the bot")
async def prefix(self, ctx, *args):
    if len(args) == 1:
        bot.command_prefix = args[0]
        await ctx.send("Prefix changed to " + args[0])
    else:
        await ctx.send("Please enter a valid prefix")

#this removes the default help command that is built into discord.py
bot.remove_command('help')

#add the cogs to the bot
bot.add_cog(help_cog(bot))
bot.add_cog(music_cog(bot))

#start the bot with our token
#the token is a secret and should not be shared with anyone
bot.run("TOKEN")
