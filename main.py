import nextcord
from nextcord.ext import commands

import os

import wikipedia
import wolframalpha

getInfo = wolframalpha.Client("W7TRW6-3UT86Y4PUP")

from config import *
from carter import *

intents = nextcord.Intents.all()
activity = nextcord.Activity(type=nextcord.ActivityType.watching, name="Discord Servers")
client = commands.Bot(command_prefix=Prefix, intents=intents)


# On startup
@client.event
async def on_ready():
  print("""
   _____                _      _   _   
  / ____|              | |    | | | |  
 | (___   ___ __ _ _ __| | ___| |_| |_ 
  \___ \ / __/ _` | '__| |/ _ \ __| __|
  ____) | (_| (_| | |  | |  __/ |_| |_ 
 |_____/ \___\__,_|_|  |_|\___|\__|\__|
                                      
  -By 2Devs
        """)


# Handles Ban command - Member need Ban permission on there role
@client.command()
async def ban(ctx, member: nextcord.Member, *, reason=None):
  await member.ban(reason=reason)
  await ctx.send(f'{member} has been banned.')


# Handles Kick command - Member need Kick members permission on there role
@client.command()
async def kick(ctx, member: nextcord.Member, *, reason=None):
  await member.kick(reason=reason)
  await ctx.send(f'{member} has been kicked.')


# Handles mute command - Member need manage roles permission on there role
@client.command()
async def mute(ctx, member: nextcord.Member):
  role = nextcord.utils.get(ctx.guild.roles, name="Muted")
  await member.add_roles(role)
  await ctx.send(f'{member} has been muted.')


# Handles unmute command - Member need manage roles permission on there role
@client.command()
async def unmute(ctx, member: nextcord.Member):
  role = nextcord.utils.get(ctx.guild.roles, name="Muted")
  await member.remove_roles(role)
  await ctx.send(f'{member} has been unmuted.')


# handle on_message event
@client.event
async def on_message(message: nextcord.Message):
  if message.author == client.user:
    return

  sentence = message.content.lower()
  User = str(message.author)
  WakeWord = UIName[1:]

  if Prefix in sentence:
    sentence = sentence.replace(Prefix, "")

    # Handles Ban command - Member need Ban permission on there role
    if Prefix + "embed" in message.content:
      if message.author.guild_permissions.ban_members:
        embedText = message.content.replace("embed", "")
        embedText = embedText.replace(Prefix, "")
        embed = nextcord.Embed(title="", description=embedText, color=0xe91e63)
        await message.channel.purge(limit=1)
        await message.channel.send(embed=embed)

    if Prefix + "info" in message.content:
      try:
        text = message.content.replace("info", "")
        text = text.replace(Prefix, "")
        info = wikipedia.summary(text, sentences=4)
        await message.channel.send(info)
      except:
        await message.channel.send(
          "Sorry, I couldn't find a solid answer to your request.")

    if Prefix + "get" in message.content:
      try:
        text = message.content.replace("get", "")
        text = text.replace(Prefix, "")
        info = getInfo.query(text)
        res = next(info.results).text
        await message.channel.send(res)
      except:
        await message.channel.send(
          "Sorry, I couldn't find a solid answer to your request.")

    if Prefix + "help" in message.content:
      embed = nextcord.Embed(title="Scarlett Help Menu",
                             description=f"**Prefix: {Prefix}**",
                             color=0xe91e63)
      embed.add_field(name="",
                      value=Prefix + "clear <number of messages>",
                      inline=False)
      embed.add_field(name="",
                      value=Prefix + "ban <user> <reason>",
                      inline=True)
      embed.add_field(name="", value=Prefix + "unban <user>", inline=False)
      embed.add_field(name="",
                      value=Prefix + "kick <user> <reason>",
                      inline=False)
      embed.add_field(name="",
                      value=Prefix + "mute <user> <duration> <reason>",
                      inline=True)
      embed.add_field(name="", value=Prefix + "unmute <user>", inline=False)
      embed.add_field(name="",
                      value=Prefix + "embed <**title**> <text>",
                      inline=False)
      embed.add_field(name="", value=Prefix + "info <keyword>", inline=False)
      embed.add_field(name="",
                      value=Prefix + "get <info you want to get>",
                      inline=False)
      embed.add_field(name="",
                      value=f"**Running Scarlett Version: {Version}**",
                      inline=False)
      #await message.channel.purge(limit=1)
      await message.channel.send(embed=embed)

    if Prefix + "deactivate-Key=1123" in message.content:
      if message.author.guild_permissions.ban_members:
        await message.channel.purge(limit=1)
        await message.channel.send("Deactivated: Exit Code 0")
        exit()

    if "ban" in sentence:
      if message.author.guild_permissions.ban_members:
        try:
          member = message.mentions[0]
          await member.ban()
          await message.channel.send(f'{member} has been banned.')
        except:
          await message.channel.send('Error Occured, please try again')

    # Handles Kick command - Member need Kick members permission on there role
    elif "kick" in sentence:
      if message.author.guild_permissions.kick_members:
        try:
          member = message.mentions[0]
          await member.kick()
          await message.channel.send(f'{member} has been kicked.')
        except:
          await message.channel.send('Error Occured, please try again')

    # Handles mute command - Member need manage roles permission on there role
    elif "mute" in sentence:
      if message.author.guild_permissions.manage_roles:
        try:
          member = message.mentions[0]
          role = nextcord.utils.get(message.guild.roles, name="Muted")
          await member.add_roles(role)
          await message.channel.send(f'{member} has been muted.')
        except:
          await message.channel.send('Error Occured, please try again')

    # Handles unmute command - Member need manage roles permission on there role
    elif "unmute" in sentence:
      if message.author.guild_permissions.manage_roles:
        try:
          member = message.mentions[0]
          role = nextcord.utils.get(message.guild.roles, name="Muted")
          await member.remove_roles(role)
          await message.channel.send(f'{member} has been unmuted.')
        except:
          await message.channel.send('Error Occured, please try again')

    # Handles clear command - Member need manage messages permission on there role
    elif "clear" in sentence:
      if message.author.guild_permissions.manage_messages:
        amount = sentence.replace("clear ", "")
        messageamount = int(amount)
        channel = message.channel
        messages = []
        await channel.purge(limit=messageamount)
        ResponseOutput = (
          f"{messageamount} messages deleted. I was authorised to do so by {User} in channel {channel}"
        )
        await channel.send(ResponseOutput)

  # CarterAPI if commands is not found
  # Use this code if you want to add some form of chatbot interface.
  elif WakeWord in sentence:
    await message.channel.trigger_typing()
    SendToCarter(sentence, User, APIkey)
    with open('ResponseOutput.txt') as f:
      ResponseOutput = f.read()

    print(User + ": " + message.content)
    await message.channel.send(f"{ResponseOutput}")
    print(ResponseOutput)
    os.remove("ResponseOutput.txt")

  else:
    pass


# run bot
client.run(DiscordAPI)
