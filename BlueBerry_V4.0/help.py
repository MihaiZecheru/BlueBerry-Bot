import discord
from tools import Tools

class Help(Tools):
    @classmethod
    def help_message_all(cls) -> discord.Embed:
        return discord.Embed(timestamp=cls.date(), color=cls.purple, title="BlueBerry Help", description='`<>` is a required parameter\n`[]` is an optional parameter\n`|` is a symbol for `or`')\
            .set_footer(text="BlueBerry Help", icon_url=cls.bburl)\
            .add_field(name="Gems 💎", value=cls.all_cmds_messages.get("gem"), inline=False)\
            .add_field(name="Misc", value=cls.all_cmds_messages.get("misc"), inline=False)\
            .add_field(name="Admin", value=cls.all_cmds_messages.get("admin"), inline=False)

    @classmethod
    def get_embed(cls, help_type: str) -> discord.Embed:
            help_info = cls.help_messages.get(help_type)

            if help_info == None:
                return

            return discord.Embed(timestamp=cls.date(), color=cls.purple, title=f'{help_type.title()}-Command Information')\
                .set_footer(text="BlueBerry Help", icon_url=cls.bburl)\
                .add_field(inline=False, name="Description", value=help_info.get("desc"))\
                .add_field(inline=False, name="Syntax", value=help_info.get("syntax"))\
                .add_field(inline=False, name="Example", value=help_info.get("example"))\
                .add_field(inline=False, name="Permission", value=help_info.get("perm"))

    _help_messages = {
        "help": {
            "desc": "Returns a card just like this one, displaying information on the given command.",
            "syntax": "`!help [command name]`\n`!info [command name]`",
            "example": "`!help award`",
            "perm": "Member"
        },
        "ping": {
            "desc": "Displays bot latency.",
            "syntax": "`!ping`\n`!latency`",
            "example": "`!ping`",
            "perm": "Member"
        },
        "award": {
            "desc": "Awards the given user a gem 💎. You can see your gems with `!bal` and see the richest members with `!leaderboard`.\n\nAnother way to award a gem to a user is to reply to any message by that user, and start your message with `thank` or `thanks`.",
            "syntax": "`!award <@user>`\n`!thanks <@user>`\n`!thank <@user>`\n",
            "example": "`!award @chrysler`",
            "perm": "Member"
        },
        "register": {
            "desc": "Registers you with the bot. You are given a role for each of the teachers you register with, which will reveal categories for each of those teachers. You can use this command more than once.",
            "syntax": "`!register <teacher> [additional teachers]`\n`!reg <teacher> [additional teachers]`",
            "example": "`!register piper simons de_la_torre king hagerty`\n`!reg konish ocegueda hagerty piper zaragoza`",
            "perm": "Member"
        },
        "leaderboard": {
            "desc": "Returns a list of the top ten richest members on the server. Wealth is determined by gem count.",
            "syntax": "`!leaderboard`\n`!lb`",
            "example": "`!lb`",
            "perm": "Member"
        },
        "balance": {
            "desc": "Displays a user's gem count. If no user is provided, your gem count will be displayed.",
            "syntax": "`!balance [@user]`\n`!balance [@user]`\n`!bal [@user]`\n`!gems [@user]`\n`!money [@user]`",
            "example": "`!bal`\n`!bal @chrysler`",
            "perm": "Member"
        },
        "reset-teacher": {
            "desc": "Multiple teachers can be provided, but they will be ignored if the first given argument is `all`. For each given teacher, BlueBerry will reset the assignment tracker in the db and delete all channels except for `#general` in that category. Assignments will be recreated shortly after",
            "syntax": "`!reset-teachers <teacher | all> [additional teachers]`",
            "example": "`!reset-teachers all`\n`!reset-teachers de_la_torre konish piper simons`",
            "perm": "Admin"
        },
        "setup-db": {
            "desc": "Creates a file for each user with a default/boilerplate json setup.\nProperties: gems, name, teachers.\nName is immediately filled in, and will update automatically.",
            "syntax": "`!setup-db`",
            "example": "`setup-db`",
            "perm": "Admin"
        },
        "clear": {
            "desc": "Removes a specified amount of messages from the channel it's called in. If no amount is specified, 3 messages will be removed.",
            "syntax": "`!clear [amount]`\n`!purge [amount]`",
            "example": "`!clear 12`\n`!purge 1000`",
            "perm": "Admin"
        },
        "save": {
            "desc": "Returns channel transcript of the last 1000 messages as a txt file. The only argument for this command is the name, and if no name is provided, it will default to the channel name.",
            "syntax": "`!save [channel name, does not have to be one word]`",
            "example": "`!save`\n`!transcript cool channel name here`\n`!transcribe HelloWorld`",
            "perm": "Admin"
        }
    }

    help_messages = {
        "help": _help_messages.get("help"),
        "info": _help_messages.get("help"),

        "ping": _help_messages.get("ping"),
        "latency": _help_messages.get("ping"),

        "register": _help_messages.get("register"),
        "reg": _help_messages.get("register"),

        "award": _help_messages.get("award"),
        "thanks": _help_messages.get("award"),
        "thank": _help_messages.get("award"),

        "leaderboard": _help_messages.get("leaderboard"),
        "lb": _help_messages.get("leaderboard"),

        "balance": _help_messages.get("balance"),
        "bal": _help_messages.get("balance"),
        "gems": _help_messages.get("balance"),
        "money": _help_messages.get("balance"),

        "reset-teacher": _help_messages.get("reset-teacher"),
        "reset_teacher": _help_messages.get("reset-teacher"),

        "setup-db": _help_messages.get("setup-db"),
        "setup_db": _help_messages.get("setup-db"),

        "clear": _help_messages.get("clear"),
        "purge": _help_messages.get("purge"),
        "remove": _help_messages.get("remove"),

        "save": _help_messages.get("save"),
        "transcript": _help_messages.get("save"),
        "transcribe": _help_messages.get("save")
    }

    all_cmds_messages = {
        "gem": """
        `!leaderboard`: returns a list of the 10 members with the most gems 💎

        `!balance [@user]`: returns the ammount of gems a user has 💎

        `!thanks <@user>`: awards the given user a gem 💎

        `!award <@user>`: awards the given user a gem 💎
        """,



        "misc": """
        `!register <teacher> [additional teachers]`: Registers you with BlueBerry, which reveals a category for each of the teachers given. Please use `!help register` to understand better.

        `!help [command name]`: returns information on a command, as well as a example on how to use it. Use this if a command is not working for you

        `!ping`: returns bot latency
        """,



        "admin": """
        `!reset-teacher <teacher | all> [additional teachers]`: resets teacher data in BlueBerry and removes the current assignment-channels for the given teacher(s)

        `!setup-db`: initializes user data

        `!clear [amount]`: removes the given amount of messages, which is 5 on default

        `!save [name]`: returns transcript of the last 1000 messages sent in a channel. Default name is the channel name
        """
    }