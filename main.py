import sys

sys.path.append('venv/lib/site-packages') # for access through batch file

import discord
from discord.ext import commands
import os
import random
import asyncio

files_calm = os.listdir("music/calm") # get all files from music/calm (you must place your mp3 there)
audios_calm = []
for key in files_calm:
    extension = key.split('.')
    if (extension[1] == 'mp3'):
        audios_calm.append(key)
random.shuffle(audios_calm)

files_move = os.listdir("music/move") # get all files from music/move (you must place your mp3 there)
audios_move = []
for key in files_move:
    extension = key.split('.')
    if (extension[1] == 'mp3'):
        audios_move.append(key)
random.shuffle(audios_move)

audios_rand = [] # randomize for music/calm && music/move folders
for key in audios_calm:
    newKey = "calm/" + key
    audios_rand.append(newKey)
for key in audios_move:
    newKey = "move/" + key
    audios_rand.append(newKey)
random.shuffle(audios_rand)

music_id_calm = 0
music_id_move = 0
music_id_rand = 0
music_stopped = False
music_playList = False
music_list = ""
cur_play_name = ""
cur_play_path = ""

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

client = commands.Bot(command_prefix="!")
token = "" # your bot token
voiceChannelName = "General" # your voice channel you would like bot to join

def queue(url_):
    global music_list
    music_list = url_
    global audios_calm
    global audios_move
    global audios_rand
    global audios_test
    global music_id_calm
    global music_id_move
    global music_id_rand
    global music_id_test
    global cur_play_name
    global cur_play_path
    global music_stopped
    if (music_list == "calm"):
        music_list = "calm"
        cur_play_name = audios_calm[music_id_calm]
        cur_play_path = "calm/" + audios_calm[music_id_calm]
        if (not music_stopped):
            music_id_calm += 1
    if (music_list == "move"):
        music_list = "move"
        cur_play_name = audios_move[music_id_move]
        cur_play_path = "move/" + audios_move[music_id_move]
        if (not music_stopped):
            music_id_move += 1
    if (music_list == "rand"):
        music_list = "rand"
        cur_play_name = audios_rand[music_id_rand].split('/')[1]
        cur_play_path = audios_rand[music_id_rand]
        if (not music_stopped):
            music_id_rand += 1
    if (music_list == "test"):
        music_list = "test"
        cur_play_name = audios_test[music_id_test]
        cur_play_path = "test/" + audios_test[music_id_test]
        if (not music_stopped):
            music_id_test += 1
    if (music_id_calm >= len(audios_calm)):
        music_id_calm = 0
    if (music_id_move >= len(audios_move)):
        music_id_move = 0
    if (music_id_rand >= len(audios_rand)):
        music_id_rand = 0
    music_stopped = False

@client.event
async def on_ready():
    print("Bot is online.")

@client.command()
async def connect(ctx):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=voiceChannelName)
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is None or not voice.is_connected():
        await voiceChannel.connect()
        await ctx.send("Bot connected to a channel.")
    else:
        await ctx.send("The bot is already connected.")

@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is not None and voice.is_connected():
        await voice.disconnect()
        await ctx.send("Bot leaved the channel.")
    else:
        await ctx.send("The bot is not connected.")

@client.command()
async def play(ctx, url_:str = ""):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is None or not voice.is_connected():
        await ctx.send("The bot is not connected.")
    else:
        if (url_ is not None and len(url_) > 0 and (url_ == "calm" or url_ == "move" or url_ == "rand")):
            if not voice.is_playing():
                queue(url_)
                global cur_play_name
                global cur_play_path
                voice.play(discord.FFmpegPCMAudio(executable="D:/Programs/FFMPEG/bin/ffmpeg.exe", source="music/" + cur_play_path))
                await ctx.send("Now is playing: " + cur_play_name)
            else:
                await ctx.send("The bot is already playing.")
        else:
            await ctx.send("You must throw the parameter (calm, move, rand).")

@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is not None and voice.is_playing():
        voice.pause()
        await ctx.send("Music paused.")
    else:
        await ctx.send("Music is paused or turned off already.")

@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is not None and voice.is_paused():
        voice.resume()
        await ctx.send("Music resumed.")
    else:
        await ctx.send("Music is playing already or not turned on.")

@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()
    global music_stopped
    music_stopped = True
    await ctx.send("Music stopped.")

@client.command()
async def skip(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is None or not voice.is_connected():
        await ctx.send("The bot is not connected.")
    else:
        if not voice.is_playing():
            await ctx.send("The bot is not playing.")
        else:
            global music_list
            queue(music_list)
            global cur_play_name
            global cur_play_path
            voice.stop()
            voice.play(discord.FFmpegPCMAudio(executable="D:/Programs/FFMPEG/bin/ffmpeg.exe",
                                              source="music/" + cur_play_path))
            await ctx.send("Now is playing: " + cur_play_name)

@client.command()
async def playList(ctx, url_:str = ""):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is None or not voice.is_connected():
        await ctx.send("The bot is not connected.")
    else:
        if (url_ is not None and len(url_) > 0 and (url_ == "calm" or url_ == "move" or url_ == "rand" or url_ == "test")):
            if not voice.is_playing():
                global music_playList
                music_playList = True
                global music_list
                music_list = url_
                queue(music_list)
                global cur_play_name
                global cur_play_path
                # voice.stop()
                voice.play(discord.FFmpegPCMAudio(executable="D:/Programs/FFMPEG/bin/ffmpeg.exe",
                                                  source="music/" + cur_play_path),
                           after=lambda e: play_next(voice, ctx, music_list))
                await ctx.send("Now is playing: " + cur_play_name)
            else:
                await ctx.send("The bot is already playing.")
        else:
            await ctx.send("You must throw the parameter (calm, move, rand).")

def play_next(voice, ctx, music_list):
    queue(music_list)
    global cur_play_name
    global cur_play_path
    global loop
    try:
        # you must download ffmpeg and put it in folder like here
        # and write the path for ffmpeg.exe
        voice.play(discord.FFmpegPCMAudio(executable="D:/Programs/FFMPEG/bin/ffmpeg.exe", source="music/" + cur_play_path), after=lambda e: play_next(voice, ctx, music_list))
        asyncio.run_coroutine_threadsafe(ctx.send("Now is playing: " + cur_play_name), loop)
    except Exception:
        print(Exception)

@client.command()
async def playListStop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is not None and voice.is_connected():
        await voice.disconnect()
        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=voiceChannelName)
        if voice is None or not voice.is_connected():
            await voiceChannel.connect()
            await ctx.send("Playlist stopped")
            global music_playList
            music_playList = False
    else:
        await ctx.send("The bot is not connected.")

@client.command()
async def playListSkip(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is not None and voice.is_connected():
        await voice.disconnect()
        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=voiceChannelName)
        if voice is None or not voice.is_connected():
            await voiceChannel.connect()
            voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
            if not voice.is_playing():
                global music_list
                queue(music_list)
                global cur_play_name
                global cur_play_path
                # you must download ffmpeg and put it in folder like here
                # and write the path for ffmpeg.exe
                voice.play(discord.FFmpegPCMAudio(executable="D:/Programs/FFMPEG/bin/ffmpeg.exe",
                                                  source="music/" + cur_play_path),
                           after=lambda e: play_next(voice, ctx, music_list))
                await ctx.send("Now is playing: " + cur_play_name)
    else:
        await ctx.send("The bot is not connected.")

client.run(token)