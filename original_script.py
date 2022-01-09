import discord
from os import environ
from replit import db
from datetime import date
from threading import Event, Timer
from webserver import to_import

yellow = 0xF3FF00
green = 0x127f06
blue = 0x110adb
purple = 0xff00ff
pink = 0xFF00A2
red = 0x8c0d13
teal = 0x48C9B0
success = 0x0adb23
error = 0xdb0a0a

# gets todays date in m/d format, then extracts date from tests and removes # # study/test category from categories that are overdue.
def auto_remove_test():
    try:
        today = date.today()
        d = str(today.strftime("%m/%d/%y"))

        dateToday = []
        dateToday.extend(d)

        for i in range(len(dateToday)):
            if dateToday[i] == "/":
                today_month = (dateToday[0:i])
                break
        today_month = "".join(today_month)

        count = 0
        for i in range(len(dateToday)):

            if dateToday[i] == "/" and count == 1:
                today_day = (dateToday[(first + 1):i])
                break
            if dateToday[i] == "/" and count == 0:
                first = i
                count += 1
        today_day = "".join(today_day)
        today_day = int(today_day)
        today_day -= 1

        def clear_test_piper():
            try:
                value = db["piper_test"]
                temp = []
                test_date = []
                temp.extend(value)
                for i in range(len(temp)):
                    if i == 0:
                        i = 1
                    if temp[-i] != " ":
                        test_date.append(temp[-i])
                    elif temp[-i] == " ":
                        break
                test_date.remove(test_date[0])
                test_date.reverse()
                test_date = "".join(test_date)

                for i in range(len(test_date)):
                    if test_date[i] == "/":
                        test_month = (test_date[0:i])
                    count = 0
                for i in range(len(test_date)):
                    if test_date[i] == "/":
                        test_day = test_date[(i + 1):]

                if (int(test_month)
                    == int(today_month)) and (int(test_day) < int(today_day)):
                    db["piper_test"] = []
                    db["piper_study_quizlet"] = []
                    db["piper_study_notes"] = []
                    db["piper_study_other"] = []
                    print(
                        f"\t\t\033[0;32;40m- Removed piper test_date: \033[0;36;40m{value}\n"
                    )
                elif (int(test_month) < int(today_month)):
                    db["piper_test"] = []
                    db["piper_study_quizlet"] = []
                    db["piper_study_notes"] = []
                    db["piper_study_other"] = []
                    print(
                        f"\t\033[0;32;40m- Removed piper test_date: \033[0;36;40m{value}\n"
                    )
                else:
                    print(
                        "\t\033[0;32;40m- piper test_date exists\n\t\033[0;36;40m- No keys deleted from piper\n"
                    )
            except:
                print("\t\033[0;31;40m - piper test_date does not exist\n")

        def clear_test_hagerty():
            try:
                value = db["hagerty_test"]
                temp = []
                test_date = []
                temp.extend(value)
                for i in range(len(temp)):
                    if i == 0:
                        i = 1
                    if temp[-i] != " ":
                        test_date.append(temp[-i])
                    elif temp[-i] == " ":
                        break
                test_date.remove(test_date[0])
                test_date.reverse()
                test_date = "".join(test_date)

                for i in range(len(test_date)):
                    if test_date[i] == "/":
                        test_month = (test_date[0:i])
                    count = 0
                for i in range(len(test_date)):
                    if test_date[i] == "/":
                        test_day = test_date[(i + 1):]

                if (int(test_month)
                    == int(today_month)) and (int(test_day) < int(today_day)):
                    db["hagerty_test"] = []
                    db["hagerty_study_quizlet"] = []
                    db["hagerty_study_notes"] = []
                    db["hagerty_study_other"] = []
                    print(
                        f"\t\t\033[0;32;40m- Removed hagerty test_date: \033[0;36;40m{value}\n"
                    )
                elif (int(test_month) < int(today_month)):
                    db["hagerty_test"] = []
                    db["hagerty_study_quizlet"] = []
                    db["hagerty_study_notes"] = []
                    db["hagerty_study_other"] = []
                    print(
                        f"\t\033[0;32;40m- Removed hagerty test_date: \033[0;36;40m{value}\n"
                    )
                else:
                    print(
                        "\t\033[0;32;40m- hagerty test_date exists\n\t\033[0;36;40m- No keys deleted from hagerty\n"
                    )
            except:
                print("\t\033[0;31;40m - hagerty test_date does not exist\n")

        def clear_test_fullerton():
            try:
                value = db["fullerton_test"]
                temp = []
                test_date = []
                temp.extend(value)
                for i in range(len(temp)):
                    if i == 0:
                        i = 1
                    if temp[-i] != " ":
                        test_date.append(temp[-i])
                    elif temp[-i] == " ":
                        break
                test_date.remove(test_date[0])
                test_date.reverse()
                test_date = "".join(test_date)

                for i in range(len(test_date)):
                    if test_date[i] == "/":
                        test_month = (test_date[0:i])
                    count = 0
                for i in range(len(test_date)):
                    if test_date[i] == "/":
                        test_day = test_date[(i + 1):]

                if (int(test_month)
                    == int(today_month)) and (int(test_day) < int(today_day)):
                    db["fullerton_test"] = []
                    db["fullerton_study_quizlet"] = []
                    db["fullerton_study_notes"] = []
                    db["fullerton_study_other"] = []
                    print(
                        f"\t\t\033[0;32;40m- Removed fullerton test_date: \033[0;36;40m{value}\n"
                    )
                elif (int(test_month) < int(today_month)):
                    db["fullerton_test"] = []
                    db["fullerton_study_quizlet"] = []
                    db["fullerton_study_notes"] = []
                    db["fullerton_study_other"] = []
                    print(
                        f"\t\033[0;32;40m- Removed fullerton test_date: \033[0;36;40m{value}\n"
                    )
                else:
                    print(
                        "\t\033[0;32;40m- fullerton test_date exists\n\t\033[0;36;40m- No keys deleted from fullerton\n"
                    )
            except:
                print("\t\033[0;31;40m - fullerton test_date does not exist\n")

        def clear_test_torre():
            try:
                value = db["torre_test"]
                temp = []
                test_date = []
                temp.extend(value)
                for i in range(len(temp)):
                    if i == 0:
                        i = 1
                    if temp[-i] != " ":
                        test_date.append(temp[-i])
                    elif temp[-i] == " ":
                        break
                test_date.remove(test_date[0])
                test_date.reverse()
                test_date = "".join(test_date)

                for i in range(len(test_date)):
                    if test_date[i] == "/":
                        test_month = (test_date[0:i])
                    count = 0
                for i in range(len(test_date)):
                    if test_date[i] == "/":
                        test_day = test_date[(i + 1):]

                if (int(test_month)
                    == int(today_month)) and (int(test_day) < int(today_day)):
                    db["torre_test"] = []
                    db["torre_study_quizlet"] = []
                    db["torre_study_notes"] = []
                    db["torre_study_other"] = []
                    print(
                        f"\t\t\033[0;32;40m- Removed torre test_date: \033[0;36;40m{value}\n"
                    )
                elif (int(test_month) < int(today_month)):
                    db["torre_test"] = []
                    db["torre_study_quizlet"] = []
                    db["torre_study_notes"] = []
                    db["torre_study_other"] = []
                    print(
                        f"\t\033[0;32;40m- Removed torre test_date: \033[0;36;40m{value}\n"
                    )
                else:
                    print(
                        "\t\033[0;32;40m- torre test_date exists\n\t\033[0;36;40m- No keys deleted from torre\n"
                    )
            except:
                print("\t\033[0;31;40m - torre test_date does not exist\n")

        def clear_test_simons():
            try:
                value = db["simons_test"]
                temp = []
                test_date = []
                temp.extend(value)
                for i in range(len(temp)):
                    if i == 0:
                        i = 1
                    if temp[-i] != " ":
                        test_date.append(temp[-i])
                    elif temp[-i] == " ":
                        break
                test_date.remove(test_date[0])
                test_date.reverse()
                test_date = "".join(test_date)
                for i in range(len(test_date)):
                    if test_date[i] == "/":
                        test_month = (test_date[0:i])
                    count = 0
                for i in range(len(test_date)):
                    if test_date[i] == "/":
                        test_day = test_date[(i + 1):]
                if (int(test_month)
                    == int(today_month)) and (int(test_day) < int(today_day)):
                    db["simons_test"] = []
                    db["simons_study_quizlet"] = []
                    db["simons_study_notes"] = []
                    db["simons_study_other"] = []
                    print(
                        f"\t\033[0;32;40m- Removed simons test_date: \033[0;36;40m{value}\n"
                    )
                elif (int(test_month) < int(today_month)):
                    db["simons_test"] = []
                    db["simons_study_quizlet"] = []
                    db["simons_study_notes"] = []
                    db["simons_study_other"] = []
                    print(
                        f"\t\033[0;32;40m- Removed simons test_date: \033[0;36;40m{value}\n"
                    )
                else:
                    print(
                        "\t\033[0;32;40m- simons test_date exists\n\t\033[0;36;40m- No keys deleted from simons\n"
                    )
            except:
                print("\t\033[0;31;40m - simons test_date does not exist\n")

        def clear_test_burns():
            try:
                value = db["burns_test"]
                temp = []
                test_date = []
                temp.extend(value)
                for i in range(len(temp)):
                    if i == 0:
                        i = 1
                    if temp[-i] != " ":
                        test_date.append(temp[-i])
                    elif temp[-i] == " ":
                        break
                test_date.remove(test_date[0])
                test_date.reverse()
                test_date = "".join(test_date)

                for i in range(len(test_date)):
                    if test_date[i] == "/":
                        test_month = (test_date[0:i])
                    count = 0
                for i in range(len(test_date)):
                    if test_date[i] == "/":
                        test_day = test_date[(i + 1):]

                if (int(test_month)
                    == int(today_month)) and (int(test_day) < int(today_day)):
                    db["burns_test"] = []
                    db["burns_study_quizlet"] = []
                    db["burns_study_notes"] = []
                    db["burns_study_other"] = []
                    print(
                        f"\t\t\033[0;32;40m- Removed burns test_date: \033[0;36;40m{value}\n"
                    )
                elif (int(test_month) < int(today_month)):
                    db["burns_test"] = []
                    db["burns_study_quizlet"] = []
                    db["burns_study_notes"] = []
                    db["burns_study_other"] = []
                    print(
                        f"\t\033[0;32;40m- Removed burns test_date: \033[0;36;40m{value}\n"
                    )
                else:
                    print(
                        "\t\033[0;32;40m- burns test_date exists\n\t\033[0;36;40m- No keys deleted from torre\n"
                    )
            except:
                print("\t\033[0;31;40m - burns test_date does not exist\n")
    except:
        print("\t- Entire Function Crashed\n")
    print("\033[0;33;40m Hourly Check Complete")
    clear_test_piper()
    clear_test_hagerty()
    clear_test_fullerton()
    clear_test_torre()
    clear_test_simons()
    clear_test_burns()


# run auto_remove_test every hour
def f(f_stop):
    auto_remove_test()
    if not f_stop.is_set():
        Timer(3600, f, [f_stop]).start()


f_stop = Event()
f(f_stop)

client = discord.Client()


@client.event
async def on_ready():
    # will be called when the bot is ready to start being used
    activity = discord.Game(name="Tennis with Wyatt", type=3)
    await client.change_presence(status=discord.Status.online,
                                 activity=activity)
    print("\033[1;32;40m Auth and Sign in Complete; Logged in as {0.user}".
          format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == "?clear all 123456789":
        # TODO: reset all DB's. Like db['piper_study_quizlet'] = []
        # and db['piper_test'] = ""
        pass

    # Piper English
    if message.content.startswith("?add piper test"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])

        db["piper_test"] = f"{' '.join(msg[1:])} | {msg[0]}"

        value = db["piper_test"]

        embedVar = discord.Embed(
            title="Success",
            description="The following test was added: '" + db["piper_test"] +
            "'",
            color=success)
        await message.channel.send(embed=embedVar)

    elif message.content.startswith(
        "?add piper hw") or message.content.startswith("?add piper homework"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])

        db["piper_hw"].append(f"\n{' '.join(msg[1:])} | {msg[0]}")

        embedVar = discord.Embed(title="Homework Added",
                                 description="'" + ' '.join(msg[1:]) + " | " +
                                 msg[0] + "' added to Piper's Homework",
                                 color=success)
        await message.channel.send(embed=embedVar)
        embedVar = discord.Embed(title="Piper's Homework",
                                 description='\n'.join(db["piper_hw"]),
                                 color=purple)
        await message.channel.send(embed=embedVar)

    elif message.content.startswith("?add piper quizlet"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = "".join(msg)
        quizlet = db["piper_study_quizlet"]
        quizlet.append(msg)
        if quizlet[0] == "":
            quizlet.remove(quizlet[0])
        embedVar = discord.Embed(
            title="Success",
            description=
            f"Your Quizlet ({msg}) was succesfully added to 'Piper Study'",
            color=success)
        await message.channel.send(embed=embedVar)
        quizlet = '\n'.join(quizlet)
        notes = '\n'.join(db['piper_study_notes'])
        other = '\n'.join(db['piper_study_other'])
        embedVar = discord.Embed(
            title="Piper's Study",
            description=
            f"**Quizlets:**\n{quizlet}\n\n**Notes:**\n{notes}\n\n**Other:**\n{other}",
            color=purple)
        await message.channel.send(embed=embedVar)

    elif message.content.startswith("?add piper notes"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = "".join(msg)
        notes = db["piper_study_notes"]
        notes.append(msg)
        embedVar = discord.Embed(
            title="Success",
            description=
            f"Your notes ({msg}) were succesfully added to 'Piper Study'",
            color=success)
        await message.channel.send(embed=embedVar)
        quizlet = '\n'.join(db['piper_study_other'])
        notes = '\n'.join(db['piper_study_notes'])
        other = '\n'.join(db['piper_study_other'])
        embedVar = discord.Embed(
            title="Piper's Study",
            description=
            f"**Quizlets:**\n{quizlet}\n\n**Notes:**\n{notes}\n\n**Other:**\n{other}",
            color=purple)
        await message.channel.send(embed=embedVar)
    elif message.content.startswith("?add piper other"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = "".join(msg)
        other = db["piper_study_other"]
        other.append(msg)
        embedVar = discord.Embed(
            title="Success",
            description=
            f"Your resource ({msg}) was succesfully added to 'Piper Study'",
            color=success)
        quizlet = '\n'.join(db['piper_study_other'])
        notes = '\n'.join(db['piper_study_notes'])
        other = '\n'.join(db['piper_study_other'])
        embedVar = discord.Embed(
            title="Piper's Study",
            description=
            f"**Quizlets:**\n{quizlet}\n\n**Notes:**\n{notes}\n\n**Other:**\n{other}",
            color=purple)
        await message.channel.send(embed=embedVar)

    elif message.content.lower() == "?piper hw" or message.content.lower(
    ) == "?piper homework":
        embedVar = discord.Embed(title="Piper's Homework",
                                 description='\n'.join(db["piper_hw"]),
                                 color=purple)
        await message.channel.send(embed=embedVar)
    elif message.content.lower() == "?piper test":
        value = db["piper_test"]
        embedVar = discord.Embed(
            title="Piper's Test",
            description=f"Piper's next test is on: {value}",
            color=purple)
        await message.channel.send(embed=embedVar)

    elif message.content.lower() == "?piper study":
        quizlet = '\n'.join(db['piper_study_quizlet'])
        notes = '\n'.join(db['piper_study_notes'])
        other = '\n'.join(db['piper_study_other'])
        embedVar = discord.Embed(
            title="Piper's Study",
            description=
            f"**Quizlets:**\n{quizlet}\n\n**Notes:**\n{notes}\n\n**Other:**\n{other}",
            color=purple)
        await message.channel.send(embed=embedVar)

    elif message.content.lower() == (
        "?remove piper test"
    ) or message.content.lower() == "?clear piper test":
        try:
            if db['piper_test'][0] == ' ':
                pass
        except:
            db['piper_test'].insert(0, ' ')
        length = len(db['piper_test'])
        if length > 1:
            if db['piper_test'][0] == ' ':
                db['piper_test'].remove(' ')
            embedVar = discord.Embed(
                title="Success",
                description=
                f"Piper's Test {(db['piper_test'])} has been removed",
                color=success)
            await message.channel.send(embed=embedVar)
            db["piper_test"] = []
        else:
            embedVar = discord.Embed(
                title="Error",
                description=f"There is no test to remove in Piper Test",
                color=error)
            await message.channel.send(embed=embedVar)

    elif message.content.startswith(
        "?remove piper hw") or message.content.startswith(
            "?remove piper homework"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = msg[0]
        if len(db['piper_hw']) >= int(msg):
            embedVar = discord.Embed(
                title="Success",
                color=success,
                description=
                f"'{db['piper_hw'][(int(msg) - 1)]}' was succesfully removed from Piper Homework"
            )
            await message.channel.send(embed=embedVar)
            db['piper_hw'].remove(db['piper_hw'][(int(msg) - 1)])
        else:
            embedVar = discord.Embed(
                title="Error",
                color=error,
                description=f"Piper Homework 'Option {msg}' does not exist")
            await message.channel.send(embed=embedVar)

    elif message.content.startswith(
        "?remove piper quizlet") or message.content.startswith(
            "?remove piper quizlets"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = msg[0]
        if len(db['piper_study_quizlet']) >= int(msg):
            embedVar = discord.Embed(
                title="Success",
                color=success,
                description=
                f"Quizlet '{db['piper_study_quizlet'][(int(msg) - 1)]}' was succesfully removed from Piper Study"
            )
            await message.channel.send(embed=embedVar)
            db['piper_study_quizlet'].remove(
                db['piper_study_quizlet'][(int(msg) - 1)])
        else:
            embedVar = discord.Embed(
                title="Error",
                color=error,
                description=
                f"Piper Study 'Option {msg}' does not exist in Quizlet")
            await message.channel.send(embed=embedVar)

    elif message.content.startswith(
        "?remove piper notes") or message.content.startswith(
            "?remove piper note"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = msg[0]
        if len(db['piper_study_notes']) >= int(msg):
            embedVar = discord.Embed(
                title="Success",
                color=success,
                description=
                f"Note '{db['piper_study_notes'][(int(msg) - 1)]}' was succesfully removed from Piper Study"
            )
            await message.channel.send(embed=embedVar)
            db['piper_study_notes'].remove(db['piper_study_notes'][(int(msg) -
                                                                    1)])
        else:
            embedVar = discord.Embed(
                title="Error",
                color=error,
                description=
                f"Piper Study 'Option {msg}' does not exist in Notes")
            await message.channel.send(embed=embedVar)

    elif message.content.startswith("?remove piper other"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = msg[0]
        if len(db['piper_study_other']) >= int(msg):
            embedVar = discord.Embed(
                title="Success",
                color=success,
                description=
                f"Other '{db['piper_study_other'][(int(msg) - 1)]}' was succesfully removed from Piper Study"
            )
            await message.channel.send(embed=embedVar)
            db['piper_study_other'].remove(db['piper_study_other'][(int(msg) -
                                                                    1)])
        else:
            embedVar = discord.Embed(
                title="Error",
                color=error,
                description=
                f"Piper Study 'Option {msg}' does not exist in Other")
            await message.channel.send(embed=embedVar)

    elif message.content.lower() == (
        "?clear piper hw"
    ) or message.content.lower() == "?clear piper homework":
        try:
            if db['piper_hw'][0] == ' ':
                pass
        except:
            db['piper_hw'].insert(0, ' ')
        length = len(db['piper_hw'])
        if length > 1:
            if db['piper_hw'][0] == ' ':
                db['piper_hw'].remove(' ')
            embedVar = discord.Embed(title="Success",
                                     description=f"Piper's Homework Cleared",
                                     color=success)
            await message.channel.send(embed=embedVar)
            db["piper_hw"] = []
        else:
            embedVar = discord.Embed(
                title="Error",
                description=f"There is no homework to clear in Piper Homework",
                color=error)
            await message.channel.send(embed=embedVar)

    elif message.content.lower(
    ) == "?clear piper quizlet" or message.content.lower(
    ) == "?clear piper quizlets":
        try:
            if db['piper_study_quizlet'][0] == ' ':
                pass
        except:
            db['piper_study_quizlet'].insert(0, ' ')
        length = len(db['piper_study_quizlet'])
        if length > 1:
            if db['piper_study_quizlet'][0] == ' ':
                db['piper_study_quizlet'].remove(' ')
            embedVar = discord.Embed(
                title="Success",
                description=f"Piper's Study Quizlets Cleared",
                color=success)
            await message.channel.send(embed=embedVar)
            db["piper_study_quizlet"] = []
        else:
            embedVar = discord.Embed(
                title="Error",
                description=f"There are no Quizlets to clear in Piper Study",
                color=error)
            await message.channel.send(embed=embedVar)

    elif message.content.lower(
    ) == "?clear piper notes" or message.content.lower(
    ) == "?clear piper note":
        try:
            if db['piper_study_notes'][0] == ' ':
                pass
        except:
            db['piper_study_notes'].insert(0, ' ')
        length = len(db['piper_study_notes'])
        if length > 1:
            if db['piper_study_notes'][0] == ' ':
                db['piper_study_notes'].remove(' ')
            embedVar = discord.Embed(
                title="Success",
                description=f"Piper's Study Notes Cleared",
                color=success)
            await message.channel.send(embed=embedVar)
            db["piper_study_notes"] = []
        else:
            embedVar = discord.Embed(
                title="Error",
                description=f"There are no Notes to clear in Piper Study",
                color=error)
            await message.channel.send(embed=embedVar)

    elif message.content.lower(
    ) == "?clear piper other" or message.content.lower(
    ) == "?clear piper others":
        try:
            if db['piper_study_other'][0] == ' ':
                pass
        except:
            db['piper_study_other'].insert(0, ' ')
        length = len(db['piper_study_other'])
        if length > 1:
            if db['piper_study_other'][0] == ' ':
                db['piper_study_other'].remove(' ')
            embedVar = discord.Embed(
                title="Success",
                description=f"Piper's Study Other Cleared",
                color=success)
            await message.channel.send(embed=embedVar)
            db["piper_study_other"] = []
        else:
            embedVar = discord.Embed(
                title="Error",
                description=
                f"There are no 'Other' resources to clear in Piper Study",
                color=error)
            await message.channel.send(embed=embedVar)

    elif message.content.lower(
    ) == "?clear piper study" or message.content.lower(
    ) == "?clear piper studys" or message.content.lower(
    ) == "?clear piper studies":
        db['piper_study_other'] = []
        db['piper_study_quizlet'] = []
        db['piper_study_notes'] = []

        embedVar = discord.Embed(title="Success",
                                 description=f"Piper's Study Cleared",
                                 color=success)
        await message.channel.send(embed=embedVar)

    # Hagerty Math
    if message.content.startswith("?add hagerty test"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])

        db["hagerty_test"] = f"{' '.join(msg[1:])} | {msg[0]}"

        value = db["hagerty_test"]

        embedVar = discord.Embed(
            title="Success",
            description="The following test was added: '" +
            db["hagerty_test"] + "'",
            color=success)
        await message.channel.send(embed=embedVar)

    elif message.content.startswith(
        "?add hagerty hw") or message.content.startswith(
            "?add hagerty homework"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])

        db["hagerty_hw"].append(f"\n{' '.join(msg[1:])} | {msg[0]}")

        embedVar = discord.Embed(title="Homework Added",
                                 description="'" + ' '.join(msg[1:]) + " | " +
                                 msg[0] + "' added to Hagerty's Homework",
                                 color=success)
        await message.channel.send(embed=embedVar)
        embedVar = discord.Embed(title="Hagerty's Homework",
                                 description='\n'.join(db["hagerty_hw"]),
                                 color=blue)
        await message.channel.send(embed=embedVar)

    elif message.content.startswith("?add hagerty quizlet"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = "".join(msg)
        quizlet = db["hagerty_study_quizlet"]
        quizlet.append(msg)
        if quizlet[0] == "":
            quizlet.remove(quizlet[0])
        embedVar = discord.Embed(
            title="Success",
            description=
            f"Your Quizlet ({msg}) was succesfully added to 'Hagerty Study'",
            color=success)
        await message.channel.send(embed=embedVar)
        quizlet = '\n'.join(quizlet)
        notes = '\n'.join(db['hagerty_study_notes'])
        other = '\n'.join(db['hagerty_study_other'])
        embedVar = discord.Embed(
            title="Hagerty's Study",
            description=
            f"**Quizlets:**\n{quizlet}\n\n**Notes:**\n{notes}\n\n**Other:**\n{other}",
            color=blue)
        await message.channel.send(embed=embedVar)

    elif message.content.startswith("?add hagerty notes"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = "".join(msg)
        notes = db["hagerty_study_notes"]
        notes.append(msg)
        embedVar = discord.Embed(
            title="Success",
            description=
            f"Your notes ({msg}) were succesfully added to 'Hagerty Study'",
            color=success)
        await message.channel.send(embed=embedVar)
        quizlet = '\n'.join(db['hagerty_study_other'])
        notes = '\n'.join(db['hagerty_study_notes'])
        other = '\n'.join(db['hagerty_study_other'])
        embedVar = discord.Embed(
            title="Hagerty's Study",
            description=
            f"**Quizlets:**\n{quizlet}\n\n**Notes:**\n{notes}\n\n**Other:**\n{other}",
            color=blue)
        await message.channel.send(embed=embedVar)
    elif message.content.startswith("?add hagerty other"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = "".join(msg)
        other = db["hagerty_study_other"]
        other.append(msg)
        embedVar = discord.Embed(
            title="Success",
            description=
            f"Your resource ({msg}) was succesfully added to 'Hagerty Study'",
            color=success)
        quizlet = '\n'.join(db['hagerty_study_other'])
        notes = '\n'.join(db['hagerty_study_notes'])
        other = '\n'.join(db['hagerty_study_other'])
        embedVar = discord.Embed(
            title="Hagerty's Study",
            description=
            f"**Quizlets:**\n{quizlet}\n\n**Notes:**\n{notes}\n\n**Other:**\n{other}",
            color=blue)
        await message.channel.send(embed=embedVar)

    elif message.content.lower() == "?hagerty hw" or message.content.lower(
    ) == "?hagerty homework":
        embedVar = discord.Embed(title="Hagerty's Homework",
                                 description='\n'.join(db["hagerty_hw"]),
                                 color=blue)
        await message.channel.send(embed=embedVar)
    elif message.content.lower() == "?hagerty test":
        value = db["hagerty_test"]
        embedVar = discord.Embed(
            title="Hagerty's Test",
            description=f"Hagerty's next test is on: {value}",
            color=blue)
        await message.channel.send(embed=embedVar)

    elif message.content.lower() == "?hagerty study":
        quizlet = '\n'.join(db['hagerty_study_quizlet'])
        notes = '\n'.join(db['hagerty_study_notes'])
        other = '\n'.join(db['hagerty_study_other'])
        embedVar = discord.Embed(
            title="Hagerty's Study",
            description=
            f"**Quizlets:**\n{quizlet}\n\n**Notes:**\n{notes}\n\n**Other:**\n{other}",
            color=blue)
        await message.channel.send(embed=embedVar)

    elif message.content.lower() == (
        "?remove hagerty test"
    ) or message.content.lower() == "?clear hagerty test":
        try:
            if db['hagerty_test'][0] == ' ':
                pass
        except:
            db['hagerty_test'].insert(0, ' ')
        length = len(db['hagerty_test'])
        if length > 1:
            if db['hagerty_test'][0] == ' ':
                db['hagerty_test'].remove(' ')
            embedVar = discord.Embed(
                title="Success",
                description=
                f"Hagerty's Test {(db['hagerty_test'])} has been removed",
                color=success)
            await message.channel.send(embed=embedVar)
            db["hagerty_test"] = []
        else:
            embedVar = discord.Embed(
                title="Error",
                description=f"There is no test to remove in Hagerty Test",
                color=error)
            await message.channel.send(embed=embedVar)

    elif message.content.startswith(
        "?remove hagerty hw") or message.content.startswith(
            "?remove hagerty homework"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = msg[0]
        if len(db['hagerty_hw']) >= int(msg):
            embedVar = discord.Embed(
                title="Success",
                color=success,
                description=
                f"'{db['hagerty_hw'][(int(msg) - 1)]}' was succesfully removed from Hagerty Homework"
            )
            await message.channel.send(embed=embedVar)
            db['hagerty_hw'].remove(db['hagerty_hw'][(int(msg) - 1)])
        else:
            embedVar = discord.Embed(
                title="Error",
                color=error,
                description=f"Hagerty Homework 'Option {msg}' does not exist")
            await message.channel.send(embed=embedVar)

    elif message.content.startswith(
        "?remove hagerty quizlet") or message.content.startswith(
            "?remove hagerty quizlets"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = msg[0]
        if len(db['hagerty_study_quizlet']) >= int(msg):
            embedVar = discord.Embed(
                title="Success",
                color=success,
                description=
                f"Quizlet '{db['hagerty_study_quizlet'][(int(msg) - 1)]}' was succesfully removed from Hagerty Study"
            )
            await message.channel.send(embed=embedVar)
            db['hagerty_study_quizlet'].remove(
                db['hagerty_study_quizlet'][(int(msg) - 1)])
        else:
            embedVar = discord.Embed(
                title="Error",
                color=error,
                description=
                f"Hagerty Study 'Option {msg}' does not exist in Quizlet")
            await message.channel.send(embed=embedVar)

    elif message.content.startswith(
        "?remove hagerty notes") or message.content.startswith(
            "?remove hagerty note"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = msg[0]
        if len(db['hagerty_study_notes']) >= int(msg):
            embedVar = discord.Embed(
                title="Success",
                color=success,
                description=
                f"Note '{db['hagerty_study_notes'][(int(msg) - 1)]}' was succesfully removed from Hagerty Study"
            )
            await message.channel.send(embed=embedVar)
            db['hagerty_study_notes'].remove(
                db['hagerty_study_notes'][(int(msg) - 1)])
        else:
            embedVar = discord.Embed(
                title="Error",
                color=error,
                description=
                f"Hagerty Study 'Option {msg}' does not exist in Notes")
            await message.channel.send(embed=embedVar)

    elif message.content.startswith("?remove hagerty other"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = msg[0]
        if len(db['hagerty_study_other']) >= int(msg):
            embedVar = discord.Embed(
                title="Success",
                color=success,
                description=
                f"Other '{db['hagerty_study_other'][(int(msg) - 1)]}' was succesfully removed from Hagerty Study"
            )
            await message.channel.send(embed=embedVar)
            db['hagerty_study_other'].remove(
                db['hagerty_study_other'][(int(msg) - 1)])
        else:
            embedVar = discord.Embed(
                title="Error",
                color=error,
                description=
                f"Hagerty Study 'Option {msg}' does not exist in Other")
            await message.channel.send(embed=embedVar)

    elif message.content.lower() == (
        "?clear hagerty hw"
    ) or message.content.lower() == "?clear hagerty homework":
        try:
            if db['hagerty_hw'][0] == ' ':
                pass
        except:
            db['hagerty_hw'].insert(0, ' ')
        length = len(db['hagerty_hw'])
        if length > 1:
            if db['hagerty_hw'][0] == ' ':
                db['hagerty_hw'].remove(' ')
            embedVar = discord.Embed(title="Success",
                                     description=f"Hagerty's Homework Cleared",
                                     color=success)
            await message.channel.send(embed=embedVar)
            db["hagerty_hw"] = []
        else:
            embedVar = discord.Embed(
                title="Error",
                description=
                f"There is no homework to clear in Hagerty Homework",
                color=error)
            await message.channel.send(embed=embedVar)

    elif message.content.lower(
    ) == "?clear hagerty quizlet" or message.content.lower(
    ) == "?clear hagerty quizlets":
        try:
            if db['hagerty_study_quizlet'][0] == ' ':
                pass
        except:
            db['hagerty_study_quizlet'].insert(0, ' ')
        length = len(db['hagerty_study_quizlet'])
        if length > 1:
            if db['hagerty_study_quizlet'][0] == ' ':
                db['hagerty_study_quizlet'].remove(' ')
            embedVar = discord.Embed(
                title="Success",
                description=f"Hagerty's Study Quizlets Cleared",
                color=success)
            await message.channel.send(embed=embedVar)
            db["hagerty_study_quizlet"] = []
        else:
            embedVar = discord.Embed(
                title="Error",
                description=f"There are no Quizlets to clear in Hagerty Study",
                color=error)
            await message.channel.send(embed=embedVar)

    elif message.content.lower(
    ) == "?clear hagerty notes" or message.content.lower(
    ) == "?clear hagerty note":
        try:
            if db['hagerty_study_notes'][0] == ' ':
                pass
        except:
            db['hagerty_study_notes'].insert(0, ' ')
        length = len(db['hagerty_study_notes'])
        if length > 1:
            if db['hagerty_study_notes'][0] == ' ':
                db['hagerty_study_notes'].remove(' ')
            embedVar = discord.Embed(
                title="Success",
                description=f"Hagerty's Study Notes Cleared",
                color=success)
            await message.channel.send(embed=embedVar)
            db["hagerty_study_notes"] = []
        else:
            embedVar = discord.Embed(
                title="Error",
                description=f"There are no Notes to clear in Hagerty Study",
                color=error)
            await message.channel.send(embed=embedVar)

    elif message.content.lower(
    ) == "?clear hagerty other" or message.content.lower(
    ) == "?clear hagerty others":
        try:
            if db['hagerty_study_other'][0] == ' ':
                pass
        except:
            db['hagerty_study_other'].insert(0, ' ')
        length = len(db['hagerty_study_other'])
        if length > 1:
            if db['hagerty_study_other'][0] == ' ':
                db['hagerty_study_other'].remove(' ')
            embedVar = discord.Embed(
                title="Success",
                description=f"Hagerty's Study Other Cleared",
                color=success)
            await message.channel.send(embed=embedVar)
            db["hagerty_study_other"] = []
        else:
            embedVar = discord.Embed(
                title="Error",
                description=
                f"There are no 'Other' resources to clear in Hagerty Study",
                color=error)
            await message.channel.send(embed=embedVar)

    elif message.content.lower(
    ) == "?clear hagerty study" or message.content.lower(
    ) == "?clear hagerty studys" or message.content.lower(
    ) == "?clear hagerty studies":
        db['hagerty_study_other'] = []
        db['hagerty_study_quizlet'] = []
        db['hagerty_study_notes'] = []

        embedVar = discord.Embed(title="Success",
                                 description=f"Hagerty's Study Cleared",
                                 color=success)
        await message.channel.send(embed=embedVar)

    # Health Fullerton
    if message.content.startswith("?add fullerton test"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])

        db["fullerton_test"] = f"{' '.join(msg[1:])} | {msg[0]}"

        value = db["fullerton_test"]

        embedVar = discord.Embed(
            title="Success",
            description="The following test was added: '" +
            db["fullerton_test"] + "'",
            color=success)
        await message.channel.send(embed=embedVar)

    elif message.content.startswith(
        "?add fullerton hw") or message.content.startswith(
            "?add fullerton homework"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])

        db["fullerton_hw"].append(f"\n{' '.join(msg[1:])} | {msg[0]}")

        embedVar = discord.Embed(title="Homework Added",
                                 description="'" + ' '.join(msg[1:]) + " | " +
                                 msg[0] + "' added to Fullerton's Homework",
                                 color=success)
        await message.channel.send(embed=embedVar)
        embedVar = discord.Embed(title="Fullerton's Homework",
                                 description='\n'.join(db["fullerton_hw"]),
                                 color=pink)
        await message.channel.send(embed=embedVar)

    elif message.content.startswith("?add fullerton quizlet"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = "".join(msg)
        quizlet = db["fullerton_study_quizlet"]
        quizlet.append(msg)
        if quizlet[0] == "":
            quizlet.remove(quizlet[0])
        embedVar = discord.Embed(
            title="Success",
            description=
            f"Your Quizlet ({msg}) was succesfully added to 'Fullerton Study'",
            color=success)
        await message.channel.send(embed=embedVar)
        quizlet = '\n'.join(quizlet)
        notes = '\n'.join(db['fullerton_study_notes'])
        other = '\n'.join(db['fullerton_study_other'])
        embedVar = discord.Embed(
            title="Fullerton's Study",
            description=
            f"**Quizlets:**\n{quizlet}\n\n**Notes:**\n{notes}\n\n**Other:**\n{other}",
            color=pink)
        await message.channel.send(embed=embedVar)

    elif message.content.startswith("?add fullerton notes"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = "".join(msg)
        notes = db["fullerton_study_notes"]
        notes.append(msg)
        embedVar = discord.Embed(
            title="Success",
            description=
            f"Your notes ({msg}) were succesfully added to 'Fullerton Study'",
            color=success)
        await message.channel.send(embed=embedVar)
        quizlet = '\n'.join(db['fullerton_study_other'])
        notes = '\n'.join(db['fullerton_study_notes'])
        other = '\n'.join(db['fullerton_study_other'])
        embedVar = discord.Embed(
            title="Fullerton's Study",
            description=
            f"**Quizlets:**\n{quizlet}\n\n**Notes:**\n{notes}\n\n**Other:**\n{other}",
            color=pink)
        await message.channel.send(embed=embedVar)
    elif message.content.startswith("?add fullerton other"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = "".join(msg)
        other = db["fullerton_study_other"]
        other.append(msg)
        embedVar = discord.Embed(
            title="Success",
            description=
            f"Your resource ({msg}) was succesfully added to 'Fullerton Study'",
            color=success)
        quizlet = '\n'.join(db['fullerton_study_other'])
        notes = '\n'.join(db['fullerton_study_notes'])
        other = '\n'.join(db['fullerton_study_other'])
        embedVar = discord.Embed(
            title="Fullerton's Study",
            description=
            f"**Quizlets:**\n{quizlet}\n\n**Notes:**\n{notes}\n\n**Other:**\n{other}",
            color=pink)
        await message.channel.send(embed=embedVar)

    elif message.content.lower() == "?fullerton hw" or message.content.lower(
    ) == "?fullerton homework":
        embedVar = discord.Embed(title="Fullerton's Homework",
                                 description='\n'.join(db["fullerton_hw"]),
                                 color=pink)
        await message.channel.send(embed=embedVar)
    elif message.content.lower() == "?fullerton test":
        value = db["fullerton_test"]
        embedVar = discord.Embed(
            title="Fullerton's Test",
            description=f"Fullerton's next test is on: {value}",
            color=pink)
        await message.channel.send(embed=embedVar)

    elif message.content.lower() == "?fullerton study":
        quizlet = '\n'.join(db['fullerton_study_quizlet'])
        notes = '\n'.join(db['fullerton_study_notes'])
        other = '\n'.join(db['fullerton_study_other'])
        embedVar = discord.Embed(
            title="Fullerton's Study",
            description=
            f"**Quizlets:**\n{quizlet}\n\n**Notes:**\n{notes}\n\n**Other:**\n{other}",
            color=pink)
        await message.channel.send(embed=embedVar)

    elif message.content.lower() == (
        "?remove fullerton test"
    ) or message.content.lower() == "?clear fullerton test":
        try:
            if db['fullerton_test'][0] == ' ':
                pass
        except:
            db['fullerton_test'].insert(0, ' ')
        length = len(db['fullerton_test'])
        if length > 1:
            if db['fullerton_test'][0] == ' ':
                db['fullerton_test'].remove(' ')
            embedVar = discord.Embed(
                title="Success",
                description=
                f"Fullerton's Test {(db['fullerton_test'])} has been removed",
                color=success)
            await message.channel.send(embed=embedVar)
            db["fullerton_test"] = []
        else:
            embedVar = discord.Embed(
                title="Error",
                description=f"There is no test to remove in Fullerton Test",
                color=error)
            await message.channel.send(embed=embedVar)

    elif message.content.startswith(
        "?remove fullerton hw") or message.content.startswith(
            "?remove fullerton homework"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = msg[0]
        if len(db['fullerton_hw']) >= int(msg):
            embedVar = discord.Embed(
                title="Success",
                color=success,
                description=
                f"'{db['fullerton_hw'][(int(msg) - 1)]}' was succesfully removed from Fullerton Homework"
            )
            await message.channel.send(embed=embedVar)
            db['fullerton_hw'].remove(db['fullerton_hw'][(int(msg) - 1)])
        else:
            embedVar = discord.Embed(
                title="Error",
                color=error,
                description=f"Fullerton Homework 'Option {msg}' does not exist"
            )
            await message.channel.send(embed=embedVar)

    elif message.content.startswith(
        "?remove fullerton quizlet") or message.content.startswith(
            "?remove fullerton quizlets"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = msg[0]
        if len(db['fullerton_study_quizlet']) >= int(msg):
            embedVar = discord.Embed(
                title="Success",
                color=success,
                description=
                f"Quizlet '{db['fullerton_study_quizlet'][(int(msg) - 1)]}' was succesfully removed from Fullerton Study"
            )
            await message.channel.send(embed=embedVar)
            db['fullerton_study_quizlet'].remove(
                db['fullerton_study_quizlet'][(int(msg) - 1)])
        else:
            embedVar = discord.Embed(
                title="Error",
                color=error,
                description=
                f"Fullerton Study 'Option {msg}' does not exist in Quizlet")
            await message.channel.send(embed=embedVar)

    elif message.content.startswith(
        "?remove fullerton notes") or message.content.startswith(
            "?remove fullerton note"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = msg[0]
        if len(db['fullerton_study_notes']) >= int(msg):
            embedVar = discord.Embed(
                title="Success",
                color=success,
                description=
                f"Note '{db['fullerton_study_notes'][(int(msg) - 1)]}' was succesfully removed from Fullerton Study"
            )
            await message.channel.send(embed=embedVar)
            db['fullerton_study_notes'].remove(
                db['fullerton_study_notes'][(int(msg) - 1)])
        else:
            embedVar = discord.Embed(
                title="Error",
                color=error,
                description=
                f"Fullerton Study 'Option {msg}' does not exist in Notes")
            await message.channel.send(embed=embedVar)

    elif message.content.startswith("?remove fullerton other"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = msg[0]
        if len(db['fullerton_study_other']) >= int(msg):
            embedVar = discord.Embed(
                title="Success",
                color=success,
                description=
                f"Other '{db['fullerton_study_other'][(int(msg) - 1)]}' was succesfully removed from Fullerton Study"
            )
            await message.channel.send(embed=embedVar)
            db['fullerton_study_other'].remove(
                db['fullerton_study_other'][(int(msg) - 1)])
        else:
            embedVar = discord.Embed(
                title="Error",
                color=error,
                description=
                f"Fullerton Study 'Option {msg}' does not exist in Other")
            await message.channel.send(embed=embedVar)

    elif message.content.lower() == (
        "?clear fullerton hw"
    ) or message.content.lower() == "?clear fullerton homework":
        try:
            if db['fullerton_hw'][0] == ' ':
                pass
        except:
            db['fullerton_hw'].insert(0, ' ')
        length = len(db['fullerton_hw'])
        if length > 1:
            if db['fullerton_hw'][0] == ' ':
                db['fullerton_hw'].remove(' ')
            embedVar = discord.Embed(
                title="Success",
                description=f"Fullerton's Homework Cleared",
                color=success)
            await message.channel.send(embed=embedVar)
            db["fullerton_hw"] = []
        else:
            embedVar = discord.Embed(
                title="Error",
                description=
                f"There is no homework to clear in fullerton Homework",
                color=error)
            await message.channel.send(embed=embedVar)

    elif message.content.lower(
    ) == "?clear fullerton quizlet" or message.content.lower(
    ) == "?clear fullerton quizlets":
        try:
            if db['fullerton_study_quizlet'][0] == ' ':
                pass
        except:
            db['fullerton_study_quizlet'].insert(0, ' ')
        length = len(db['fullerton_study_quizlet'])
        if length > 1:
            if db['fullerton_study_quizlet'][0] == ' ':
                db['fullerton_study_quizlet'].remove(' ')
            embedVar = discord.Embed(
                title="Success",
                description=f"Fullerton's Study Quizlets Cleared",
                color=success)
            await message.channel.send(embed=embedVar)
            db["fullerton_study_quizlet"] = []
        else:
            embedVar = discord.Embed(
                title="Error",
                description=
                f"There are no Quizlets to clear in Fullerton Study",
                color=error)
            await message.channel.send(embed=embedVar)

    elif message.content.lower(
    ) == "?clear fullerton notes" or message.content.lower(
    ) == "?clear fullerton note":
        try:
            if db['fullerton_study_notes'][0] == ' ':
                pass
        except:
            db['fullerton_study_notes'].insert(0, ' ')
        length = len(db['fullerton_study_notes'])
        if length > 1:
            if db['fullerton_study_notes'][0] == ' ':
                db['fullerton_study_notes'].remove(' ')
            embedVar = discord.Embed(
                title="Success",
                description=f"Fullerton's Study Notes Cleared",
                color=success)
            await message.channel.send(embed=embedVar)
            db["fullerton_study_notes"] = []
        else:
            embedVar = discord.Embed(
                title="Error",
                description=f"There are no Notes to clear in Fullerton Study",
                color=error)
            await message.channel.send(embed=embedVar)

    elif message.content.lower(
    ) == "?clear fullerton other" or message.content.lower(
    ) == "?clear fullerton others":
        try:
            if db['fullerton_study_other'][0] == ' ':
                pass
        except:
            db['fullerton_study_other'].insert(0, ' ')
        length = len(db['fullerton_study_other'])
        if length > 1:
            if db['fullerton'][0] == ' ':
                db['fullerton_study_other'].remove(' ')
            embedVar = discord.Embed(
                title="Success",
                description=f"Fullerton's Study Other Cleared",
                color=success)
            await message.channel.send(embed=embedVar)
            db["fullerton_study_other"] = []
        else:
            embedVar = discord.Embed(
                title="Error",
                description=
                f"There are no 'Other' resources to clear in Fullerton Study",
                color=error)
            await message.channel.send(embed=embedVar)

    elif message.content.lower(
    ) == "?clear fullerton study" or message.content.lower(
    ) == "?clear fullerton studys" or message.content.lower(
    ) == "?clear fullerton studies":
        db['fullerton_study_other'] = []
        db['fullerton_study_quizlet'] = []
        db['fullerton_study_notes'] = []

        embedVar = discord.Embed(title="Success",
                                 description=f"Fullerton's Study Cleared",
                                 color=success)
        await message.channel.send(embed=embedVar)

    if message.content.startswith("?add torre test"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])

        db["torre_test"] = f"{' '.join(msg[1:])} | {msg[0]}"

        value = db["torre_test"]

        embedVar = discord.Embed(
            title="Success",
            description="The following test was added: '" + db["torre_test"] +
            "'",
            color=success)
        await message.channel.send(embed=embedVar)

    # De La Torre Spanish
    elif message.content.startswith(
        "?add torre hw") or message.content.startswith("?add torre homework"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])

        db["torre_hw"].append(f"\n{' '.join(msg[1:])} | {msg[0]}")

        embedVar = discord.Embed(title="Homework Added",
                                 description="'" + ' '.join(msg[1:]) + " | " +
                                 msg[0] + "' added to Torre's Homework",
                                 color=success)
        await message.channel.send(embed=embedVar)
        embedVar = discord.Embed(title="Torre's Homework",
                                 description='\n'.join(db["torre_hw"]),
                                 color=teal)
        await message.channel.send(embed=embedVar)

    elif message.content.startswith("?add torre quizlet"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = "".join(msg)
        quizlet = db["torre_study_quizlet"]
        quizlet.append(msg)
        if quizlet[0] == "":
            quizlet.remove(quizlet[0])
        embedVar = discord.Embed(
            title="Success",
            description=
            f"Your Quizlet ({msg}) was succesfully added to 'Torre Study'",
            color=success)
        await message.channel.send(embed=embedVar)
        quizlet = '\n'.join(quizlet)
        notes = '\n'.join(db['torre_study_notes'])
        other = '\n'.join(db['torre_study_other'])
        embedVar = discord.Embed(
            title="Torre's Study",
            description=
            f"**Quizlets:**\n{quizlet}\n\n**Notes:**\n{notes}\n\n**Other:**\n{other}",
            color=teal)
        await message.channel.send(embed=embedVar)

    elif message.content.startswith("?add torre notes"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = "".join(msg)
        notes = db["torre_study_notes"]
        notes.append(msg)
        embedVar = discord.Embed(
            title="Success",
            description=
            f"Your notes ({msg}) were succesfully added to 'Torre Study'",
            color=success)
        await message.channel.send(embed=embedVar)
        quizlet = '\n'.join(db['torre_study_other'])
        notes = '\n'.join(db['torre_study_notes'])
        other = '\n'.join(db['torre_study_other'])
        embedVar = discord.Embed(
            title="Torre's Study",
            description=
            f"**Quizlets:**\n{quizlet}\n\n**Notes:**\n{notes}\n\n**Other:**\n{other}",
            color=teal)
        await message.channel.send(embed=embedVar)
    elif message.content.startswith("?add torre other"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = "".join(msg)
        other = db["torre_study_other"]
        other.append(msg)
        embedVar = discord.Embed(
            title="Success",
            description=
            f"Your resource ({msg}) was succesfully added to 'Torre Study'",
            color=success)
        quizlet = '\n'.join(db['torre_study_other'])
        notes = '\n'.join(db['torre_study_notes'])
        other = '\n'.join(db['torre_study_other'])
        embedVar = discord.Embed(
            title="Torre's Study",
            description=
            f"**Quizlets:**\n{quizlet}\n\n**Notes:**\n{notes}\n\n**Other:**\n{other}",
            color=teal)
        await message.channel.send(embed=embedVar)

    elif message.content.lower() == "?torre hw" or message.content.lower(
    ) == "?torre homework":
        embedVar = discord.Embed(title="Torre's Homework",
                                 description='\n'.join(db["torre_hw"]),
                                 color=teal)
        await message.channel.send(embed=embedVar)
    elif message.content.lower() == "?torre test":
        value = db["torre_test"]
        embedVar = discord.Embed(
            title="Torre's Test",
            description=f"Torre's next test is on: {value}",
            color=teal)
        await message.channel.send(embed=embedVar)

    elif message.content.lower() == "?torre study":
        quizlet = '\n'.join(db['torre_study_quizlet'])
        notes = '\n'.join(db['torre_study_notes'])
        other = '\n'.join(db['torre_study_other'])
        embedVar = discord.Embed(
            title="Torre's Study",
            description=
            f"**Quizlets:**\n{quizlet}\n\n**Notes:**\n{notes}\n\n**Other:**\n{other}",
            color=teal)
        await message.channel.send(embed=embedVar)

    elif message.content.lower() == (
        "?remove torre test"
    ) or message.content.lower() == "?clear torre test":
        try:
            if db['torre_test'][0] == ' ':
                pass
        except:
            db['torre_test'].insert(0, ' ')
        length = len(db['torre_test'])
        if length > 1:
            if db['torre_test'][0] == ' ':
                db['torre_test'].remove(' ')
            embedVar = discord.Embed(
                title="Success",
                description=
                f"Torre's Test {(db['torre_test'])} has been removed",
                color=success)
            await message.channel.send(embed=embedVar)
            db["torre_test"] = []
        else:
            embedVar = discord.Embed(
                title="Error",
                description=f"There is no test to remove in Torre Test",
                color=error)
            await message.channel.send(embed=embedVar)

    elif message.content.startswith(
        "?remove torre hw") or message.content.startswith(
            "?remove torre homework"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = msg[0]
        if len(db['torre_hw']) >= int(msg):
            embedVar = discord.Embed(
                title="Success",
                color=success,
                description=
                f"'{db['torre_hw'][(int(msg) - 1)]}' was succesfully removed from Torre Homework"
            )
            await message.channel.send(embed=embedVar)
            db['torre_hw'].remove(db['torre_hw'][(int(msg) - 1)])
        else:
            embedVar = discord.Embed(
                title="Error",
                color=error,
                description=f"Torre Homework 'Option {msg}' does not exist")
            await message.channel.send(embed=embedVar)

    elif message.content.startswith(
        "?remove torre quizlet") or message.content.startswith(
            "?remove torre quizlets"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = msg[0]
        if len(db['torre_study_quizlet']) >= int(msg):
            embedVar = discord.Embed(
                title="Success",
                color=success,
                description=
                f"Quizlet '{db['torre_study_quizlet'][(int(msg) - 1)]}' was succesfully removed from Torre Study"
            )
            await message.channel.send(embed=embedVar)
            db['torre_study_quizlet'].remove(
                db['torre_study_quizlet'][(int(msg) - 1)])
        else:
            embedVar = discord.Embed(
                title="Error",
                color=error,
                description=
                f"Torre Study 'Option {msg}' does not exist in Quizlet")
            await message.channel.send(embed=embedVar)

    elif message.content.startswith(
        "?remove torre notes") or message.content.startswith(
            "?remove torre note"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = msg[0]
        if len(db['torre_study_notes']) >= int(msg):
            embedVar = discord.Embed(
                title="Success",
                color=success,
                description=
                f"Note '{db['torre_study_notes'][(int(msg) - 1)]}' was succesfully removed from Torre Study"
            )
            await message.channel.send(embed=embedVar)
            db['torre_study_notes'].remove(db['torre_study_notes'][(int(msg) -
                                                                    1)])
        else:
            embedVar = discord.Embed(
                title="Error",
                color=error,
                description=
                f"Torre Study 'Option {msg}' does not exist in Notes")
            await message.channel.send(embed=embedVar)

    elif message.content.startswith("?remove torre other"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = msg[0]
        if len(db['torre_study_other']) >= int(msg):
            embedVar = discord.Embed(
                title="Success",
                color=success,
                description=
                f"Other '{db['torre_study_other'][(int(msg) - 1)]}' was succesfully removed from Torre Study"
            )
            await message.channel.send(embed=embedVar)
            db['torre_study_other'].remove(db['torre_study_other'][(int(msg) -
                                                                    1)])
        else:
            embedVar = discord.Embed(
                title="Error",
                color=error,
                description=
                f"Torre Study 'Option {msg}' does not exist in Other")
            await message.channel.send(embed=embedVar)

    elif message.content.lower() == (
        "?clear torre hw"
    ) or message.content.lower() == "?clear torre homework":
        try:
            if db['torre_hw'][0] == ' ':
                pass
        except:
            db['torre_hw'].insert(0, ' ')
        length = len(db['torre_hw'])
        if length > 1:
            if db['torre_hw'][0] == ' ':
                db['torre_hw'].remove(' ')
            embedVar = discord.Embed(title="Success",
                                     description=f"Torre's Homework Cleared",
                                     color=success)
            await message.channel.send(embed=embedVar)
            db["torre_hw"] = []
        else:
            embedVar = discord.Embed(
                title="Error",
                description=f"There is no homework to clear in Torre Homework",
                color=error)
            await message.channel.send(embed=embedVar)

    elif message.content.lower(
    ) == "?clear torre quizlet" or message.content.lower(
    ) == "?clear torre quizlets":
        try:
            if db['torre_study_quizlet'][0] == ' ':
                pass
        except:
            db['torre_study_quizlet'].insert(0, ' ')
        length = len(db['torre_study_quizlet'])
        if length > 1:
            if db['torre_study_quizlet'][0] == ' ':
                db['torre_study_quizlet'].remove(' ')
            embedVar = discord.Embed(
                title="Success",
                description=f"Torre's Study Quizlets Cleared",
                color=success)
            await message.channel.send(embed=embedVar)
            db["torre_study_quizlet"] = []
        else:
            embedVar = discord.Embed(
                title="Error",
                description=f"There are no Quizlets to clear in Torre Study",
                color=error)
            await message.channel.send(embed=embedVar)

    elif message.content.lower(
    ) == "?clear torre notes" or message.content.lower(
    ) == "?clear torre note":
        try:
            if db['torre_study_notes'][0] == ' ':
                pass
        except:
            db['torre_study_notes'].insert(0, ' ')
        length = len(db['torre_study_notes'])
        if length > 1:
            if db['torre_study_notes'][0] == ' ':
                db['torre_study_notes'].remove(' ')
            embedVar = discord.Embed(
                title="Success",
                description=f"Torre's Study Notes Cleared",
                color=success)
            await message.channel.send(embed=embedVar)
            db["torre_study_notes"] = []
        else:
            embedVar = discord.Embed(
                title="Error",
                description=f"There are no Notes to clear in Torre Study",
                color=error)
            await message.channel.send(embed=embedVar)

    elif message.content.lower(
    ) == "?clear torre other" or message.content.lower(
    ) == "?clear torre others":
        try:
            if db['torre_study_other'][0] == ' ':
                pass
        except:
            db['torrer_study_other'].insert(0, ' ')
        length = len(db['torre_study_other'])
        if length > 1:
            if db['torre_study_other'][0] == ' ':
                db['torre_study_other'].remove(' ')
            embedVar = discord.Embed(
                title="Success",
                description=f"Torre's Study Other Cleared",
                color=success)
            await message.channel.send(embed=embedVar)
            db["torre_study_other"] = []
        else:
            embedVar = discord.Embed(
                title="Error",
                description=
                f"There are no 'Other' resources to clear in Torre Study",
                color=error)
            await message.channel.send(embed=embedVar)

    elif message.content.lower(
    ) == "?clear torre study" or message.content.lower(
    ) == "?clear torre studys" or message.content.lower(
    ) == "?clear torre studies":
        db['torre_study_other'] = []
        db['torre_study_quizlet'] = []
        db['torre_study_notes'] = []

        embedVar = discord.Embed(title="Success",
                                 description=f"Torre's Study Cleared",
                                 color=success)
        await message.channel.send(embed=embedVar)

    # Simons Science
    if message.content.startswith("?add simons test"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])

        db["simons_test"] = f"{' '.join(msg[1:])} | {msg[0]}"

        value = db["simons_test"]

        embedVar = discord.Embed(
            title="Success",
            description="The following test was added: '" + db["simons_test"] +
            "'",
            color=success)
        await message.channel.send(embed=embedVar)

    elif message.content.startswith(
        "?add simons hw") or message.content.startswith(
            "?add simons homework"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])

        db["simons_hw"].append(f"\n{' '.join(msg[1:])} | {msg[0]}")

        embedVar = discord.Embed(title="Homework Added",
                                 description="'" + ' '.join(msg[1:]) + " | " +
                                 msg[0] + "' added to Simons's Homework",
                                 color=success)
        await message.channel.send(embed=embedVar)
        embedVar = discord.Embed(title="Simons's Homework",
                                 description='\n'.join(db["simons_hw"]),
                                 color=green)
        await message.channel.send(embed=embedVar)

    elif message.content.startswith("?add simons quizlet"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = "".join(msg)
        quizlet = db["simons_study_quizlet"]
        quizlet.append(msg)
        if quizlet[0] == "":
            quizlet.remove(quizlet[0])
        embedVar = discord.Embed(
            title="Success",
            description=
            f"Your Quizlet ({msg}) was succesfully added to 'Simons Study'",
            color=success)
        await message.channel.send(embed=embedVar)
        quizlet = '\n'.join(quizlet)
        notes = '\n'.join(db['simons_study_notes'])
        other = '\n'.join(db['simons_study_other'])
        embedVar = discord.Embed(
            title="Simons's Study",
            description=
            f"**Quizlets:**\n{quizlet}\n\n**Notes:**\n{notes}\n\n**Other:**\n{other}",
            color=green)
        await message.channel.send(embed=embedVar)

    elif message.content.startswith("?add simons notes"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = "".join(msg)
        notes = db["simons_study_notes"]
        notes.append(msg)
        embedVar = discord.Embed(
            title="Success",
            description=
            f"Your notes ({msg}) were succesfully added to 'Simons Study'",
            color=success)
        await message.channel.send(embed=embedVar)
        quizlet = '\n'.join(db['simons_study_other'])
        notes = '\n'.join(db['simons_study_notes'])
        other = '\n'.join(db['simons_study_other'])
        embedVar = discord.Embed(
            title="Simons's Study",
            description=
            f"**Quizlets:**\n{quizlet}\n\n**Notes:**\n{notes}\n\n**Other:**\n{other}",
            color=green)
        await message.channel.send(embed=embedVar)
    elif message.content.startswith("?add simons other"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = "".join(msg)
        other = db["simons_study_other"]
        other.append(msg)
        embedVar = discord.Embed(
            title="Success",
            description=
            f"Your resource ({msg}) was succesfully added to 'Simons Study'",
            color=success)
        quizlet = '\n'.join(db['simons_study_other'])
        notes = '\n'.join(db['simons_study_notes'])
        other = '\n'.join(db['simons_study_other'])
        embedVar = discord.Embed(
            title="Simons's Study",
            description=
            f"**Quizlets:**\n{quizlet}\n\n**Notes:**\n{notes}\n\n**Other:**\n{other}",
            color=green)
        await message.channel.send(embed=embedVar)

    elif message.content.lower() == "?simons hw" or message.content.lower(
    ) == "?simons homework":
        embedVar = discord.Embed(title="Simons's Homework",
                                 description='\n'.join(db["simons_hw"]),
                                 color=green)
        await message.channel.send(embed=embedVar)
    elif message.content.lower() == "?simons test":
        value = db["simons_test"]
        embedVar = discord.Embed(
            title="Simons's Test",
            description=f"Simons's next test is on: {value}",
            color=green)
        await message.channel.send(embed=embedVar)

    elif message.content.lower() == "?simons study":
        quizlet = '\n'.join(db['simons_study_quizlet'])
        notes = '\n'.join(db['simons_study_notes'])
        other = '\n'.join(db['simons_study_other'])
        embedVar = discord.Embed(
            title="Simons's Study",
            description=
            f"**Quizlets:**\n{quizlet}\n\n**Notes:**\n{notes}\n\n**Other:**\n{other}",
            color=green)
        await message.channel.send(embed=embedVar)

    elif message.content.lower() == (
        "?remove simons test"
    ) or message.content.lower() == "?clear simons test":
        try:
            if db['simons_test'][0] == ' ':
                pass
        except:
            db['simons_test'].insert(0, ' ')
        length = len(db['simons_test'])
        if length > 1:
            if db['simons_test'][0] == ' ':
                db['simons_test'].remove(' ')
            embedVar = discord.Embed(
                title="Success",
                description=
                f"Simons's Test {(db['simons_test'])} has been removed",
                color=success)
            await message.channel.send(embed=embedVar)
            db["simons_test"] = []
        else:
            embedVar = discord.Embed(
                title="Error",
                description=f"There is no test to remove in Simons Test",
                color=error)
            await message.channel.send(embed=embedVar)

    elif message.content.startswith(
        "?remove simons hw") or message.content.startswith(
            "?remove simons homework"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = msg[0]
        if len(db['simons_hw']) >= int(msg):
            embedVar = discord.Embed(
                title="Success",
                color=success,
                description=
                f"'{db['simons_hw'][(int(msg) - 1)]}' was succesfully removed from Simons Homework"
            )
            await message.channel.send(embed=embedVar)
            db['simons_hw'].remove(db['simons_hw'][(int(msg) - 1)])
        else:
            embedVar = discord.Embed(
                title="Error",
                color=error,
                description=f"Simons Homework 'Option {msg}' does not exist")
            await message.channel.send(embed=embedVar)

    elif message.content.startswith(
        "?remove simons quizlet") or message.content.startswith(
            "?remove simons quizlets"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = msg[0]
        if len(db['simons_study_quizlet']) >= int(msg):
            embedVar = discord.Embed(
                title="Success",
                color=success,
                description=
                f"Quizlet '{db['simons_study_quizlet'][(int(msg) - 1)]}' was succesfully removed from Simons Study"
            )
            await message.channel.send(embed=embedVar)
            db['simons_study_quizlet'].remove(
                db['simons_study_quizlet'][(int(msg) - 1)])
        else:
            embedVar = discord.Embed(
                title="Error",
                color=error,
                description=
                f"Simons Study 'Option {msg}' does not exist in Quizlet")
            await message.channel.send(embed=embedVar)

    elif message.content.startswith(
        "?remove simons notes") or message.content.startswith(
            "?remove simons note"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = msg[0]
        if len(db['simons_study_notes']) >= int(msg):
            embedVar = discord.Embed(
                title="Success",
                color=success,
                description=
                f"Note '{db['simons_study_notes'][(int(msg) - 1)]}' was succesfully removed from Simons Study"
            )
            await message.channel.send(embed=embedVar)
            db['simons_study_notes'].remove(
                db['simons_study_notes'][(int(msg) - 1)])
        else:
            embedVar = discord.Embed(
                title="Error",
                color=error,
                description=
                f"Simons Study 'Option {msg}' does not exist in Notes")
            await message.channel.send(embed=embedVar)

    elif message.content.startswith("?remove simons other"):
        msg = message.content.split()
        for _ in range(3):
            msg.remove(msg[0])
        msg = msg[0]
        if len(db['simons_study_other']) >= int(msg):
            embedVar = discord.Embed(
                title="Success",
                color=success,
                description=
                f"Other '{db['simons_study_other'][(int(msg) - 1)]}' was succesfully removed from Simons Study"
            )
            await message.channel.send(embed=embedVar)
            db['simons_study_other'].remove(
                db['simons_study_other'][(int(msg) - 1)])
        else:
            embedVar = discord.Embed(
                title="Error",
                color=error,
                description=
                f"Simons Study 'Option {msg}' does not exist in Other")
            await message.channel.send(embed=embedVar)

    elif message.content.lower() == (
        "?clear simons hw"
    ) or message.content.lower() == "?clear simons homework":
        try:
            if db['simons_hw'][0] == ' ':
                pass
        except:
            db['simons_hw'].insert(0, ' ')
        length = len(db['simons_hw'])
        if length > 1:
            if db['simons_hw'][0] == ' ':
                db['simons_hw'].remove(' ')
            embedVar = discord.Embed(title="Success",
                                     description=f"Simons's Homework Cleared",
                                     color=success)
            await message.channel.send(embed=embedVar)
            db["simons_hw"] = []
        else:
            embedVar = discord.Embed(
                title="Error",
                description=f"There is no homework to clear in Simons Homework",
                color=error)
            await message.channel.send(embed=embedVar)

    elif message.content.lower(
    ) == "?clear simons quizlet" or message.content.lower(
    ) == "?clear simons quizlets":
        try:
            if db['simons_study_quizlet'][0] == ' ':
                pass
        except:
            db['simons_study_quizlet'].insert(0, ' ')
        length = len(db['simons_study_quizlet'])
        if length > 1:
            if db['simons_study_quizlet'][0] == ' ':
                db['simons_study_quizlet'].remove(' ')
            embedVar = discord.Embed(
                title="Success",
                description=f"Simons's Study Quizlets Cleared",
                color=success)
            await message.channel.send(embed=embedVar)
            db["simons_study_quizlet"] = []
        else:
            embedVar = discord.Embed(
                title="Error",
                description=f"There are no Quizlets to clear in Simons Study",
                color=error)
            await message.channel.send(embed=embedVar)

    elif message.content.lower(
    ) == "?clear simons notes" or message.content.lower(
    ) == "?clear simons note":
        try:
            if db['simons_study_notes'][0] == ' ':
                pass
        except:
            db['simons_study_notes'].insert(0, ' ')
        length = len(db['simons_study_notes'])
        if length > 1:
            if db['simons_study_notes'][0] == ' ':
                db['simons_study_notes'].remove(' ')
            embedVar = discord.Embed(
                title="Success",
                description=f"Simons's Study Notes Cleared",
                color=success)
            await message.channel.send(embed=embedVar)
            db["simons_study_notes"] = []
        else:
            embedVar = discord.Embed(
                title="Error",
                description=f"There are no Notes to clear in Simons Study",
                color=error)
            await message.channel.send(embed=embedVar)

    elif message.content.lower(
    ) == "?clear simons other" or message.content.lower(
    ) == "?clear simons others":
        try:
            if db['simons_study_other'][0] == ' ':
                pass
        except:
            db['simons_study_other'].insert(0, ' ')
        length = len(db['simons_study_other'])
        if length > 1:
            if db['simons_study_other'][0] == ' ':
                db['simons_study_other'].remove(' ')
            embedVar = discord.Embed(
                title="Success",
                description=f"Simons's Study Other Cleared",
                color=success)
            await message.channel.send(embed=embedVar)
            db["simons_study_other"] = []
        else:
            embedVar = discord.Embed(
                title="Error",
                description=
                f"There are no 'Other' resources to clear in Simons Study",
                color=error)
            await message.channel.send(embed=embedVar)

    elif message.content.lower(
    ) == "?clear simons study" or message.content.lower(
    ) == "?clear simons studys" or message.content.lower(
    ) == "?clear simons studies":
        db['simons_study_other'] = []
        db['simons_study_quizlet'] = []
        db['simons_study_notes'] = []

        embedVar = discord.Embed(title="Success",
                                 description=f"Simons's Study Cleared",
                                 color=success)
        await message.channel.send(embed=embedVar)


# TODO: add statements to control the amount of arguments on the remove statements
# there should only be one extra, which is just the option number.

# super idol
    if message.content.lower() == "?super_idol" or message.content.lower(
    ) == "?super idol":
        await message.channel.send(
            'https://cdn.discordapp.com/attachments/910784334984802325/911124716138397747/super_idol.mp4'
        )
        await message.channel.send(
            'https://media.discordapp.net/attachments/910343377604722778/911106976719724564/unknown.png?width=198&height=146'
        )

    # whitey pizza
    if message.content.lower() == "?costco" or message.content.lower(
    ) == "?pizza" or "pizza" in message.content.lower().split():
        embedVar = discord.Embed(
            title="BREAKTHROUGH!!",
            description=
            "EVERYONE, I found a breakthrough. I have found a way to get rid of the greasiness from Costco pizza and make it more delicious. First you buy the pizza and leave it out until it gets to room temp (I left mine in the box overnight). Next day I took 2 slices, and airfried them until you see a slight darkening (blackness) on the pizza. If it looks burnt don’t worry it’s normal to look that way. Then, eat. A pizza that doesn’t sweat grease but only produces a small amount of it, and has melty cheese and a delicious taste\n\t- Whitey",
            color=success)
        await message.channel.send(embed=embedVar)

    # laugh.mp4
    if message.content.lower() == "?laugh":
        await message.channel.send(
            "https://cdn.discordapp.com/attachments/680928395399266314/851702440625438741/lol-1.mp4"
        )

    # dance.mp4
    if message.content.lower() == "?dance":
        await message.channel.send(
            "https://cdn.discordapp.com/attachments/874447411144171610/875769944225222706/video1.mp4"
        )

    # mini_motorways free
    if message.content.lower() == "?mini_motorways" or message.content.lower(
    ) == "?mini motorways" or message.content.lower(
    ) == "?mini motorway" or message.content.lower() == "?mini_motorway":
        await message.author.send(
            "Here's a quick preview of the game:\nhttps://media.discordapp.net/attachments/742932318137876615/912959901519732766/header.png\nhttps://media.discordapp.net/attachments/742932318137876615/912960033548025886/ss_a4db48bc510aa79f01147e1137d1137143b2ca6d.png?width=1014&height=676\nhttps://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DRHX0CfcgOas&psig=AOvVaw24j9YS5dshtdsf9VyKAZ-A&ust=1637823426180000&source=images&cd=vfe&ved=0CA0Q3YkBahcKEwiAxKXttbD0AhUAAAAAHQAAAAAQCQ"
        )
        await message.author.send(
            "**If you're interested, you can download Mini Motorways for free here:** https://drive.google.com/uc?export=download&id=15I4qy5tUCJLdULv0z-6gPZbplaIpuisR"
        )
        embedVar = discord.Embed(
            title="Success",
            color=success,
            description="Mini Motorways preview sent to direct messages")
        await message.channel.send(embed=embedVar)

    # ronaldo drinking cheers
    if "cheers" in message.content.lower():
        await message.channel.send("https://cdn.discordapp.com/attachments/742932318137876615/913186339942445086/ronaldo.mp4")

    # baby escape arab music
    if message.content.lower() == "?baby":
      await message.channel.send("https://cdn.discordapp.com/attachments/742932318137876615/913199703699632208/escape.mp4")
    
    # my website
    if message.content.lower() == "?web" or message.content.lower() == "?website":
      await message.channel.send("https://sites.google.com/view/downloadmystuff/home")

    if message.content.lower() == "?beatkill" or message.content.lower() == "?kill" or message.content.lower() == "?kid" or message.content.lower() == "?kick" or message.content.lower() == "?child":
      await message.channel.send("https://cdn.discordapp.com/attachments/742932318137876615/913560066328768542/beatkill.mp4")
    
    # spam func
    if message.content.startswith("?spam"):
      msg = message.content.lower()
      msg = msg.split()
      id_input = msg[1]
      user = await client.fetch_user(id_input)
      for i in range(10):
        await user.send("What the fuck did you just fucking say about me, you little bitch? I'll have you know I graduated top of my class in the Navy Seals, and I've been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I'm the top sniper in the entire US armed forces. You are nothing to me but just another target. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You're fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that's just with my bare hands. Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little 'clever' comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn't, you didn't, and now you're paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You're fucking dead, kiddo.")
        embedVar = discord.Embed(title="Success", color=success, description="Message sent to user '{}'".format(str(id_input)))
      await message.channel.send(embed=embedVar)
    
    # polish cow trap remix
    if message.content.lower() == "?polish cow" or message.content.lower() == "?polish_cow" or message.content.lower() == "?polish" or message.content.lower() == "?trap" or message.content.lower() == "?polska":
      msg = 'https://cdn.discordapp.com/attachments/742932318137876615/914304482794418226/polish_cow_trap_remix.mp4'
      await message.channel.send(msg)

    if message.content.lower() == '?night':
      msg = 'https://cdn.discordapp.com/attachments/742932318137876615/918035868231565352/Dominic_Fike_3Nights.mp4'
      await message.channel.send(msg)
    
    if "ws" == message.content.lower() or "website" == message.content.lower():
      await message.channel.send('ADD WEBSITE HERE')
    
    if message.content.lower() == "?help":
      msg = "__<> is a required arg, | means 'or'__\n\n**Check Test:** ?<teacher> test\n\n**Check Homework:** ?<teacher> <homework | hw>\n\n**Check Study Resources:**?<teacher> study\n\n**Add Test:** ?add <teacher> test <date> <test name>\n\n**Add Homework:** ?add <teacher> <homework | hw> <date> <name>\n\n**Add Quizlet:** ?add <teacher> quizlet <link>\n\n**Add Notes:** ?add <teacher> notes <note content>\n\n**Add Other Resource:** ?add <teacher> other <resource content>\n\n**Remove Test:** ?remove <teacher> test\n\n**Remove Homework:** ?remove <teacher> <homework | hw> <option number>\n\n**Remove Quizlet:** ?remove <teacher> quizlet <option number>\n\n**Remove Notes:** ?remove <teacher> notes <option number>\n\n**Remove 'Other' Resource:** ?remove <teacher> other <option number>\n\n**Clear Test:** ?clear <teacher> test\n\n**Clear Homework:** ?clear <teacher> <homework | hw>\n\n**Clear Study:** ?clear <teacher> <study | quizlet | notes | other>\n\n**Generate Channel Transcript:** ?<transcript | trans>\n\n**Clear Messages:** ?clear <amount>"
      embedVar = discord.Embed(title="BlueBerry Help", color=yellow, description=msg)
      await message.channel.send(embed=embedVar)

    if message.content.lower() == "?transcribe" or message.content.lower() == "?trans":
      transcript = f"{message.channel.name}.txt"
      with open(transcript, "w") as file:
        async for msg in message.channel.history(limit=None):
          file.write(f"{msg.created_at} - {msg.author.display_name}: {msg.clean_content}\n")
      file = discord.File(transcript)
      await message.channel.send(file=file)
    
    if message.content.startswith('?clear'):
      msg = message.content.split()
      await message.delete()
      amount = int(msg[1])
      await message.channel.purge(limit=amount)

to_import()
client.run(environ['TOKEN'])
