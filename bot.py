import aiohttp, random, disnake, asyncio, datetime, openai, os
from disnake.ext import commands
from bs4 import BeautifulSoup
from keep_alive import keep_alive

client = commands.Bot(command_prefix="nil!", case_insensitive=True, intents=disnake.Intents.all())
client.remove_command('help')
client_token = os.environ['TOKEN']

@client.event
async def on_ready():
    await client.change_presence(activity=disnake.Activity(type=disnake.ActivityType.watching, name='People Speak With /'))

class Help:

    @client.slash_command(description="Displays a list of available commands and their descriptions.")
    async def help(self, ctx):
        embed = disnake.Embed(title="Help", description="Here are the available commands:", colour=disnake.Colour.green())
        embed.add_field(name="/song-search", value="Searches for a song and displays info about it.", inline=False)
        embed.add_field(name="/wiki-search", value="Searches for a topic on Wikipedia.", inline=False)
        embed.add_field(name="/dictionary", value="Browse the dictionary!", inline=False)
        embed.add_field(name="/urban-dict", value="Browse the Urban Dictionary!", inline=False)
        embed.add_field(name="/image-of", value="Displays an image of said object. OPEN-AI.", inline=False)
        embed.add_field(name="/chat", value="Chat with me!", inline=False)
        embed.add_field(name="/gpt3", value="Chat with gpt3. OPEN-AI.", inline=False)
        embed.add_field(name="/set-api-key", value="Set your api-key for open-ai commands!", inline=False)
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar.url)
        await ctx.response.send_message(embed=embed)

class Talk:

    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    @client.slash_command(name="chat", description="Ask me anything!", timeout=60.0)
    async def question(ctx: disnake.ApplicationCommandInteraction, message: str):
        await ctx.response.defer()
        async with aiohttp.ClientSession() as session:
            api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
            headers = {"Authorization": "Bearer lol"}
            payload = {"inputs": message}


            async with session.post(api_url, headers=headers, json=payload) as response:
                response_json = await response.json()
                embed = disnake.Embed(title="ChatBot Response", description=response_json['generated_text'],
                                          color=disnake.Color.green())
                embed.set_footer(text=f"{ctx.author.display_name}", icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

    @question.error
    async def question_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = disnake.Embed(colour=disnake.Colour.red(),
                                  description=f"You are going too fast! Please wait {round(error.retry_after, 2)} seconds before trying again.")
            embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        else:
            embed = disnake.Embed(colour=disnake.Colour.red(), description=f"Error: {error}")
            embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)


    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    @client.slash_command(name="wiki-search",description="Search Wikipedia!")
    async def wikipedia(ctx, *, topic: str):
        parameters = {
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "exintro": 1,
            "explaintext": 1,
            "titles": topic,
        }

        async with aiohttp.ClientSession() as session:
            async with session.get("https://en.wikipedia.org/w/api.php", params=parameters) as response:
                data = await response.json()

                pages = data["query"]["pages"]
                for page in pages.values():
                    content = page.get("extract")

                if content:
                    embed = disnake.Embed(
                        title=page.get("title"),
                        description=content[:2000],
                        color=disnake.Color.green(),
                    )
                    embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)

                    await ctx.send(embed=embed)
                else:
                    embed = disnake.Embed(colour=disnake.Colour.red(),description=f"No Such Topic {topic}..")
                    embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
                    await ctx.send(embed=embed)

    @wikipedia.error
    async def wikipedia_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = disnake.Embed(colour=disnake.Colour.red(),
                                  description=f"You are going too fast! Please wait {round(error.retry_after, 2)} seconds before trying again.")
            embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        else:
            embed = disnake.Embed(colour=disnake.Colour.red(), description=f"Error: {error}")
            embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    @client.slash_command(name="song-search", description="Get details about a song")
    async def song(ctx, name: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.deezer.com/search?q={name}") as response:
                data = await response.json()

                if data.get("error"):
                    embed = disnake.Embed(colour=disnake.Colour.red(), description="Error: Song not found")
                else:
                    track = data["data"][0]
                    artist = track["artist"]["name"]
                    title = track["title"]
                    album = track["album"]["title"]
                    release_date = track.get("release_date", "Unknown")
                    duration = datetime.timedelta(seconds=track["duration"])
                    image = track["album"]["cover_big"]
                    embed = disnake.Embed(title=f"{artist} - {title}",
                                          description=f"Album: {album}\nRelease Date: {release_date}\nDuration: {duration}",
                                          color=disnake.Colour.green())
                    embed.set_thumbnail(url=image)

                embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

    @song.error
    async def song_error(ctx, error):
        embed = disnake.Embed(colour=disnake.Colour.red(), description=f"Error: {error}")
        embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @client.slash_command(name="set-api-key",description="Set your api-key to use OpenAI commands!")
    async def set_key(ctx,api_key:str):
        with open("user_lock/{}".format(ctx.author.name), "w+") as key:
            key.write(api_key)
            user = await client.fetch_user(ctx.author.id)
            await user.send("Thank you for setting your API-KEY!, you make re-use this command to change your api-key otherwise you are free to use openai commands!")

    @client.slash_command(name="image-of", description="Generate an image of a celebrity! OPEN-AI")
    async def celebrity(ctx: disnake.ApplicationCommandInteraction, *, name: str):
        await ctx.response.defer()
        with open(f"user_lock/{ctx.author.name}", "r+") as key:
            openai.api_key = key.read()

        response = openai.Image.create(
            prompt=f"Generate an image of {name}",
            n=1,
            size="256x256",
            response_format="url"
        )

        embed = disnake.Embed(title=f"Image of {name}", color=disnake.Colour.green())
        embed.set_image(url=response["data"][0]["url"])
        embed.set_footer(text=f"{ctx.author.display_name}", icon_url=ctx.author.avatar.url)

        await ctx.send(embed=embed)

    @celebrity.error
    async def celebrity_error(ctx, error):
        embed = disnake.Embed(colour=disnake.Colour.red(), description=f"Error: {error}")
        embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)


    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    @client.slash_command(name="urban-dict", description="Get the definition of a word from Urban Dictionary")
    async def urban(ctx, word: str):
        async with aiohttp.ClientSession() as session:
            url = f"https://api.urbandictionary.com/v0/define?term={word}"
            async with session.get(url) as response:
                data = await response.json()

            if not data["list"]:
                await ctx.send(f"Sorry, I couldn't find a definition for '{word}' on Urban Dictionary.")
                return

            definition = data["list"][0]["definition"]
            example = data["list"][0]["example"]

            embed = disnake.Embed(title=f"Urban Definitions for '{word}'", colour=disnake.Colour.green())
            embed.add_field(name="Definition", value=definition, inline=False)
            embed.add_field(name="Example", value=example, inline=False)
            embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)

            await ctx.send(embed=embed)

    @urban.error
    async def urban_error(ctx, error):
        embed = disnake.Embed(colour=disnake.Colour.red(), description=f"Error: {error}")
        embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    @client.slash_command(name="dictionary", description="Browse the dictionary!")
    async def dict(ctx, word: str):
        async with aiohttp.ClientSession() as s:
            async with s.get("https://www.dictionary.com/browse/{}".format(word)) as r:
                response = await r.text()

                soup = BeautifulSoup(response, "html.parser")
                definition = soup.find("div", {"value": "1"}).text

                embed = disnake.Embed(title="Results For {}".format(word), description=definition,
                                      colour=disnake.Colour.green())
                embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

    @dict.error
    async def dict_error(ctx, error):
        embed = disnake.Embed(colour=disnake.Colour.red(), description=f"Error: {error}")
        embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    @client.slash_command(name="gpt3", description="Talk to chatgpt3, OPENAI",timeout=60)
    async def chat(ctx, message):
        await ctx.response.defer()
        with open(f"user_lock/{ctx.author.name}", "r+") as key:
            openai.api_key = key.read()

        response = openai.Completion.create(model="text-davinci-003", prompt=message, temperature=0, max_tokens=200)
        response_text = response.choices[0].text

        embed = disnake.Embed(colour=disnake.Colour.green(), title="Response From Gpt!",
                              description=response_text[:2000])
        embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)

        await ctx.send(embed=embed)

    @chat.error
    async def gpt3_api_error(ctx, error):
        embed = disnake.Embed(colour=disnake.Colour.red(), description=f"Error: {error}")
        embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)


keep_alive()
client.run(client_token)
