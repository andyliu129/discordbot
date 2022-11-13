import discord                   #import discord.py
from discord.ext import commands #Import the commands extension

class help_cog(commands.Cog):       #inheriting from commands.Cog
    
    def __init__(self, bot):        #constructor
        
        self.bot = bot              #assigning bot to self.bot, this is so that we can use the bot in the cog 
        self.list = []              #list of text channels where the bot is allowed to send messages
        
        self.help_off = False       #set the help_off variable to false, this will be used to turn the help message off and on
        self.help_on_message = "```Help is now on, type =help for info```"     #set the help_on_message variable to the message that will be sent when the help is turned on
        self.help_off_message = "```Help is now off, type =help for info```"   #set the help_off_message variable to the message that will be sent when the help is turned off
        self.help_message= """```

***___Music commands:___***
____________________________________________________________
='help (h)' - 

='play (p) <keywords>' - Finds the song on youtube and plays it in your current channel. Will resume playing the current song if it was paused
='queue (q)' - Shows the current music queue, if there is one.
='skip' - Skips the song that is playing right now
='clear' - Clears the queue, including the song that is playing right now
='pause' - Pauses the song that is playing right now
='resume' - Resumes the current song that is paused
='leave' - Duuh, leaves the voice channel lol
='volume (v) <number>' - Sets the volume of the bot, the number must be between 0 and 100
='current volume (cv)' - Shows the current volume of the bot
='current (c)' - Shows the current song that is playing right now
='shuffle (s)' - Shuffles the queue
____________________________________________________________

***___Help commands:___***

='help off' - turns off the help message
='help on' - turns on the help message
='add channel' - adds the current channel to the list of channels where the bot is allowed to send messages
='remove channel' - removes the current channel from the list of channels where the bot is allowed to send messages
='edit help <message>' - edits the help message (pls don't abuse this)
____________________________________________________________

```
"""

    #command to display all the available commands
    @commands.command(name="help", aliases=["h"], help="Sends all help commands")   #decorator to register the command
    async def help(self, ctx):  #function that will be called when the command is used
        await ctx.send(self.help_message)   #send the help message to the channel where the command was used  


    #disables the help command
    @commands.command(name="help off", aliases=["Help off"], hidden=True)                       #decorator to register the command
    async def help_off(self, ctx):                                                              #the command function                                     
        self.bot.remove_command("help")                                                         #remove the help command 
        await ctx.send("Help command disabled")                                                 #send a message to the user
        
        
    #enables the help command
    @commands.command(name="help on", aliases=["Help on"], hidden=True)                         #decorator to register the command    
    async def help_on(self, ctx):                                                               #the command function
        self.bot.add_command(self.help)                                                         #add the help command                        
        await ctx.send("Help command enabled")                                                  #send a message to the user          
                 
    
    #adds the text channel to the list of text channels where the bot is allowed to send messages
    @commands.command(name="add channel", aliases=["Add channel"], hidden=True)
    async def add_channel(self, ctx):
        if ctx.channel not in self.list:
            self.list.append(ctx.channel)
            await ctx.send("Channel added")
        else:
            await ctx.send("Channel already added")
    
    
    #removes the text channel from the list of text channels where the bot is allowed to send messages
    @commands.command(name="remove channel", aliases=["Remove channel"], hidden=True)
    async def remove_channel(self, ctx):
        if ctx.channel in self.list:
            self.list.remove(ctx.channel)
            await ctx.send("Channel removed")
        else:
            await ctx.send("Channel not added")
            
           
    #edit the help message, can be used to add new commands or do something creative/chaotic with it
    @commands.command(name="edit help", aliases=["Edit help", "edit"], hidden=True)
    async def edit_help(self, ctx, *, message):
        if ctx.channel in self.list:
            self.help_message = message
            await ctx.send("Help message edited")
        else:
            await ctx.send("Bot not allowed to send messages in this channel")  