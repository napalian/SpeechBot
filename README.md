# SpeechBot
Source code for SpeechBot. Cancelled bot..

This is a Python script for a Discord bot that uses the Disnake library, which is a fork of the popular Discord.py library. The bot can perform various tasks such as searching for songs, searching on Wikipedia, browsing dictionaries, and chatting with users using GPT-3.

The script starts by importing the necessary libraries such as aiohttp for making HTTP requests, Disnake for creating the bot, asyncio for asynchronous programming, datetime for working with dates and times, openai for accessing the GPT-3 API, and os for accessing environment variables.

The client object is then created using the commands.Bot class from Disnake, with the command prefix set to "nil!" and case_insensitive set to True. The client object is then configured to remove the default help command using the remove_command() method.

The bot's token is obtained from an environment variable and stored in the client_token variable.

The script defines two classes, Help and Talk, each containing methods for the bot's various commands.

The Help class contains a single method that responds to the /help command. It creates an Embed object using Disnake and adds fields for each available command, along with their descriptions. The Embed object is then sent as a message using the send_message() method.

The Talk class contains two methods that handle the /chat and /wiki-search commands, respectively. Both methods have a cooldown decorator that limits how often a user can use the command. The /chat command uses the GPT-3 API to generate a response to a user's question, while the /wiki-search command searches for a topic on Wikipedia and returns a summary.

Both methods first use Disnake's ApplicationCommandInteraction object to handle the user's request. The /chat command uses the aiohttp library to make a POST request to the GPT-3 API with the user's question, and then generates an Embed object with the response. The /wiki-search command also uses the aiohttp library to make a GET request to the Wikipedia API, and then generates an Embed object with the summary of the topic.

If there is an error in handling the request, such as a CommandOnCooldown error due to the user exceeding the command's cooldown time, an error message is generated and sent as an Embed object.

The script ends with the client object running using the run() method, with the token passed as an argument. A keep_alive() function is also imported from a separate module to ensure the bot remains online.
