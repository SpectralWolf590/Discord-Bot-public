import discord
from discord.ext import commands
import asyncio
import random

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

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["clear", "pur", "purge"], name="Purge")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx):
        await ctx.channel.purge()
        await ctx.send("The Channel Was Purged")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def vote(self, ctx, *, tovote):
        await ctx.channel.purge(limit=1)
        message = await ctx.send(f"@everyone Vote for: {tovote}")
        await message.add_reaction('\U0001F44D')
        await message.add_reaction('\U0001F44E')
        

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def giveaway(self, ctx):
        await ctx.send("Let's start with this giveaway! Answer these questions within 15 seconds!")

        questions = ["Which channel should it be hosted in?", "What should be the duration of the giveaway? (s|m|h|d)", "What is the prize of the giveaway?"]

        answers = []

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        for i in questions:
            await ctx.send(i)

            try:
                msg = await commands.wait_for('message', timeout=15.0, check=check)
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

        channel = commands.get_channel(c_id)

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
        users.pop(users.index(commands.user))

        winner = random.choice(users)

        await channel.send(f"Congrats! {winner.mention} won: {prize}!")


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reroll(self, ctx, channel : discord.TextChannel, id_ : int):
        try:
            new_msg = await channel.fetch_message(id_)
        except:
            await ctx.send("The ID that was entered was incorrect, make sure you have entered the correct giveaway message ID.")
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(commands.user))

        winner = random.choice(users)

        await channel.send(f"Congrats the new winner is: {winner.mention} for the giveaway")

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def ban(self, ctx, member : discord.Member, reason=None):
        """Bans a user"""
        if reason == None:
            await ctx.send(f"Woah {ctx.author.mention}, Make sure you provide a reason!")
        else:
            messageok = f"You have been banned from {ctx.guild.name} for {reason}"
            await member.send(messageok)
            await member.ban(reason=reason)

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):

        await member.kick(reason=reason)

        await ctx.send(f'User {member} has been kicked.')
def setup(bot):
    bot.add_cog(AdminCog(bot))