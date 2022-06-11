import discord
from discord.ext import commands
import pickle
import os
import random
import asyncio

validanswers = ["yes", "Yes", "no", "No", "n", 'N', "Y", "y"]
yes = ["Yes", "yes", "Y", "y"]
no = ["No", "no", "N", "n"]

def loadPickle(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)

def savePickle(filename, data):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)
        
class GameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["newSave"])
    async def makeSave(self, ctx):
        gamedata = {"money": 50, "pet": "none", "weapon": "none", "battlepasses": 0, "kills": 0, "job": "none"}
        if os.path.isfile(f"{ctx.author.id}-save.dat") == False:
            savePickle(f"{ctx.author.id}-save.dat", gamedata)
            await ctx.send("Save Created. You start with 50 money")
        else:
            await ctx.send("You already have a save")

    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def job(self, ctx):
        gamedata = loadPickle(f"{ctx.author.id}-save.dat")

        global validanswers
        global yes
        global no

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
                reaction, user = await commands.wait_for("reaction_add", check=check, timeout=30)
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
            
            await ctx.send("Would You like to work?")
            def check(message):
                return message.author == ctx.author and message.content in validanswers
            try:
                yesNo = await commands.wait_for('message', check=check, timeout=30)
            except asyncio.TimeoutError:
                await ctx.send("Timed out, Please try again.")
                return
            
            YesNo = yesNo.content

            if YesNo in yes:
                await ctx.send(f'You chose to work as a(n) {gamedata["job"]}')
                moneyearned = random.randint(20, 30)
                await ctx.send(f"After working you earned {moneyearned} money")
                gamedata["money"] += moneyearned
                await ctx.send(f'You have {gamedata["money"]} total money')
            
            savePickle(f"{ctx.author.id}-save.dat", gamedata)

    @commands.command()
    async def weaponShop(self, ctx):
        gamedata = loadPickle(f"{ctx.author.id}-save.dat")

        embed = discord.Embed(title="Shop")
        numOfItems = 0
        shoplist = ["Sword", "Shield", "Rapier", "Scimitar", "Spear", "Bow", "Staff", "Wand"]
        descriptors = ["A Classic", "To Gaurd You", "Fast And Light", "Heavy but Packs a Punch", "Very easy to Use from a Distance", "Good For Far Distance Attacks", "Allows for Powerful Spells", "Easy To Cast"]
        embed = discord.Embed(title="Welcome to the Weapon Shop")
        embed.add_field(name="***Choose Wisely***", value="***All Weapons are 250 Money***")
        
        for item in shoplist:
            
            embed.add_field(name=f"{numOfItems + 1}. {item}", value=descriptors[numOfItems])
            numOfItems += 1

        await ctx.send(embed=embed)
        await ctx.send("Would You Like To Buy a Weapon?")

        def check(message):
                return message.author == ctx.author and message.content in validanswers
        try:
            yesNo = await commands.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("Timed out, Please try again.")
            return

        yesNo = yesNo.content
        if yesNo in yes:
            await ctx.send("What Would You Like to Buy? Use a Value between 1 and 8 for choice.")
        
        nums = ["1", "2", "3", "4", "5", "6", "7", "8"]
        def check(message):
            return message.author == ctx.author and message.content in nums
        try:
            NumBuy = await commands.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("Timed out, Please try again.")
            return
        NumBuy = NumBuy.content

        Num = int(NumBuy)
        Num -= 1

        buying = shoplist[Num]
        await ctx.send(f"You are buying {buying}")
        await asyncio.sleep(2)
        await ctx.send(f"Transaction Complete. Enjoy Your New {buying}!")
        gamedata["money"] -= 250

        gamedata["weapon"] = buying
        savePickle(f"{ctx.author.id}-save.dat", gamedata)



    @commands.command()
    async def printSaveData(self, ctx):
        gamedata = loadPickle(f"{ctx.author.id}-save.dat")
        await ctx.send(gamedata)

    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def rob(self, ctx, user):

        await ctx.send(f"You are robbing {user}")
        gamedata = loadPickle(f"{ctx.author.id}-save.dat")

        if user.startswith("<@"):
            stolenuser = user.replace("<", "")
            stolenuser = stolenuser.replace(">", "")
            stolenuser = stolenuser.replace("@", "")

            gamedatasteal = loadPickle(f"{stolenuser}-save.dat")

            failchance = random.randint(1, 2)

            if failchance == 1:
                moneymoved = random.randint(40, 60)
                if gamedata["money"] < moneymoved:
                    await ctx.send(f"You were caught. You gave <@{stolenuser}> the rest of your money.")
                    gamedatasteal["money"] += gamedata["money"]
                    gamedata["money"] = 0
                else:
                    await ctx.send(f"You were caught, You paid <@{stolenuser}> {moneymoved} money")
                    gamedata["money"] -= moneymoved
                    gamedatasteal["money"] += moneymoved
                    await ctx.send(f"You now have {gamedata['money']} money")
            elif failchance == 2:
                moneymoved = random.randint(40, 60)
                if gamedatasteal["money"] < moneymoved:
                    moneymoved = gamedatasteal["money"]
                    await ctx.send(f"You stole {moneymoved} from <@{stolenuser}>")
                    gamedata["money"] += gamedatasteal["money"]
                    gamedatasteal["money"] = 0
                else:
                    await ctx.send(f"You stole {moneymoved} from <@{stolenuser}>.")
                    gamedatasteal["money"] -= moneymoved
                    gamedata["money"] += moneymoved
                    await ctx.send(f"You now have {gamedata['money']} money")

        else:
            await ctx.send("You have to properly @ someone")

        savePickle(f"{ctx.author.id}-save.dat", gamedata)
        savePickle(f"{stolenuser}-save.dat", gamedatasteal)

    @commands.command()
    async def bal(self, ctx):
        gamedata = loadPickle(f"{ctx.author.id}-save.dat")
        await ctx.send(f'You have {gamedata["money"]} money')

    @commands.command()
    async def cheatmesomemoneybitch(self, ctx):
        gamedata = loadPickle(f"{ctx.author.id}-save.dat")
        gamedata["money"] += 9000000
        await ctx.send("HERE IS YOUR FUCKING MONEY!")

        savePickle(f"{ctx.author.id}-save.dat", gamedata)

    @commands.command()
    async def resetSave(self, ctx):
        global validanswers
        global yes

        await ctx.send("Are you sure you want to reset?")
        def check(message):
            return message.author == ctx.author and message.content in validanswers
        try:
            YesNo = await commands.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("Timed out, Please try again.")
            return
        
        YesNo = YesNo.content

        if YesNo in yes:
            gamedata = {"money": 50, "pet": "none", "weapon": "none", "battlepasses": 0, "kills": 0, "job": "none"}
            savePickle(f"{ctx.author.id}-save.dat", gamedata)
            await ctx.send("Save Reset! You Have 50 starting money.")
        else:
            await ctx.send("You did not Reset your save")


def setup(bot):
    bot.add_cog(GameCog(bot))