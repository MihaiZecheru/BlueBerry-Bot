from datetime import datetime
import discord

class Constants:
    purple = 0x951cff # purple
    blue = 0x87CEEB # blue
    success = 0x0adb23 # green
    error = 0xdb0a0a # red

    bburl = 'https://cdn.discordapp.com/emojis/932147404344533013.webp?size=96&quality=lossless'
    prefix = "!"
    
    hoopla_categories = {
        # English
        "piper": 950444139546308649,
        "decoste": 951903989627256863,
        
        # History/Health
        "king": 950559617753186345,
        "fullerton": 951926082200805416,
        "ocegueda": 952292825406529616,

        # Math
        "hagerty": 950444514449977364,
        "kilbane": 951903890096398336,
        "burns": 953516313391804466,

        # Spanish
        "de_la_torre": 950556513926254593,
        "konish": 951649334590599168,

        # French
        "jones": 953515928992251934,

        # Science
        "simons": 950444478685122650,
        "zaragoza": 951902900626542662
    }

    roles = {
        "piper": 928111806709366794,
        "king": 928111700572532766,
        "hagerty": 928111640489127997,
        "simons": 928111599561113612,
        "fullerton": 928111672181276783,
        "konish": 928111729039265872,
        "de_la_torre": 928111757908672572,
        "ocegueda": 928118397248614430,
        "decoste": 951903438285996073,
        "kilbane": 951903562202509352,
        "zaragoza": 951903029181972541,
        "jones": 953508296088776724,
        "burns": 953516014652518400
    }


class Tools(Constants):
    @staticmethod
    def get_intents() -> discord.Intents:
        return discord.Intents.all()

    @staticmethod
    def sort_in_reverse(parent_list: list) -> list:
        parent_list.sort(key=lambda x: x[0], reverse=True)
        return parent_list
    
    @staticmethod
    def date() -> datetime.time:
        return datetime.utcnow()