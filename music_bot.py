import discord
from discord.ext import commands
import urllib.request
import re
import bot_functions as bf
from discord import FFmpegPCMAudio
import youtube_dl
import os
import time

ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }


client = commands.Bot(command_prefix = "$")


@client.event
async def on_ready():
    print("ready")


@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel

        global voice
        voice = await channel.connect()

    else:
        await ctx.send("Join Voice Channel")



@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()

    else:
        await ctx.send("Not in Voice Channel")


@client.command(pass_context = True)
async def play(ctx, arg):
    
    if os.path.exists("song.mp3"):
        os.remove("song.mp3")

    url = bf.song_url(arg)
    

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")

    await ctx.send(url)

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



client.run('ODY1MzkyNzk5OTQyNzA1MTky.YPDV2Q.j1z2UJvZkBqG4g2UBTY-s1l2RvE')  