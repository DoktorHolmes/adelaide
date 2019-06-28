import random
import time
import os
import sys
import pyttsx3
import speech_recognition as sr

from textblob import TextBlob

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

import argparse
from collections import deque


from cakechat.utils.env import init_theano_env

init_theano_env()

from cakechat.api.response import get_response
from cakechat.config import INPUT_CONTEXT_SIZE, DEFAULT_CONDITION

_context = deque(maxlen=INPUT_CONTEXT_SIZE)

from cakechat.api.v1.server import app




class EmotionState: #Class to store emotional dats
    def __init__(self):
        self.thought_polarity = 0.0 #Positivity/Negativity
        self.thought_subjectivity = 0.0 #Subjectivity/Objectivity
        self.emotions_dividend = 2.3 #Controls intensity of the sentiment detection; lower is more intense, higher is less

    def new_sentiment_analysis(self, input):
        txtblob = TextBlob(input)
        sent = txtblob.sentiment
        COND = DEFAULT_CONDITION
        #TO-DO: More fine tuning
        if(sent.subjectivity < 0.27):
            self.thought_subjectivity -= sent.subjectivity / 3
        else:
            self.thought_subjectivity += sent.subjectivity / 3
        if(self.thought_subjectivity < 0.0):
            self.thought_subjectivity = 0.0
        if(self.thought_subjectivity > 1.0):
            self.thought_subjectivity = 1.0
        self.thought_polarity += sent.polarity / self.emotions_dividend #Adjust polarity based on sentiment detection results
        if(self.thought_polarity < -1.0):
            self.thought_polarity = -1.0
        if(self.thought_polarity > 1.0):
            self.thought_polarity = 1.0
        if(self.thought_subjectivity >= 0.0 and self.thought_subjectivity <= 0.3 and self.thought_polarity > -0.7 and self.thought_polarity < 0.3): #If feeling neutral and indifferent, then change condition to neutral
            COND = "neutral"
        if(self.thought_subjectivity >= 0.3 and self.thought_polarity >= 0.45):
            COND = "joy"
        if(self.thought_subjectivity >= 0.4 and self.thought_polarity <= -0.1):
            COND = "sadness"
        if(self.thought_subjectivity >= 0.55 and self.thought_polarity <= -0.45):
            COND = "anger"
        if(self.thought_subjectivity >= 0.15 and self.thought_polarity <= -0.75):
            COND = "fear"
        return COND #Return the condition to respond with!



#Determine the intent of a sentence and the emotion to respond with (TODO: This should be more dynamic! Rework coming eventually)
def sentiment_analysis(input): 
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
    #await client.change_presence(activity=discord.Game(name='feeling ' + COND)) #Display the bot's emotion as a status
    return COND #Return the condition to respond with!


#Called when a message is received
def respond(txtinput):
	if(len(txtinput) > 220): #Spam protection
		txt = "I am sorry, that is too long for me."
	else:
		_context.append(txtinput)
		COND = es.new_sentiment_analysis(txtinput) #Determine how to respond to the sentence emotionally
		txt = get_response(_context, COND) #Get a response!
	print(txt)
	engine.say(txt)
	engine.runAndWait()
	

print('Starting...')


r = sr.Recognizer()


while(True):
	with sr.Microphone() as source:
		print("Listening!")
		audio = r.listen(source)
	try:
		txt = r.recognize_google(audio)
		print("Recognized: " + txt)
		respond(txtinput)
	except sr.UnknownValueError:
		print("Google Speech Recognition could not understand audio")
	except sr.RequestError as e:
		print("Could not request results from Google Speech Recognition service; {0}".format(e))
	