import discord
from discord.ext import commands
import urllib.request
import re
import bot_functions as bf
from discord import FFmpegPCMAudio
import youtube_dl
import os
import time


#Standard youtube_dl download options
ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }


client = commands.Bot(command_prefix = "$")


#Prints ready in terminal when bot can be used in server
@client.event
async def on_ready():
    print("ready")


#Joins voice channel of user who made call
@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel

        global voice
        voice = await channel.connect()

    else:
        await ctx.send("Join Voice Channel")


#Leaves voice channel
@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()

    else:
        await ctx.send("Not in Voice Channel")


#Plays the requested song
@client.command(pass_context = True)
async def play(ctx, arg):
    
    #Removes previous song file
    if os.path.exists("song.mp3"):
        os.remove("song.mp3")
    
    #Uses song_url function from bf file to get url
    url = bf.song_url(arg)
    
    #Passes URL into a library that downloads youtube videos
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")

    await ctx.send(url)
    
    #Pass the audio file into FFmpeg to play in voice channel
    source = FFmpegPCMAudio("song.mp3")
    player = voice.play(source)


@client.command(pass_context = True)
async def pause(ctx):
    voice.pause()


@client.command(pass_context = True)
async def end(ctx):
    voice.stop()


@client.command(pass_context = True)
async def resume(ctx):
    voice.resume()


client.run('TOKEN_ID')  
