from discord.ext import commands
import random

validanswers = ["yes", "Yes", "no", "No", "n", 'N', "Y", "y"]
yes = ["Yes", "yes", "Y", "y"]
no = ["No", "no", "N", "n"]

class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["dice", "roll", "diceroll"])
    async def rolldice(self, ctx, arg = int(0)):
        if arg == 0:
            await ctx.send("You need to specify how many sides.")
        else:
            await ctx.send(f"You rolled a D{arg}")
            numrolled = random.randint(1, arg)
            await ctx.send(f"You rolled a {numrolled}!")

    @commands.command(aliases=["flipcoin", "coin"])
    async def coinflip(self, ctx):
        sides = ["Heads", "Tails"]
        flipside = random.choice(sides)
        await ctx.send(f"The coin flipped and landed {flipside}")

    @commands.command()
    async def kill(self, ctx, user):
        weapon=("Knife", "Gun", "Sword")
        await ctx.send(ctx.message.author.mention + f" Killed {user} with a {random.choice(weapon)}")

    @commands.command()
    async def stab(self, ctx, user):
        await ctx.send(f"{ctx.message.author.mention} Just stabbed {user}")
        
    @commands.command()
    async def insult(self, ctx, user):
        insults = ("Screw you", "You are a jerk", "You suck", "OH NO ITS", "Ugh, its", "EVERYBODY GET OUT, ITS", "Deal with it")
        await ctx.send(f"{random.choice(insults)} {user}")
        
    @commands.command()
    async def compliment(self, ctx, user):
        compliments = ("Is Looking nice today", "Is Awesome", "Is a good person", "Is nice", "Is A cool person", "Isn't an idiot", "Needs to talk more")
        await ctx.send(f"{user} {random.choice(compliments)}")
        
    @commands.command()
    async def mental(self, ctx):
        answers = ("Is Mentally Insane", "Is Mentally Stable", "Is Going Insane", "Needs therapy", "Needs a huge suppository", "Is an idiot", "Has Crippling Depression")
        await ctx.send(f"{ctx.author.mention} {random.choice(answers)}")

    @commands.command(name="8ball",
                    decription="Chooses stuff For You, maybe a little insulting",
                    aliases=["Eight Ball", "8-ball", "eight ball", "8-Ball"],
                    pass_context=True)
    async def eight_ball(self, ctx):
        possible_responses = [
                'Thats gonna have to be a no',
                'It Is not looking likely',
                'For Sure you jerk',
                'Fuck you im not answering that',
                'Might be Likely you idiot',
                'I dont care you piece of shit',
                'Ok The answer is FRICK yes.', ]
        await ctx.send(random.choice(possible_responses) + ", " + ctx.message.author.mention)

def setup(bot):
    bot.add_cog(FunCog(bot))