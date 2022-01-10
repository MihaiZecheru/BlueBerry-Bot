import discord
from os import environ
from replit import db
from webserver import to_import

yellow = 0xF3FF00
success = 0x0adb23
error = 0xdb0a0a

def reset_testingDB():
  del db['members_Wop']
  del db['ids_Wop']
  del db['admins_Wop']

def Sort_by_pointsNum(parent_list: list): 
  parent_list.sort(key = lambda x: x[1], reverse=True) 
  return parent_list

intents = discord.Intents.all()
client = discord.Client(intents=intents)

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

    async def leaderboard():
      # get list of all server members based on score
      member_info = []
      keys = db[f'members_{server_name}'].keys()
      for key in keys:
        name = key
        score = db[f'members_{server_name}'][key]
        member_info.append([name, score])
      # put all members into descending order by points
      member_info = Sort_by_pointsNum(member_info)
      # get leaderboard
      body = ''
      for member in member_info:
        name = member[0]
        score = member[1]
        body += f'**{name}**: {score}\n'
      # send leaderboard
      await message.channel.send(embed=discord.Embed(title='{} Leaderboard'.format(server_name), description=body, color=yellow))

    try:
      # get server info
      admins = []
      all_members = message.guild.members
      server_name = message.guild.name.replace(" ", "_")
      user_ids = []
      for member in all_members:
        if not member.bot:
          user_ids.append(member.id)
      id_to_name_dict = {}
      for member in all_members:
        if not member.bot:
          id_to_name_dict[member.id] = member.name
      # see if dict exists
      _ = db[f'members_{server_name}']
    except Exception as e:
      print(e)
      members_dict = {}
      id_to_name_dict = {}

      for user in all_members:
        if not user.bot:
          members_dict[user.name] = 0
          id_to_name_dict[user.id] = user.name
      db[f'members_{server_name}'] = members_dict
      db[f'ids_{server_name}'] = id_to_name_dict
      db[f'admins_{server_name}'] = [549456138698227712]

    if message.content.lower() == '!lb':
      await leaderboard()

    if message.content.startswith('!thanks'):
      parsed_msg = message.content.split()
      user = parsed_msg[1]
      if user.startswith('<@!'):
        user_id = int(user[3:-1])
        if user_id != message.author.id:
          if user_id in user_ids:
            # get username
            username = id_to_name_dict.get(user_id)
            # add one point
            db[f'members_{server_name}'][username] += 1
            # tell user it worked
            await message.channel.send(embed=discord.Embed(description='Added 1 point to {}'.format(username), color=success))
          else:
            await message.channel.send(embed=discord.Embed(title='Invalid User', description='{} is not in server'.format(f'<@!{user_id}>'), color=error))
        else:
          await message.channel.send(embed=discord.Embed(description="You can't give points to yourself", color=error))
    elif message.content.startswith('?reset'):
      msg = message.content.split()
      victim = msg[1]
      if victim.startswith('<@!'):
        victim_id = int(victim[3:-1])
        if message.author.id in db[f'admins_{server_name}']:
          if victim_id in id_to_name_dict.keys():
            # get username
            username = id_to_name_dict.get(victim_id)
            # reset points
            db[f'members_{server_name}'][username] = 0
            await message.channel.send(embed=discord.Embed(color=success, description="Reset points for {}".format(username)))
            await leaderboard()
          else:
            await message.channel.send(embed=discord.Embed(color=error, description="You can't reset the points of a bot"))
        else:
          await message.channel.send(embed=discord.Embed(color=error, description="You can't use this command"))
      else:
        if victim == 'all':
          if message.author.id in db[f'admins_{server_name}']:
            # reset points
            for member_id in id_to_name_dict.keys():
              db[f'members_{server_name}'][id_to_name_dict[member_id]] = 0
            await message.channel.send(embed=discord.Embed(color=success, description="Reset points for all members"))
            await leaderboard()
          else:
            await message.channel.send(embed=discord.Embed(color=error, description="You can't use this command"))
        else:
          await message.channel.send(embed=discord.Embed(color=error, description="Command format: ?reset <@user | all>"))
    elif message.content.startswith("?remove"):
      msg = message.content.split()
      try:
        victim = msg[1]
        amount = msg[2]
        proceed = True
      except:
        await message.channel.send(embed=discord.Embed(color=error, description="Command format: ?remove @user <amount: int>"))
        proceed = False
      if proceed:
        if victim.startswith('<@!'):
          victim_id = int(victim[3:-1])
          if amount.isdigit():
            if int(amount) > 0:
              if message.author.id in db[f'admins_{server_name}']:
                if victim_id in id_to_name_dict.keys():
                  # get username
                  username = id_to_name_dict.get(victim_id)
                  # remove points
                  if int(amount) > db[f'members_{server_name}'][username]:
                    previous_value = db[f'members_{server_name}'][username]
                    db[f'members_{server_name}'][username] = 0
                    await message.channel.send(embed=discord.Embed(color=success, description="Removed {} from {}".format(previous_value, username)))
                    await leaderboard()
                  else:
                    db[f'members_{server_name}'][username] -= int(amount)
                    await message.channel.send(embed=discord.Embed(color=success, description="Could only remove {} from {}".format(amount, username)))
                    await leaderboard()
                else:
                  await message.channel.send(embed=discord.Embed(color=error, description="You can't remove the points of a bot"))
              else:
                await message.channel.send(embed=discord.Embed(color=error, description="You can't use this command"))
            else:
              await message.channel.send(embed=discord.Embed(color=error, description="Amount to remove should be greater than one"))
          else:
            await message.channel.send(embed=discord.Embed(color=error, description="Command format: ?remove @user <amount: int>"))
        else:
          await message.channel.send(embed=discord.Embed(color=error, description="Command format: ?remove @user <amount: int>"))
    elif message.content.startswith("?add"):
      msg = message.content.split()
      try:
        victim = msg[1]
        amount = msg[2]
        proceed = True
      except:
        await message.channel.send(embed=discord.Embed(color=error, description="Command format: ?add @user <amount: int>"))
        proceed = False
      if proceed:
        if victim.startswith('<@!'):
          victim_id = int(victim[3:-1])
          if amount.isdigit():
            if int(amount) > 0:
              if message.author.id in db[f'admins_{server_name}']:
                if victim_id in id_to_name_dict.keys():
                  # get username
                  username = id_to_name_dict.get(victim_id)
                  # add points
                  db[f'members_{server_name}'][username] += int(amount)
                  await message.channel.send(embed=discord.Embed(color=success, description="Added {} to {}".format(amount, username)))
                  await leaderboard()
                else:
                  await message.channel.send(embed=discord.Embed(color=error, description="You can't add points to a bot"))
              else:
                await message.channel.send(embed=discord.Embed(color=error, description="You can't use this command"))
            else:
              await message.channel.send(embed=discord.Embed(color=error, description="Amount to add should be greater than one"))
          else:
            await message.channel.send(embed=discord.Embed(color=error, description="Command format: ?add @user <amount: int>"))
        else:
          await message.channel.send(embed=discord.Embed(color=error, description="Command format: ?add @user <amount: int>"))
    if message.content.startswith('?promote') or message.content.startswith('?admin'):
      if message.author.id in db[f'admins_{server_name}']:
        msg = message.content.split()
        if len(msg) == 2:
          victim = msg[1]
          if victim.startswith('<@!'):
            victim_id = int(victim[3:-1])
            if victim_id in id_to_name_dict.keys():
              if victim_id not in db[f'admins_{server_name}']:
                # promote user
                db[f'admins_{server_name}'].append(victim_id)
                await message.channel.send(embed=discord.Embed(color=success, title="User Promoted", description="***{}*** was promoted to admin\n\n**Current Admins:** {}".format(id_to_name_dict.get(victim_id), ('\n' + ''.join((('{}\n'.format(id_to_name_dict.get(db['admins_{}'.format(server_name)][i]))) for i in range(len(db['admins_{}'.format(server_name)]))))))))
              else:
                await message.channel.send(embed=discord.Embed(color=error, description="User is already admin"))
            else:
              await message.channel.send(embed=discord.Embed(color=error, description="You can't promote a bot"))
          else:
            await message.channel.send(embed=discord.Embed(color=error, description="Command format: ?<promote | admin> <@user>"))
        else:
          await message.channel.send(embed=discord.Embed(color=error, description="Command format: ?<promote | admin> <@user>"))
      else:
        await message.channel.send(embed=discord.Embed(color=error, description="You can't use this command"))
    elif message.content.startswith('?demote'):
      if message.author.id in db[f'admins_{server_name}']:
        msg = message.content.split()
        if len(msg) == 2:
          victim = msg[1]
          if victim.startswith('<@!'):
            victim_id = int(victim[3:-1])
            if victim_id in id_to_name_dict.keys():
              if victim_id in db[f'admins_{server_name}']:
                # demote user
                db[f'admins_{server_name}'].remove(victim_id)
                await message.channel.send(embed=discord.Embed(color=success, title="User Demoted", description="***{}*** was demoted\n\n**Current Admins:** {}".format(id_to_name_dict.get(victim_id), ('\n' + ''.join((('{}\n'.format(id_to_name_dict.get(db['admins_{}'.format(server_name)][i]))) for i in range(len(db['admins_{}'.format(server_name)]))))))))
              else:
                await message.channel.send(embed=discord.Embed(color=error, description="User is not admin"))
            else:
              await message.channel.send(embed=discord.Embed(color=error, description="You can't demote a bot"))
          else:
            await message.channel.send(embed=discord.Embed(color=error, description="Command format: ?demote <@user>"))
        else:
          await message.channel.send(embed=discord.Embed(color=error, description="Command format: ?demote <@user>"))
      else:
        await message.channel.send(embed=discord.Embed(color=error, description="You can't use this command"))


    # laugh.mp4
    if message.content.lower() == "!laugh":
        await message.channel.send(
            "https://cdn.discordapp.com/attachments/680928395399266314/851702440625438741/lol-1.mp4"
        )

    # dance.mp4
    if message.content.lower() == "!dance":
        await message.channel.send(
            "https://cdn.discordapp.com/attachments/874447411144171610/875769944225222706/video1.mp4"
        )

    # mini_motorways free
    if message.content.lower() == "!mini_motorways" or message.content.lower(
    ) == "!mini motorways" or message.content.lower(
    ) == "!mini motorway" or message.content.lower() == "!mini_motorway":
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

    if message.content.lower() == "!kick":
      await message.channel.send("https://cdn.discordapp.com/attachments/742932318137876615/913560066328768542/beatkill.mp4")

    if message.content.lower() == "!help" or message.content.lower() == "?help":
      msg = "**Give Rep:** !thanks <@user>\n\n**Leaderboard:** !lb\n\n**Add Rep**: ?add <@user> <amount: int>\n\n**Remove Rep**: ?remove <@user> <amount: int>\n\n**Reset Rep**: ?reset <@user | all>\n\n**Get Channel Transcript**: ?<trans | transcript>\n\n**Add Admin**: ?<promote | admin> <@user>\n\n**Remove Admin**: ?demote <@user>\n\n**?clear <amount: int>**"
      await message.channel.send(embed=discord.Embed(title="BlueBerry Help", color=yellow, description=msg))

    if message.content.lower() == "?transcript" or message.content.lower() == "?trans":
      if message.author.id in db[f'admins_{server_name}']:
        await message.channel.send(embed=discord.Embed(description="Transcribing '{}'...".format(message.channel.name)))
        transcript = f"{message.channel.name}.txt"
        with open(transcript, "w") as file:
          async for msg in message.channel.history(limit=None):
            file.write(f"{msg.created_at} - {msg.author.display_name}: {msg.clean_content}\n")
        await message.channel.send(file=discord.File(transcript))
      else:
        await message.channel.send(embed=discord.Embed(color=error, description="You can't use this command"))

    # clear messages
    if message.content.startswith('?clear'):
      if message.author.id in db[f'admins_{server_name}']:
        msg = message.content.split()
        await message.delete()
        amount = int(msg[1])
        await message.channel.purge(limit=amount)
      else:
        await message.channel.send(embed=discord.Embed(color=error, description="You can't use this command"))

to_import()
client.run(environ['TOKEN'])
