Adelaide is my personal experiment with lukalabs' Cakechat program.  I've added discord.py support, sentiment analysis with the TextBlob library, and there is more to come.


SETUP:
Clone the repository and run "pip install -r requirements.txt".  You will need Python 3.6.8 for the program to run well.  
Then, open "tools/discord_bot.py" and change the client ID and discord API token to your client ID and token.  
If you do not have a discord bot, you can get one here: https://discordapp.com/developers/applications/

Currently it uses lukalabs' pretrained model until I can get hardware sufficient to train it myself.  
Run "python tools/download_model.py" to download the pre-trained model.

