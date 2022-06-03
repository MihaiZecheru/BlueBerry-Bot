from datetime import datetime
import discord, pytz, time
from tools import Tools
from threading import Thread
from discord.ext import commands

class Assignment:
    def __init__(self, assignment: dict, assignment_name: str, assigned_in: str) -> None:
        self.assignment = assignment
        self.name = assignment_name
        self.teacher = assigned_in
    
    def _desc(self) -> str:
        return self.assignment.get("description") if self.assignment.get("description") != "" else "This assignment has no description."
    
    def _due(self) -> datetime:
        """ Gets the date and converts it from UTC to PST """

        # example date: 2022-03-12T07:59:59Z
        canvas_date = self.assignment.get("due_at")[:-1] # -1 to remove the Z at the end
        t = canvas_date.index("T")
        day = canvas_date[:t]
        time = canvas_date[t+1:]

        utc = datetime(int(day[:4]), int(day[5:7]), int(day[8:]), int(time[:2]), int(time[3:5]), int(time[6:]), tzinfo = pytz.utc)
        pst = utc.astimezone(pytz.timezone('US/Pacific')).strftime('%Y-%m-%d %H:%M:%S')
        return " - ".join([pst[pst.index(" ")+1:], pst[:pst.index(" ")]])

    def _points_possible(self) -> float:
        return self.assignment.get("points_possible")
    
    def _submission_types(self) -> list:
        types = self.assignment.get("submission_types")
        for i in range(len(types)):
            while "_" in types[i]:
                types[i] = types[i].replace("_", " ").title()

        return ", ".join(types)
    
    def _link(self) -> str:
        return self.assignment.get("html_url")

    def make_embed(self) -> discord.Embed:
        """ Create a discord embed for this assignment object """
        return discord.Embed(color=Tools.blue, timestamp=Tools.date(), title=self.name + "\u200b")\
            .set_footer(text=f"Assignment Created For {self.teacher.capitalize()}")\
            .add_field(name="Description", value=self._desc()+"\u200b" if len("".join(self._desc().split())) < 950 else "".join(self._desc().replace(" ", "*^&").split())[:950].replace("*^&", " ") + " [Description was cut off here]", inline=False)\
            .add_field(name="Due By", value=self._due() + "\u200b", inline=True)\
            .add_field(name="Points Possible", value=str(self._points_possible()) + "\u200b", inline=True)\
            .add_field(name="Submission Types", value=self._submission_types() + "\u200b", inline=False)\
            .add_field(name="Link", value=self._link() + "\u200b", inline=False)

    def _aie_deletion_countdown(self, bot) -> None:
        """ continously remove 5 seconds until remaining_time expires. When the remaining time is less than 0, the due date has passed, so this function handles the deletion sequence """

        # remaining_time is the time in seconds before the due date of the assignment is reached
        while self.__getattribute__("remaining_time") > 0:
            time.sleep(5)
            self.__setattr__("remaining_time", int(self.__getattribute__("remaining_time") - 5))

        ''' remaining_time is less than zero, meaning the assignment's due date has passed. Remove assignment channel and delete the obj '''
        
        # remove assignment channel
        channel = bot.get_channel(self.__getattribute__("AIE_id"))
        bot.loop.create_task(channel.delete())

        # delete the obj
        self.__del__()

    def __begin_aie_deletion_countdown__(self, bot: commands.bot) -> None:
        """ start aie deletion countdown function asyncronously """
        thread = Thread(daemon=True, target=self._aie_deletion_countdown, args=(bot,))
        thread.start()
    
    def __del__(self) -> None:
        """ deletes an object """
        del self