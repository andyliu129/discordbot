import discord                     # Import discord, this is the module that allows us to interact with discord
from discord.ext import commands   # Import commands from discord.ext, this is the module that allows us to create commands
from youtube_dl import YoutubeDL    # import youtube_dl



#class for the music cog, this will contain all the music commands
class music_cog(commands.Cog):
    
    def __init__(self, bot):                    #initializes the cog
        self.bot = bot                          #sets the bot, this is the bot that is passed in when the cog is registered
        self.vc = None                          #voice client, this is the voice client that will be used to play music
        self.queue = []                         #queue for the music
        self.playing = False                    #check if the bot is playing music
        self.pause = False                      #check if the bot is paused

        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}   #options for youtube_dl, this is the module that will be used to download the audio from youtube
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}  #options for ffmpeg, this is the module that will be used to play the audio
        
    #searches youtube for the song
    def search(self, song):
        if song == None:
            return False
        else:
            with YoutubeDL(self.YDL_OPTIONS) as ydl:
                try:
                    search = ydl.extract_info(f"ytsearch:{song}", download=False)['entries'][0]
                except Exception:
                    return False
            return {'source': search['formats'][0]['url'], 'title': search['title']}


    #play the next song in the queue
    def next(self):
        
        if len(self.queue) > 0:
            self.playing = True                                                                             #set playing to true
            
            link = self.queue[0][0]['source']                                                               #get the first url
            self.queue.pop(0)                                                                               #remove the first element as you are currently playing it                                          
            
            self.vc.play(discord.FFmpegPCMAudio(link, **self.FFMPEG_OPTIONS), after=lambda e: self.next())  #play the song
        
        else:
            self.playing = False
        
    
    #checking for loops
    async def play_music(self, ctx):
        
        #if the queue is not empty
        if len(self.queue) > 0:
            self.playing = True

            #get the first url
            link = self.queue[0][0]['source']
            
            #try to connect to voice channel if you are not already connected
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.queue[0][1].connect()

                #in case we fail to connect
                if self.vc == None:
                    await ctx.send("Could not connect to voice channel")
                    return
            else:
                await self.vc.move_to(self.queue[0][1])
            
            #remove the first element as you are currently playing it
            self.queue.pop(0)

            #play the song
            self.vc.play(discord.FFmpegPCMAudio(link, **self.FFMPEG_OPTIONS), after=lambda e: self.next())
            
        else:
            self.playing = False
    
    
    @commands.command(name="play", aliases=["p","Play"], help="Plays the selected song from youtube")
    async def play(self, ctx, *args):
        
        query = " ".join(args)
        
        voice_channel = ctx.author.voice.channel
        
        #if the user is not in a voice channel
        if voice_channel is None:
            await ctx.send("Join a VC first.")       #you need to be connected so that the bot knows where to go
            
        elif self.pause:
            self.vc.resume()                                    #resume the song
            
        else:
            song = self.search(query)                           #search for the song
            
            if type(song) == type(True):                        #if the song is not found
                await ctx.send("Song not found, please try again")
                
            else:
                await ctx.send("Song is added to queue")       #add the song to the queue
                self.queue.append([song, voice_channel])  
                
                if self.playing == False:                  
                    await self.play_music(ctx) == True          #play the song if the bot is not playing anything
                    self.vc.source = discord.PCMVolumeTransformer(self.vc.source, volume=0.1)   #set the volume to 10%
                      
                    #***This is the part that is not working***
                    #if PCMVolumeTransformer is not set to 0.1 then the volume is too loud
                    
                    if self.vc.source.volume != 0.1:
                        self.vc.source.volume = 0.1
                    else:
                        await ctx.send("Volume is already set to 0.1")           
                    
    #command to pause the song                   
    @commands.command(name="pause", aliases=["stop","Pause"], help="Pauses the current song")
    async def pause(self, ctx, *args):
        if self.playing:

            self.playing = False        #set playing to false
            self.pause = True           #set pause to true
            self.vc.pause()             #pause the song
            
        else:
            await ctx.send("Nothing is playing")
            

    #command to resume the song
    @commands.command(name = "resume", aliases=["r"], help="Resumes the current song")
    async def resume(self, ctx, *args):
        if self.pause:
            
            self.pause = False      #set pause to false
            self.playing = True     #set playing to true
            self.vc.resume()        #resume the song
            
        else:
            await ctx.send("Nothing is paused")
            
            
    #command to skip the song
    @commands.command(name="skip", aliases=["s"], help="Skips the current song being played")
    async def skip(self, ctx):
        
        if self.vc != None and self.vc: 

            self.vc.stop()                  #stop the song
            await self.play_music(ctx)      #play the next song in the queue

    #command to show the queue
    @commands.command(name="queue", aliases=["q"], help="Displays the current songs in queue")
    async def queue(self, ctx):
        
        queue = ""
        
        if queue != "":
            await ctx.send("Current Queue:\n" + queue)   #display the queue
            
        else:
            await ctx.send("No songs in queue")

    #command to clear the queue
    @commands.command(name="clear", aliases=["c"], help="Stops the music and clears the queue")
    async def clear(self, ctx):
        
        if self.vc != None and self.playing:    
            self.vc.stop()                    #stop the song

        self.queue = []                       #clear the queue
        
        await ctx.send("Music queue cleared") 

    #command to kick the bot from the voice channel
    @commands.command(name="leave", aliases=["disconnect", "l", "d", "kill"], help="Kick the bot from VC")
    async def dc(self, ctx):
        
        self.playing = False        #set playing to false
        self.pause = False          #set pause to false
        
        await self.vc.disconnect(), self.queue.clear(), await ctx.send("Disconnected from VC")  #disconnect from the voice channel, clear the queue, and send a message
        
    #use getters and setters to adjust volume
    #command to adjust volume
    @commands.command(name="volume", aliases=["vol"], help="Adjusts the volume of the bot")
    async def volume(self, ctx, vol: int): 
        
        if self.vc != None and self.vc:                                                                             #setter for volume
            self.vc.source = discord.PCMVolumeTransformer(self.vc.source, volume=vol)
            await ctx.send("Volume set to {}%".format(vol))
            
        else:
            await ctx.send("Not connected to a voice channel")
            
    #command to display the current volume
    @commands.command(name="current volume", aliases=["cv"], help="Displays the current volume of the bot")         #getter for volume
    async def current_volume(self, ctx):
        await ctx.send("Current volume is {}%".format(self.vc.source.volume))
