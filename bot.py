import discord
from discord.ext import commands
import random 

BOT_PREFIX = ["sam ", "sam", "Sam ", "Sam"]
INTENTS = discord.Intents.default()
TOKEN = ""
client = commands.Bot(command_prefix=BOT_PREFIX,
                      decription="Sam is a discord bot meant to make things easier and play some games.", intents=INTENTS, allowed_mentions = discord.AllowedMentions(users = True, everyone = True, replied_user=True, roles = True))

client.remove_command('help')

extentions = ["Extentions.game", "Extentions.admin", "Extentions.fun"]

if __name__ == "__main__": 
  for ext in extentions:
    client.load_extension(ext)

@client.event
async def on_ready():
    print("Connected to the bot")
    await client.change_presence(activity=discord.Game(name="TESTING/DEVELOPING, DO NOT USE."))
#    while True:
#        statusNum = random.randint(1, 4)
#        if statusNum == 1:
#            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name= ' Lots of Anime'))
#        elif statusNum == 2:
#            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name = " sam help"))
#        elif statusNum == 3:
#            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name = " Terraria with friends"))
#        elif statusNum == 4:
#            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name = " Rick and Morty"))
#        await asyncio.sleep(50)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("Command Not Found, Please try a different command")

@client.command(aliases = ["Help"])
async def help(ctx, *, helpgroup = ""):
    embed = discord.Embed(
        title = "Help",
        color = discord.Color.blurple()
    )
    if helpgroup == "admin":
        embed.add_field(name="purge", value="Resets the chat")
        embed.add_field(name="vote", value="Asks for people to vote for whatever you say.")
        embed.add_field(name = "giveaway", value = "Starts a giveaway!")
        embed.add_field(name="ban", value="Bans someone")
        embed.add_field(name="unban", value="Unbans someone")
        embed.add_field(name="kick", value="Kicks someone")
        embed.set_thumbnail(url="https://pic.onlinewebfonts.com/svg/img_261633.png")
        await ctx.send(embed=embed)
    if helpgroup == "game":
        embed.add_field(name="job", value="Lets you pick a job or work for money!")
        embed.add_field(name="rob", value="Rob one of your friends of their money")
        embed.add_field(name="bal", value="Checks how much money you have")
        embed.add_field(name="weaponShop", value="Buy A Weapon")
        embed.set_thumbnail(url="https://pic.onlinewebfonts.com/svg/img_261633.png")
        await ctx.send(embed=embed)
    if helpgroup == "":
        embed.add_field(name="spam", value="Spam Something Fun")
        embed.add_field(name="kill", value="Kill your friends, requires you at @ someone")
        embed.add_field(name="insult", value="Insult your friends, needs you to @ someone")
        embed.add_field(name="compliment", value="Compliment your friends, needs you to @ someone")
        embed.add_field(name="rolldice", value="Rolls a die, you need to specify the ammount of sides")
        embed.add_field(name="coinflip", value="Flips a coin!")
        embed.add_field(name="mental", value="Tells everyone your mental state!")
        embed.add_field(name="8ball", value="A (maybe insulting) 8Ball!")
        embed.add_field(name="help", value="Sends the command list!")
        embed.add_field(name="makeSave", value="Creates a save for the game!")
        embed.add_field(name='After the Help Command', value='Add "admin" to view admin commands or "game" for game commands')
        embed.set_thumbnail(url="https://pic.onlinewebfonts.com/svg/img_261633.png")
        await ctx.send(embed=embed)




client.run(TOKEN)
