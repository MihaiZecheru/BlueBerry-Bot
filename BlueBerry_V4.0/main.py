# BlueBerry.py


# ---------------------------------------------------------------------


from discord.ext.commands import cooldown, BucketType
import json, discord, webserver, os, time
from discord.ext import commands
from threading import Thread
from help import Help
from tools import *
from canvasEvents import EventsHandler


# ---------------------------------------------------------------------


class Embeds(Tools):
    @classmethod
    def thanks(cls, giver: str, reciever: str) -> discord.Embed:
        return discord.Embed(timestamp=cls.date(), color=cls.success, description=f"{giver} gave 1 gem :gem: to {reciever}\n\nClick the gem to also thank {reciever}").set_footer(text="+1 💎", icon_url=cls.bburl)
    @classmethod
    def thanks_error(cls, giver: str) -> discord.Embed:
        return discord.Embed(timestamp=cls.date(), color=cls.error, description=f"{giver} you can't give yourself a gem! 💎").set_footer(text="Error", icon_url=cls.bburl)
    
    @classmethod
    def leaderboard(cls, values: list, server_name: str = "Hoopla") -> discord.Embed:
        leaderboard = "\n".join([f"**{values[i][1]}:** {values[i][0]} 💎" for i in range(len(values))])
        return discord.Embed(timestamp=cls.date(), color=cls.blue, description=leaderboard).set_footer(text=f"{server_name.title()} Leaderboard", icon_url=cls.bburl)

    @classmethod
    def balance(cls, user: discord.User) -> discord.Embed:
        return discord.Embed(timestamp=cls.date(), color=cls.blue, description=f"{user.name} has {Gems.get(user.id)} gems 💎").set_footer(text=f"{user.name}'s Balance", icon_url=cls.bburl)
    
    @classmethod
    def user_on_cooldown(cls, username: str, userid: int) -> discord.Embed:
        user_cooldowns = getattr(BlueBerry, "user_cooldowns")
        return discord.Embed(timestamp=cls.date(), color=cls.error, description=f"{username}, you're on cooldown for this command ({user_cooldowns.get(str(userid))}s)").set_footer(text="Cooldown", icon_url=cls.bburl)


class Gems:
    @classmethod
    def __get_user__(cls, id: int) -> json:
        with open(f"jsons/users/{id}.json", "r") as f:
            return json.load(f)

    @classmethod
    def __update_user__(cls, id: int, user_json: object) -> None:
        with open(f"jsons/users/{id}.json", "w") as f:
            json.dump(user_json, f)
        
    @classmethod
    def add(cls, id: int, amount: int = 1) -> None:
        current = cls.__get_user__(id)
        current["gems"] += amount
        cls.__update_user__(id, current)

    @classmethod
    def get(cls, id: int) -> json:
        user = cls.__get_user__(id)
        return user.get("gems")


# ---------------------------------------------------------------------


class BotEvents(Tools):
    bot = commands.Bot(command_prefix=Tools.prefix, intents=Tools.get_intents(), help_command=None)

    @staticmethod
    @bot.event
    async def on_ready(bot=bot) -> None:
        # will be called when the bot is ready to start being used
        activity = discord.Game(name="Tennis with Wyatt", type=3)
        await bot.change_presence(status=discord.Status.online, activity=activity)
        print("\033[1;32;40mAuth and Sign in Complete; Logged in as \033[33m{0.user}\033[0m".format(bot))
        # these cooldowns are only for the thanks/award command
        user_cooldowns = {str(member.id): 0 for member in BlueBerry.bot.get_guild(838622489739001906).members} # guild is hoopla
        setattr(BlueBerry, "user_cooldowns", user_cooldowns)
    
    @staticmethod
    @bot.event
    async def on_member_update(before, after) -> None:
        """ handle name changes """
        if before.name != after.name:
            # change name in file
            with open(f"jsons/users/{before.id}.json", "r") as f:
                data = json.load(f)
                data["name"] = after.name
            with open(f"jsons/users/{after.id}.json", "w") as f:
                json.dump(data, f)

    @staticmethod
    @bot.event
    async def on_member_join(member) -> None:
        """ handle member join """

        # send message
        join_message = "Welcome to {}! To see what I can do, type `!help` in a server you're in with me".format(member.guild.name)
        await member.send(join_message)

        # add to db
        if not os.path.exists(f"jsons/users/{member.id}.json"):
            with open("jsons/users/example_user.json", "r") as f:
                obj = json.load(f)
                obj["name"] = member.name
            with open(f"jsons/users/{member.id}.json", "w") as f:
                json.dump(obj, f)

        # add to cooldowns obj
        user_cooldowns = getattr(BlueBerry, "user_cooldowns")
        user_cooldowns[str(member.id)] = 0
        setattr(BlueBerry, "user_cooldowns", user_cooldowns)
              

    @staticmethod
    @bot.event
    async def on_member_leave(member) -> None:
        """ handle member leave """
        await member.send("bye bye")
        user_cooldowns = getattr(BlueBerry, "user_cooldowns")
        del user_cooldowns[str(member.id)]
        setattr(BlueBerry, "user_cooldowns", user_cooldowns)

    @staticmethod
    @bot.event
    async def on_message(ctx, bot=bot) -> None:
        """ handle thanks command and delete all message in #info channel after 5 seconds """

        """ thanks command """

        if ctx.reference is None or ctx.author == bot.user:
            await bot.process_commands(ctx)
            return

        """ message is a reply """

        # get author
        ref = await ctx.channel.fetch_message(ctx.reference.message_id)
        author = ref.author.name

        if ref.author.id == 910784674664701963:
            await ctx.channel.send("I have enough gems! 💎", delete_after=5)
            return

        # check original message
        if ctx.content.lower().split(" ")[0] in ["!thanks", "thanks", "thanks!", "!thank", "thank", "thank!"]: # checks if message starts with one of these values
            if author == ctx.author.name:
                await ctx.channel.send(embed=Embeds.thanks_error(giver=ctx.author.name))
                return

            if ref.author.bot:
                await ctx.channel.send("You can't thank a bot")
                return
            
            # check cooldown
            user_cooldowns = getattr(BlueBerry, "user_cooldowns")
            if int(user_cooldowns.get(str(ctx.author.id))) > 0:
                await ctx.channel.send(embed=Embeds.user_on_cooldown(ctx.author.name, ctx.author.id))
                return

            award_cooldown = 300 # 5 minutes in seconds
            
            """ user was thanked; award point """
            message = await ctx.channel.send(embed=Embeds.thanks(giver=ctx.author.name, reciever=author))
            Gems.add(ref.author.id)

            # set command cooldown timer
            user_cooldowns[str(ctx.author.id)] = award_cooldown
            setattr(BlueBerry, "user_cooldowns", user_cooldowns)
            cooldown_thread = Thread(daemon=True, target=BotEvents._cooldown_countdown, args=(ctx.author.id,))
            cooldown_thread.start()

            # handle reactions
            await message.add_reaction("💎")

            users_who_reacted = []
            
            @bot.event
            async def on_reaction_add(reaction, user) -> None:
                if user.id == bot.user.id or user.id == ctx.author.id or user.id == ref.author.id or user.id in users_who_reacted:
                    if user.id == ref.author.id:
                        await ctx.channel.send(f"{user.name} you can't give yourself a gem! 💎", delete_after=5)
                    if user.id == ctx.author.id:
                        await ctx.channel.send(f"{ctx.author.name} you can't give someone a gem twice", delete_after=5)
                    return # initial bot reaction or user thanking themselves

                # add gem to user
                Gems.add(ref.author.id)
                users_who_reacted.append(user.id)
                await ctx.channel.send("+1 💎 for **{}** from **{}**".format(author, user.name), delete_after=3)

    @staticmethod
    def _cooldown_countdown(userid: int) -> None:
        user_cooldowns = getattr(BlueBerry, "user_cooldowns")
        while int(user_cooldowns.get(str(userid))) > 0:
            time.sleep(1)
            user_cooldowns[str(userid)] -= 1
            setattr(BlueBerry, "user_cooldowns", user_cooldowns)
          

# ---------------------------------------------------------------------


class BlueBerry(BotEvents, Constants):
    bot = BotEvents.bot

    @staticmethod
    @bot.command(aliases=["info"])
    async def help(ctx: commands.Context, help_with=None) -> None:
        embed = Help.get_embed(help_with) if help_with != None else Help.help_message_all()
        await ctx.channel.send(embed=embed)
    
    @staticmethod
    @bot.command(aliases=["latency"])
    async def ping(ctx: commands.Context, *xtra, bot=bot) -> None:
        await ctx.send(f"Pingu Time: {round(bot.latency * 1000)}ms")

    @staticmethod
    @bot.command(aliases=["thank", "award"])
    async def thanks(ctx: commands.Context, user: discord.User = None, bot=bot) -> None:
        
        award_cooldown = 300 # 5 minutes in seconds

        # check if user is on cooldown
        user_cooldowns = getattr(BlueBerry, "user_cooldowns")
        if int(user_cooldowns.get(str(ctx.author.id))) > 0:
          await ctx.channel.send(embed=Embeds.user_on_cooldown(ctx.author.name, ctx.author.id))
          return

        if user is None:
          return

        if ctx.author.id == user.id:
          await ctx.channel.send(embed=Embeds.thanks_error(ctx.author.name))
          return

        if user.id == 910784674664701963: # bot id
          await ctx.channel.send("I already have enough gems! 💎", delete_after=5)
          return
        
        if user.bot:
            await ctx.channel.send("You can't thank a bot")
            return

        # set command cooldown timer
        user_cooldowns[str(ctx.author.id)] = award_cooldown
        setattr(BlueBerry, "user_cooldowns", user_cooldowns)
        cooldown_thread = Thread(daemon=True, target=BlueBerry._cooldown_countdown, args=(ctx.author.id,))
        cooldown_thread.start()
      
        # send embed
        message = await ctx.channel.send(embed=Embeds.thanks(giver=ctx.author.name, reciever=user.name))

        Gems.add(user.id)

        # handle reactions
        await message.add_reaction("💎")

        users_who_reacted = []
        
        @bot.event
        async def on_reaction_add(reaction, _user) -> None:
            if _user.id == bot.user.id or _user.id == ctx.author.id or _user.id == user.id or _user.id in users_who_reacted:
              if _user.id == user.id:
                await ctx.channel.send(f"{_user.name} you can't give yourself a gem! 💎", delete_after=5)
              if _user.id == ctx.author.id:
                await ctx.channel.send(f"{ctx.author.name} you can't give someone a gem twice", delete_after=5)
              return # initial bot reaction or _user thanking themselves

            # add gem to user
            Gems.add(user.id)
            users_who_reacted.append(_user.id)
            await ctx.channel.send("+1 💎 for **{}** from **{}**".format(_user.name, user.name), delete_after=3)
    
    @staticmethod
    @bot.command(aliases=["lb"])
    async def leaderboard(ctx: commands.Context) -> None:
        # get all user values
        user_gems = []
        for i in os.listdir("jsons/users"):
            if i == "example_user.json":
                continue
            with open(f"jsons/users/{i}", "r") as f:
                content = json.load(f)
                user_gems.append((content.get("gems"), content.get("name")))

        user_gems = Tools.sort_in_reverse(user_gems)[0:10] # sort by first value. user_gems looks like: [(2, 'aditz'), (0, 'Chrysler'), (0, 'VladStefan')]

        await ctx.channel.send(embed=Embeds.leaderboard(user_gems))
    
    @staticmethod
    @bot.command(aliases=["setup_dbs", "setup_members"])
    @commands.has_permissions(administrator=True)
    async def setup_db(ctx: commands.Context) -> None:
        # get boilerplate
        with open('jsons/users/example_user.json', "r") as f:
            obj = json.load(f)

        members = ctx.guild.members
        for member in members:
            if member.bot == True:
                continue
            if not os.path.exists(f"jsons/users/{member.id}.json"):
                # create member
                with open(f"jsons/users/{member.id}.json", "w") as f:
                    obj["name"] = member.name
                    json.dump(obj, f)

        await ctx.channel.send("done")
    
    @staticmethod
    @bot.command(aliases=["balance", "gems", "money"])
    async def bal(ctx: commands.Context, user: discord.User = None) -> None:
        if f"{user.id if user != None else ctx.author.id}.json" in list(os.listdir("jsons/users")): # check if user exists in the server
            await ctx.channel.send(embed=Embeds.balance(user if user != None else ctx.author))

    @staticmethod
    @bot.command(aliases=["reg"])
    async def register(ctx: commands.Context, *teachers: str):
        """ register user's teachers and give them the requested roles """

        await ctx.author.send("Your command was `{}`".format(ctx.message.content.lower()))
        await ctx.message.delete()

        # update file
        user = Gems.__get_user__(ctx.author.id)
        user["teachers"] = []

        # remove current teacher roles
        for teacher in Constants.roles:
          role = discord.utils.get(ctx.guild.roles, id=Constants.roles.get(teacher))
          await ctx.author.remove_roles(role)
        
        # lower all teacher names
        teachers = [teacher.lower() for teacher in teachers]

        # give roles
        _teachers = Constants.hoopla_categories.keys() # teacher names
        for teacher in teachers:
            # add the roles
            if teacher not in _teachers:
                await ctx.author.send("Could not add you to class '{}'".format(teacher))
                continue
            
            role = discord.utils.get(ctx.guild.roles, id=Constants.roles.get(teacher))
            await ctx.author.add_roles(role)
            await ctx.author.send("Added you to class '{}'".format(teacher))
            user['teachers'].append(teacher)

        # process is over
        await ctx.author.send("You are in the following classes: {}".format(", ".join(user.get("teachers"))))
        Gems.__update_user__(ctx.author.id, user_json=user)
        await ctx.channel.send("Done. Check direct messages for the command response", delete_after=5)

    @staticmethod
    @bot.command(aliases=["reset-teacher"])
    @commands.has_permissions(administrator=True)
    async def reset_teacher(ctx: commands.Context, teacher: str = None, *teachers) -> None:
        if teacher == None:
            await ctx.channel.send(embed=Help.get_embed(help_type="reset_teacher"))
            return

        async def remove_channels(teacher: str) -> None:
            """ remove all channels under a teacher except for `#general` """
            # get category
            for guild in BlueBerry.bot.guilds:
                for category in guild.categories:
                    if category.id == Constants.hoopla_categories.get(teacher):
                        channels = category.channels
                        break
            # delete all assignment channels that are not "#general"
            for channel in channels:
                if channel.name not in ["📕│general", "📘│general", "📓│general", "📗│general", "📒│general"]:
                    await channel.delete()
        async def reset_teacher(_teacher: str):
            # check if teacher exists
            if _teacher not in Constants.roles:
                await ctx.channel.send("Teacher does not exist")
                return
            
            # reset teacher
            with open(f"jsons/current_course_assignments/{_teacher}.json", "w") as f:
                f.write("{}")
            await remove_channels(_teacher)
            await ctx.channel.send("Reset {}".format(_teacher))

        if teacher == "all": 
            for i in os.listdir("jsons/current_course_assignments"):
                with open(f"jsons/current_course_assignments/{i}", "w") as f:
                    f.write("{}")
                await remove_channels(i[:-5]) # remove the .json at the end of "i"
            await ctx.channel.send("Reset all teachers")
            return
        
        # reset the initial teacher as teacher arg is not "all"
        await reset_teacher(teacher)

        for _teacher in teachers:
            await reset_teacher(_teacher)
    
    @staticmethod
    @bot.command(aliases=["purge", "remove"])
    @commands.has_permissions(administrator=True)
    async def clear(ctx: commands.Context, amount: int = 5) -> None:
        await ctx.channel.purge(limit=(amount if amount <= 1000 else 1000))
        await ctx.channel.send(f"Removed {amount if amount <= 1000 else 1000} messages", delete_after=3)
    
    @staticmethod
    @bot.command(aliases=["transcript", "transcribe"])
    @commands.has_permissions(administrator=True)
    async def save(ctx: commands.Context, name: str = None) -> None:
        """ generate channel transcript of the past 1000 messages then send to ctx.channel """
        with open(f"{ctx.channel.name if name == None else name}.txt", "w") as file:
            first = True
            async for msg in ctx.channel.history(limit=None):
                if first: # skip first iteration as first message is the "save" cmd
                    first = False
                    continue
                file.write(f"{msg.created_at.strftime('%m/%d/%Y, %H:%M:%S')} - {msg.author.display_name}: {msg.clean_content}\n")
        file = discord.File(f"{ctx.channel.name if name == None else name}.txt")
        await ctx.send(file=file)
        os.remove(f"{ctx.channel.name if name == None else name}.txt")


# ---------------------------------------------------------------------


async def handle_assignment_thread(assignment: object) -> None:
    """ Create the thread and send the assignment_info_embed in that thread """

    # get category id to tell bot where to make new channel
    category_id = Tools.hoopla_categories.get(assignment.teacher)
  
    # get category obj from id
    guild = BlueBerry.bot.get_guild(838622489739001906) # hoopla
    category = discord.utils.get(guild.categories, id=category_id)

    # create new channel for assignment
    channel = await guild.create_text_channel(assignment.name, category=category)
  
    # send the aie message
    assignment_info_embed = await channel.send(embed=assignment.make_embed())

    # DEBUGGING: embeds.fields.value.0 is desc, 1 is date!
    time.sleep(1)
    # get time until due_at date is reached in seconds
    date = assignment._due()
    time_until_expiration = (datetime(int(date[11:15]), int(date[16:18]), int(date[19:]), int(date[:2]), int(date[3:5]), int(date[6:8])) - datetime.today()).total_seconds()

    # save info to obj 
    assignment.__setattr__("remaining_time", int(time_until_expiration)) # round
    assignment.__setattr__("AIE_id", assignment_info_embed.channel.id) # aie = assignment info embed

    # begin deletion timer
    assignment.__begin_aie_deletion_countdown__(BlueBerry.bot)

# handle assignment-posted events
@EventsHandler.__new_assignment_posted__
def on_assignment_post(assignment: object) -> None:
    """ create coro to send embed to channel. The channel the thread & embed are made/sent in is sent in is determined by what class the assignment was made. IE: piper, simons, hagerty """
    BlueBerry.bot.loop.create_task(handle_assignment_thread(assignment))


# ---------------------------------------------------------------------


if __name__ == "__main__":
    # get token
    with open("jsons/token.json", "r") as f:
        token = json.load(f).get("token")
    
    webserver.start()

    # start bot
    BlueBerry.bot.run(token)