#Discord Bot for Cakechat
#By Victor Yuska

import discord
import asyncio
import requests
import random
import time
import os
import sys

from textblob import TextBlob

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
from collections import deque


from cakechat.utils.env import init_theano_env

init_theano_env()

from cakechat.api.response import get_response
from cakechat.config import INPUT_CONTEXT_SIZE, DEFAULT_CONDITION

client = discord.Client()

_context = deque(maxlen=INPUT_CONTEXT_SIZE)

from cakechat.api.v1.server import app

def getAllUsersCount():
    guilds = client.guilds
    user_count = 0
    for g in guilds:
         user_count += len(g.members)
    return("Current user count: " + str(user_count))

@client.event
async def on_ready():
    mood = 0.0
    print('Logged in as '+client.user.name+' (ID:'+str(client.user.id)+') | '+str(len(client.guilds))+' servers | ' + getAllUsersCount())
    await client.change_presence(activity=discord.Game(name='chat with me!'))

#Determine the intent of a sentence and the emotion to respond with (TODO: This should be more dynamic! Rework coming eventually)
async def sentiment_analysis(input): 
    txtblob = TextBlob(input)
    sent = txtblob.sentiment
    #The below values should be fine-tuned or replaced completely with a more dynamic system
    if(sent.subjectivity < 0.27):
        COND = "neutral"
    elif(sent.polarity < -0.88):
       COND = "fear"
    elif(sent.polarity > 0.4):
        COND = "joy"
    elif(sent.polarity < -0.67):
        COND = "anger"
    elif(sent.polarity < -0.39):
        COND = "sadness"
    else:
        COND = DEFAULT_CONDITION
    await client.change_presence(activity=discord.Game(name='feeling ' + COND)) #Display the bot's emotion as a status
    return COND #Return the condition to respond with!


#Called when a message is received
@client.event
async def on_message(message):
    if not (message.author == client.user): #Check to ensure the bot does not respond to its own messages
        if(client.user.mentioned_in(message) or isinstance(message.channel, discord.abc.PrivateChannel)): #Check if the bot is mentioned or if the message is in DMs
            async with message.channel.typing(): #Show that the bot is typing
                txtinput = message.content.replace("<@" + str(client.user.id) + ">", "")  #Filter out the mention so the bot does not get confused
                if(len(txtinput) > 220): #Spam protection
                    txt = "I am sorry, that is too long for me."
                else:
                    _context.append(txtinput)
                    COND = await sentiment_analysis(txtinput) #Determine how to respond to the sentence emotionally
                    txt = get_response(_context, COND) #Get a response!
                await message.channel.send(txt) #Fire away!

print('Starting...')
client.run('TOKEN_GOES_HERE') #Replace TOKEN_GOES_HERE with your bot's API token
