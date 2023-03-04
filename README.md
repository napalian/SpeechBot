#Source Code for SpeechBot
This is a Python script for a Discord bot that uses the Disnake library, which is a fork of the popular Discord.py library. The bot can perform various tasks such as searching for songs, searching on Wikipedia, browsing dictionaries, and chatting with users using GPT-3.

The script starts by importing the necessary libraries:

python
Copy code
import aiohttp
from disnake.ext import commands
import asyncio
import datetime
import openai
import os
The aiohttp library is used for making HTTP requests, Disnake for creating the bot, asyncio for asynchronous programming, datetime for working with dates and times, openai for accessing the GPT-3 API, and os for accessing environment variables.

The client object is then created using the commands.Bot class from Disnake, with the command prefix set to "nil!" and case_insensitive set to True. The client object is then configured to remove the default help command using the remove_command() method.

##python##
#client = commands.Bot(command_prefix='nil!', case_insensitive=True)
#client.remove_command('help')

The bot's token is obtained from an environment variable and stored in the client_token variable.

python

client_token = os.environ['BOT_TOKEN']
The script defines two classes, Help and Talk, each containing methods for the bot's various commands.

The Help class contains a single method that responds to the /help command. It creates an Embed object using Disnake and adds fields for each available command, along with their descriptions. The Embed object is then sent as a message using the send_message() method.

python

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='help')
    async def help_command(self, ctx):
        help_embed = disnake.Embed(
            title='SpeechBot Help',
            description='Here are the available commands and their descriptions:'
        )
        help_embed.add_field(name='/help', value='Shows this help message', inline=False)
        help_embed.add_field(name='/chat [question]', value='Talk with the bot', inline=False)
        help_embed.add_field(name='/wiki-search [topic]', value='Search for a topic on Wikipedia', inline=False)
        await ctx.send(embed=help_embed)
The Talk class contains two methods that handle the /chat and /wiki-search commands, respectively. Both methods have a cooldown decorator that limits how often a user can use the command.

python

class Talk(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name='chat')
    async def chat_command(self, ctx, *, question: str):
        try:
            response = openai.Completion.create(
                engine="davinci",
                prompt=f"{question}",
                max_tokens=50
            )
            answer = response.choices[0].text.strip()
            chat_embed = disnake.Embed(
                title='SpeechBot Chat',
                description=f'**User**: {question}\n**Bot**: {answer}'
            )
            await ctx.send(embed=chat_embed)
        except:
            error_embed = disnake.Embed(
                title='Error',
                description='An error occurred while handling your request'
            )
            await ctx.send(embed=error_embed)
