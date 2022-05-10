from ast import Await, ExceptHandler
import random
import discord
import time
import pickle
import os
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands, tasks
import aiohttp

BOT_PREFIX = ["sam ", "sam"]
INTENTS = discord.Intents.default()
TOKEN = ""
client = commands.Bot(command_prefix=BOT_PREFIX,
                      decription="Sam is a discord bot meant to make things easier and play some games.", intents=INTENTS, allowed_mentions = discord.AllowedMentions(users = True, everyone = True, replied_user=True, roles = True))

client.remove_command('help')

def convert(time):
  pos = ["s","m","h","d"]

  time_dict = {"s" : 1, "m" : 60, "h" : 3600, "d": 3600*24}

  unit = time[-1]

  if unit not in pos:
    return -1
  try:
    val = int(time[:-1])
  except:
    return -2

  return val * time_dict[unit]


def loadPickle(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def savePickle(filename, data):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

@client.event
async def on_ready():
    print("Connected to the bot")
    while True:
        statusNum = random.randint(1, 4)
        if statusNum == 1:
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name= ' Demon Slayer'))
        elif statusNum == 2:
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name = " sam help"))
        elif statusNum == 3:
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name = " Terraria with friends"))
        elif statusNum == 4:
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name = " The Rising of the Shield Hero"))
        await asyncio.sleep(50)


@client.command(aliases=["dice", "roll", "diceroll"])
async def rolldice(ctx, arg = int(0)):
    if arg == 0:
        await ctx.send("You need to specify how many sides.")
    else:
        await ctx.send(f"You rolled a D{arg}")
        numrolled = random.randint(1, arg)
        await ctx.send(f"You rolled a {numrolled}!")

@client.command(aliases=["flipcoin", "coin"])
async def coinflip(ctx):
    sides = ["Heads", "Tails"]
    flipside = random.choice(sides)
    await ctx.send(f"The coin flipped and landed {flipside}")

@client.command(aliases=["ded", "dead", "d"])
async def death(ctx):
    heavenorhell = ["heaven", "hell", "hell", "hell", "the void"]
    await ctx.send(ctx.message.author.mention + f" You are going to go to {random.choice(heavenorhell)} when you die")

@client.command(aliases=["clear", "pur", "purge"], name="Purge")
@commands.has_permissions(manage_messages=True)
async def purge(ctx):
    await ctx.channel.purge()
    await ctx.send("The Channel Was Purged")
    time.sleep(3)
    await ctx.channel.purge(limit=1)

@client.command()
async def kill(ctx, arg):
    weapon=("Knife", "Gun", "Sword")
    await ctx.send(ctx.message.author.mention + f" Killed {arg} with a {random.choice(weapon)}")

@client.command()
async def stab(ctx, arg):
    await ctx.send(f"{ctx.message.author.mention} Just stabbed {arg}")
     
@client.command()
async def insult(ctx, arg):
    insults = ("Screw you", "You are a jerk", "You suck", "OH NO ITS", "Ugh, its", "EVERYBODY GET OUT, ITS", "Deal with it")
    await ctx.send(f"{random.choice(insults)} {arg}")
    
@client.command()
async def compliment(ctx, arg):
    compliments = ("Is Looking nice today", "Is Awesome", "Is a good person", "Is nice", "Is A cool person", "Isn't an idiot", "Needs to talk more")
    await ctx.send(f"{arg} {random.choice(compliments)}")
     
@client.command()
async def mental(ctx):
    answers = ("Is Mentally Insane", "Is Mentally Stable", "Is Going Insane", "Needs therapy", "Needs a huge suppository", "Is an idiot", "Has Crippling Depression")
    await ctx.send(f"{ctx.author.mention} {random.choice(answers)}")
    
@client.command()
async def spam(ctx, *, arg):
    spam = 0
    while spam != 20:
        await ctx.send(arg)
        spam += 1

@client.command(aliases=["save", "StartSave", "startsave", "startSave", "Startsave"])
async def createGameSave(ctx):
    playerData = {}
    inventoryData = {}
    if os.path.isfile(f"{ctx.author.id}-player.dat") == False or os.path.isfile(f"{ctx.author.id}-inventory.dat") == False:
        savePickle(f"{ctx.author.id}-player.dat", playerData)
        savePickle(f"{ctx.author.id}-inventory.dat", inventoryData)

        await ctx.send("Save Data Created")
    else:
        await ctx.send("You Already Have Save Data")

@client.command(name="8ball",
                decription="Chooses stuff For You, maybe a little insulting",
                aliases=["Eight Ball", "8-ball", "eight ball", "8-Ball"],
                pass_context=True)
async def eight_ball(ctx):
    possible_responses = [
            'Thats gonna have to be a no',
            'It Is not looking likely',
            'For Sure you jerk',
            'Fuck you im not answering that',
            'Might be Likely you idiot',
            'I dont care you piece of shit',
            'Ok The answer is FRICK yes.', ]
    await ctx.send(random.choice(possible_responses) + ", " + ctx.message.author.mention)

@client.command(pass_context=True)
async def meme(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/memes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)

@client.command(aliases = ["Help"])
async def help(ctx, *, arg = ""):
    embed = discord.Embed(
        title = "Help",
        color = discord.Color.blurple()
    )
    if arg == "admin":
        embed.add_field(name="purge", value="Resets the chat")
        embed.add_field(name="vote", value="Asks for people to vote for whatever you say.")
        embed.add_field(name = "giveaway", value = "Starts a giveaway!")
        embed.add_field(name="ban", value="Bans someone")
        embed.add_field(name="unban", value="Unbans someone")
        embed.add_field(name="kick", value="Kicks someone")
        await ctx.send(embed=embed)
    else:
        embed.add_field(name = "meme", value = "Sends a meme off of the r/memes subreddit")
        embed.add_field(name="spam", value="Spam Something Fun")
        embed.add_field(name="kill", value="Kill your friends, requires you at @ someone")
        embed.add_field(name="insult", value="Insult your friends, needs you to @ someone")
        embed.add_field(name="compliment", value="Compliment your friends, needs you to @ someone")
        embed.add_field(name="rolldice", value="Rolls a die, you need to specify the ammount of sides")
        embed.add_field(name="coinflip", value="Flips a coin!")
        embed.add_field(name="mental", value="Tells everyone your mental state!")
        embed.add_field(name="8ball", value="A (maybe insulting) 8Ball!")
        embed.add_field(name="death", value="Tells you where you are going when you die!")
        embed.add_field(name="help", value="Sends the command list!")
        embed.add_field(name="reddit", value="Searches a Sub you specify for an image! May not send image if it picks a non-media post.")
        embed.add_field(name='After the Help Command', value='Add "admin" to view admin commands')
        embed.set_thumbnail(url="https://pic.onlinewebfonts.com/svg/img_261633.png")
        await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(administrator=True)
async def vote(ctx, *, arg):
    await ctx.channel.purge(limit=1)
    message = await ctx.send(f"@everyone Vote for: {arg}")
    await message.add_reaction('\U0001F44D')
    await message.add_reaction('\U0001F44E')
    

@client.command()
@commands.has_permissions(administrator=True)
async def giveaway(ctx):
  await ctx.send("Let's start with this giveaway! Answer these questions within 15 seconds!")

  questions = ["Which channel should it be hosted in?", "What should be the duration of the giveaway? (s|m|h|d)", "What is the prize of the giveaway?"]

  answers = []

  def check(message):
    return message.author == ctx.author and message.channel == ctx.channel

  for i in questions:
    await ctx.send(i)

    try:
      msg = await client.wait_for('message', timeout=15.0, check=check)
    except asyncio.TimeoutError:
      await ctx.send('You didn\'t answer in time, please be quicker next time!')
      return
    else: 
      answers.append(msg.content)

  try:
    c_id = int(answers[0][2:-1])
  except:
    await ctx.send(f"You didn't mention a channel properly. Do it like this {ctx.channel.mention} next time.")
    return

  channel = client.get_channel(c_id)

  time = convert(answers[1])
  if time == -1:
    await ctx.send(f"You didn't answer with a proper unit. Use (s|m|h|d) next time!")
    return
  elif time == -2:
    await ctx.send(f"The time just be an integer. Please enter an integer next time.")
    return
  
  prize = answers[2]

  await ctx.send(f"The giveaway will be in {channel.mention} and will last {answers[1]} seconds!")

  embed = discord.Embed(title = "Giveaway!", description = f"{prize}", color = ctx.author.color)

  embed.add_field(name = "Hosted by:", value = ctx.author.mention)

  embed.set_footer(text = f"Ends {answers[1]} from now!")

  my_msg = await channel.send(embed = embed)

  await my_msg.add_reaction("🎉")

  await asyncio.sleep(time)

  new_msg = await channel.fetch_message(my_msg.id)

  users = await new_msg.reactions[0].users().flatten()
  users.pop(users.index(client.user))

  winner = random.choice(users)

  await channel.send(f"Congrats! {winner.mention} won: {prize}!")


@client.command()
@commands.has_permissions(administrator=True)
async def reroll(ctx, channel : discord.TextChannel, id_ : int):
  try:
    new_msg = await channel.fetch_message(id_)
  except:
    await ctx.send("The ID that was entered was incorrect, make sure you have entered the correct giveaway message ID.")
  users = await new_msg.reactions[0].users().flatten()
  users.pop(users.index(client.user))

  winner = random.choice(users)

  await channel.send(f"Congrats the new winner is: {winner.mention} for the giveaway")
    
@client.command()
async def reddit(ctx, *, arg):
    embed = discord.Embed(title="", description="")
    sub = arg.replace(" ", "")
    sub = sub.lower()
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f'https://www.reddit.com/r/{sub}/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 20)]['data']['url'])
            await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(administrator = True)
async def ban(ctx, member : discord.Member, reason=None):
    """Bans a user"""
    if reason == None:
        await ctx.send(f"Woah {ctx.author.mention}, Make sure you provide a reason!")
    else:
        messageok = f"You have been banned from {ctx.guild.name} for {reason}"
        await member.send(messageok)
        await member.ban(reason=reason)

@client.command()
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):

    await member.kick(reason=reason)

    await ctx.send(f'User {member} has been kicked.')

@client.command(aliases=["newSave"])
async def makeSave(ctx):
    gamedata = {"money": 0, "pet": "none", "weapon": "none", "battlepasses": 0, "kills": 0, "job": "none"}
    if os.path.isfile(f"{ctx.author.id}-save.dat") == False:
        savePickle(f"{ctx.author.id}-save.dat", gamedata)
        await ctx.send("Save Created")
    else: 
        await ctx.send("You already have a save")

@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def job(ctx):
    gamedata = loadPickle(f"{ctx.author.id}-save.dat")
    if gamedata["job"] == "none":
        embed = discord.Embed(title= "Job Huntin'")
        jobchoices = ["Streamer", "Programmer", "Police", "Sports Player", "Artist", "Factory Worker", "Engineer", "Game Developer"]
        job1 = random.choice(jobchoices)
        jobchoices.remove(job1)
        job2 = random.choice(jobchoices)
        jobchoices.remove(job2)
        job3 = random.choice(jobchoices)
        embed.add_field(name="choice 1️⃣ is:", value=f"{job1}")
        embed.add_field(name="choice 2️⃣ is:", value=f"{job2}")
        embed.add_field(name="choice 3️⃣ is:", value=f"{job3}")
        embed.add_field(name ="Choosing", value="react with cooresponding emoji to choose job")

        msg = await ctx.send(embed=embed)
        await msg.add_reaction("1️⃣")
        await msg.add_reaction("2️⃣")
        await msg.add_reaction("3️⃣")

        check = lambda r, u: u == ctx.author and str(r.emoji) in "1️⃣2️⃣3️⃣" 
        try: 
            reaction, user = await client.wait_for("reaction_add", check=check, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("Timed out, please try again")
            return

        if str(reaction.emoji) == "1️⃣":
            await ctx.send(f"You chose {job1} for your job")
            gamedata["job"] = job1
        if str(reaction.emoji) == "2️⃣":
            await ctx.send(f"You chose {job2} for your job")
            gamedata["job"] = job2
        if str(reaction.emoji) == "3️⃣":
            await ctx.send(f"You chose {job3} for your job")
            gamedata["job"] = job3
        
        savePickle(f"{ctx.author.id}-save.dat", gamedata)
    elif gamedata["job"] != "none":
        validanswers = ["yes", "Yes", "no", "No"]
        await ctx.send("Would You like to work?")
        def check(message):
            return message.author == ctx.author and message.content in validanswers
        try:
            yesNo = await client.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("Timed out, Please try again.")
            return
        
        YesNo = yesNo.content

        if YesNo == "Yes" or YesNo == "yes":
            await ctx.send(f'You chose to work as a(n) {gamedata["job"]}')
            moneyearned = random.randint(20, 30)
            await ctx.send(f"After working you earned {moneyearned}")
            gamedata["money"] += moneyearned
            await ctx.send(f'You have {gamedata["money"]} total money')
        
        savePickle(f"{ctx.author.id}-save.dat", gamedata)

@client.command()
async def shop(ctx):
    embed = discord.Embed(title="Shop")

    await ctx.send(embed=embed)

@client.command()
async def printSaveData(ctx):
    gamedata = loadPickle(f"{ctx.author.id}-save.dat")
    await ctx.send(gamedata)
client.run(TOKEN)
