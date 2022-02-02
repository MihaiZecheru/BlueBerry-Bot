from discord.ext.commands import cooldown, BucketType
import discord
import os, time, math, asyncio
from replit import db
from webserver import to_import
from discord.ext import commands
from datetime import datetime
from threading import Thread

lb = 0x951cff # purple
blue = 0x87CEEB # blue
success = 0x0adb23 # green
error = 0xdb0a0a # red

bburl = 'https://cdn.discordapp.com/emojis/932147404344533013.webp?size=96&quality=lossless'

class GlobalsAndDefaults:
    @classmethod
    def get_intents(cls):
        return discord.Intents.all()

    @staticmethod
    def reset_testingDBs():
      try:
        del db['admins_Wop']
        print("Removed 'admin' from 'Wop'")
      except:
        pass
      try:
        del db['members_Wop']
        print("Removed 'members' from 'Wop'")
      except:
        pass
      try:
        del db['opts_Wop']
        print("Removed 'opts' from 'Wop'")
      except:
        pass
      try:
        del db[f'bounties_742932317986750594']
        print("Removed 'bounties' from Wop")
      except:
        pass
      try:
        del db[f'weekly_tracker_Wop']
        print('Removed weekly_tracker from Wop')
      except:
        pass

    @staticmethod
    def reset_serverDBs(server_name, ID):
      try:
        del db['members_{}'.format(server_name)]
        print("Remove 'members' from '{}'".format(server_name))
      except:
        pass
      try:
        del db['opts_{}'.format(server_name)]
        print("Remove 'opts' from '{}'".format(server_name))
      except:
        pass
      try:
        del db['admins_{}'.format(server_name)]
        print("Remove 'admins' from '{}'".format(server_name))
      except:
        pass
      try:
        del db['bounties_{}'.format(ID)]
        print("Removed 'bounties' from {}".format(server_name))
      except:
        pass
      try:
        del db['weekly_tracker_{}'.format(server_name)]
        print('Removed weekly_tracker from {}'.format(server_name))
      except:
        pass

    @staticmethod
    def Sort_by_pointsNum(parent_list: list):
        parent_list.sort(key=lambda x: x[1], reverse=True)
        return parent_list


# create bot obj
bot = commands.Bot(command_prefix="!", intents=GlobalsAndDefaults.get_intents(), help_command=None)

@bot.event
async def on_ready():
  # will be called when the bot is ready to start being used
  activity = discord.Game(name="Tennis with Wyatt", type=3)
  await bot.change_presence(status=discord.Status.online,
                            activity=activity)
  print("\033[1;32;40mAuth and Sign in Complete; Logged in as \033[33m{0.user}\033[0m".format(bot))
  
  # get all guilds
  guilds = {guild.name.replace(" ", "_"): {'true_name': guild.name, 'id': guild.id, 'members': guild.members, 'channels': guild.text_channels} for guild in bot.guilds}

  # guild = discord.utils.get(bot.guilds, id=guilds.get("Test_server").get('id'))
  # channels = guild.text_channels 

class AdminCmds:

    @staticmethod
    @bot.event
    async def on_message(ctx):
        if (ctx.author == bot.user):
          return

        if isinstance(ctx.channel, discord.channel.DMChannel):
          '''is DM'''
          if ctx.reference is not None:
            message_id = ctx.reference.message_id

            channel = bot.get_channel(ctx.reference.channel_id)
            message = await channel.fetch_message(message_id)

            for guild in bot.guilds:
              try:
                if len(db['bounties_{}'.format(guild.id)].keys()) > 0:
                  '''bounty exists in this guild'''
                  # iterate through bounties
                  for key in db['bounties_{}'.format(guild.id)].keys():
                    bounty_info = db['bounties_{}'.format(guild.id)].get(key)
                    bounty_id_sets = bounty_info.get('idList')
                    for bounty_id_set in bounty_id_sets:
                      if bounty_id_set[0] == message_id or bounty_id_set[1] == message_id:
                        '''user replied to valid bounty message'''

                        # get channel and bounty creator id/obj
                        bounty_channel_id = bounty_info.get('channelID')
                        bounty_creator_id = bounty_info.get('authorID')

                        bounty_channel_obj = bot.get_channel(bounty_channel_id)
                        bounty_creator_obj = bot.get_user(bounty_creator_id)

                        answer = ctx.content

                        member_obj = guild.get_member(bounty_creator_id)
                        
                        convert_status = {
                          'dnd': 'DnD ⛔',
                          'idle': 'Idle 🌙',
                          'online': 'Online 🟢'
                        }

                        creator_status = convert_status.get(member_obj.status.name)

                        prompt = "If you feel that this answer has fulfilled your bounty's request, press the check mark to award {} the bounty.\n\nOtherwise press the X. **DO NOT LEAVE THIS UNMARKED**".format(ctx.author.name)

                        # create embeds for channel
                        pending = discord.Embed(timestamp=datetime.utcnow(), color=0x878a8a)
                        pending.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                        pending.add_field(name='Question', value=bounty_info.get('prompt'), inline=False)
                        pending.add_field(name='Answer', inline=False, value=answer)
                        pending.add_field(name='Status', value='**Pending...**', inline=True)
                        pending.add_field(name='Bounty Creator', inline=True, value=f'{bounty_creator_obj.name}: {creator_status}')
                        pending.add_field(name="Amount", inline=True, value=f'{str(bounty_info.get("amount"))} rep')
                        pending.set_footer(text='Bounty Answer Submitted', icon_url=bburl)

                        denied = discord.Embed(timestamp=datetime.utcnow(), color=error)
                        denied.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                        denied.add_field(name='Question', value=bounty_info.get('prompt'), inline=False)
                        denied.add_field(name='Answer', inline=False, value=answer)
                        denied.add_field(name='Status', value='**Declined** ❌', inline=True)
                        denied.add_field(name='Bounty Creator', inline=True, value=f'{bounty_creator_obj.name}: {creator_status}')
                        denied.add_field(name="Amount", inline=True, value=f'{str(bounty_info.get("amount"))} rep')
                        denied.set_footer(text='Bounty Answer Declined', icon_url=bburl)

                        accepted = discord.Embed(timestamp=datetime.utcnow(), color=success)
                        accepted.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                        accepted.add_field(name='Question', value=bounty_info.get('prompt'), inline=False)
                        accepted.add_field(name='Answer', inline=False, value=answer)
                        accepted.add_field(name='Status', value='**Accepted** ✅', inline=True)
                        accepted.add_field(name='Bounty Creator', inline=True, value=f'{bounty_creator_obj.name}: {creator_status}')
                        accepted.add_field(name="Amount", inline=True, value=f'{str(bounty_info.get("amount"))} rep')
                        accepted.set_footer(text='Bounty Answer Accepted', icon_url=bburl)

                        # create prompt embed
                        prompt_pending = discord.Embed(color=0x878a8a, timestamp=datetime.utcnow())
                        prompt_pending.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                        prompt_pending.set_footer(text='Answer Pending', icon_url=bburl)
                        prompt_pending.add_field(name='Answer', value=answer, inline=False)
                        prompt_pending.add_field(name='Prompt', inline=False, value=prompt)

                        prompt_denied = discord.Embed(timestamp=datetime.utcnow(), color=error)
                        prompt_denied.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                        prompt_denied.set_footer(text='Answer Declined', icon_url=bburl)
                        prompt_denied.add_field(name='Answer', value=answer, inline=False)
                        prompt_denied.add_field(name='Status', inline=True, value='**Declined** ❌')
                        prompt_denied.add_field(inline=True, name='Amount', value=f"{str(bounty_info.get('amount'))} rep")

                        prompt_accepted = discord.Embed(timestamp=datetime.utcnow(), color=success)
                        prompt_accepted.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                        prompt_accepted.set_footer(text='Answer Accepted', icon_url=bburl)
                        prompt_accepted.add_field(name='Answer', value=answer, inline=False)
                        prompt_accepted.add_field(name='Status', inline=True, value='**Accepted** ✅')
                        prompt_accepted.add_field(inline=True, name='Amount', value=f"{str(bounty_info.get('amount'))} rep")
                        
                        # send user answer to bounty channel as 'pending' embed
                        cnl = await bounty_channel_obj.send(embed=pending)
                        # send user answer to bounty creator as 'pending' prompt embed
                        dm = await bounty_creator_obj.send(embed=prompt_pending)
                        await dm.add_reaction('✅')
                        await dm.add_reaction('❌')

                        user_guild = bot.get_guild(guild.id)

                        # create event listeners for bounty creator reaction to prompt
                        @bot.event
                        async def on_reaction_add(reaction, user):
                          if user != bot.user:
                            if reaction.emoji == '✅':
                              await cnl.edit(embed=accepted)
                              await dm.edit(embed=prompt_accepted)
                              # award user
                              db['members_{}'.format(user_guild.name)][ctx.author.name] += bounty_info.get('amount')

                              # create closing embed
                              closing_embed = discord.Embed(color=success, timestamp=datetime.utcnow(), title='Bounty Claimed', description=f'**{ctx.author.name}** has been awarded **{bounty_info.get("amount")}** rep').set_footer(text='Bounty Claimed', icon_url=bburl)

                              REF = await bounty_channel_obj.fetch_message(int(bounty_info.get('REF')))

                              # kill daemon
                              db['THREAD{}'.format(bounty_info.get("ID"))] = False
                              
                              await bounty_channel_obj.send(embed=closing_embed, reference=REF, mention_author=True)
                              await Rep.leaderboard(ctx)
                            elif reaction.emoji == '❌':
                              await cnl.edit(embed=denied)
                              await dm.edit(embed=prompt_denied)
                            await dm.delete()
                            await bounty_creator_obj.send('The prompt has been automatically deleted. You can view the prompt in the channel where you created your bounty')
              except:
                continue
          else:
            # error: answer must be reply
            await ctx.author.send('Your answer must be a reply to the bounty notice')
          # escape to avoid errors
          return

        class Help:
          @classmethod
          def init_messages(cls):
            '''Create all help messages as class attribute'''

            # Full Member Message
            cls.member = {
              'rep': 
              """
              Place Bounty: `!bounty <amount: int> [additional information]` *\n
              Give Thanks: `!<thanks | thank> <@user>`\n
              Leaderboard: `!<leaderboard | lb>`\n
              Toggle Opt Status: `!opt`\n
              Help: `!help [command]`\n
              """,
            'games': 
              '''
              info: `!`\n
              info: `!`\n
              info: `!`\n
              '''
            }

            # Full Admin Message
            cls.admin = { 
              'rep': 
              """
              Add: `?add <@user> <amount: int>`\n
              Remove: `?remove <@user> <amount: int>`\n
              Reset: `?reset <@user>`\n
              """,
              'admin':
              """
              Promote: `?<promote | admim> <@user>`\n
              Demote: `?demote <@user>`\n
              List: `?<list | admins>`\n
              """,
              'other':
              """
              Clear: `?<clear | purge> <amount: int>`\n
              Transcribe: `?<trans | transcribe>`\n
              """
            }

            # admin level
            cls.clear = {
              'desc':"""
              Clears the specified amount of messages, which does not include the command itself
              """,
              'cmd': """
              ?clear <amount: int>
              ?purge <amount: int>
              """,
              'perm': """
              Admin
              """
            }

            cls.add = {
              'desc':"""
              Add the specified amount of rep to the specified user
              """,
              'cmd': """
              `?add <@user> <amount: int>`
              """,
              'perm': """
              Admin
              """
            }

            cls.remove = {
              'desc':"""
              Remove the specified amount of rep from the specified user
              """,
              'cmd': """
              `?remove <@user> <amount: int>`
              """,
              'perm': """
              Admin
              """
            }

            cls.reset = {
              'desc':"""
              Reset the points of the specified user or all users
              """,
              'cmd': """
              `?reset <@user | all>`
              """,
              'perm': """
              Admin
              """
            }

            cls.promote = {
              'desc':"""
              Promote a user to admin, which allows them to access all admin commands.
              """,
              'cmd': """
              `?promote <@user>`
              `?admin <@user>`
              """,
              'perm': """
              Admin
              """
            }

            cls.demote = {
              'desc':"""
              Demote a user to member. Removed access to all admin commands.
              """,
              'cmd': """
              `?demote <@user>`
              """,
              'perm': """
              Admin
              """
            }

            cls.list = {
              'desc':"""
              Lists all current admins.
              """,
              'cmd': """
              `?list`
              """,
              'perm': """
              Admin
              """
            }

            cls.trans = {
              'desc':"""
              Generate a channel transcript for the current channel. Returns a txt file of the entire channel
              """,
              'cmd': """
              `?transcribe`
              `?trans`
              """,
              'perm': """
              Admin
              """
            }

            # member level
            cls.opt = {
              'desc':"""
              Toggles opt status. When off, user will not recieve Bounty Notices in DMs
              """,
              'cmd': """
              `!opt`
              """,
              'perm': """
              Member, once per 24 hours
              """
            }

            cls.thanks = {
              'desc':"""
              Thanks a user, giving them 1 rep
              """,
              'cmd': """
              `!thanks <@user>`
              """,
              'perm': """
              Member, once per 5 minutes
              """
            }
            
            cls.bounty = {
              'desc':"""
              Sets a bounty on a message and sends a direct message to all users to alert them of the bounty. Opt out of bounty DM's with `!opt` if you are opted in.
              
              Minimum bounty amount is 5 rep. The bounty rep is taken directly from your total rep and given to the user who is first to help.
              
              When a user has an answer to your initial question, they can reply to the bot in their direct messages. When they do this, you will get a prompt asking if you want to award the bounty to the user who gave this answer.

              If you press yes, the accepted answer will be sent to the channel where the bounty was created, and the bounty award will be sent to the person who made the accepted answer
              """,
              'cmd': """
              `!bounty <amount: int> [additional message]` *
              """,
              'perm': """
              Member, once per 3 hours
              """
            }

            cls.lb = {
              'desc':"""
              Returns server reputation leaderbaord
              """,
              'cmd': """
              `!lb`
              `!leaderboard`
              """,
              'perm': """
              Member
              """
            }

            cls.help = {
              'desc':"""
              Help for member commands starts with `!` and help for admin commands starts with `?`. Type `!help` or `?help` and then a command name to get more information on that command
              """,
              'cmd': """
              `!help [command]`
              `?help [command]`
              """,
              'perm': """
              Member
              """
            }

            # member games
            cls.games = {
              'game': {
              'desc':"""
              description
              """,
              'cmd': """
              command
              """,
              'perm': """
              Member
              """
              },
              'game': {
              'desc':"""
              description
              """,
              'cmd': """
              command
              """,
              'perm': """
              Member
              """
              },
              'game': {
              'desc':"""
              description
              """,
              'cmd': """
              command
              """,
              'perm': """
              Member
              """,
              },
              'game': {
              'desc':"""
              description
              """,
              'cmd': """
              command
              """,
              'perm': """
              Member
              """
              }
            }

        class Data:
            def __init__(self, ctx):
                try:
                    # get server info
                    self.admins = []
                    self.all_members = ctx.guild.members
                    self.server_name = ctx.guild.name.replace(" ", "_")
                    self.user_ids = []

                    # get ids
                    for member in self.all_members:
                        if not member.bot:
                            self.user_ids.append(member.id)
                    self.id_to_name_dict = {}

                    # get names
                    for member in self.all_members:
                        if not member.bot:
                            self.id_to_name_dict[member.id] = member.name

                    # if dict does not exit, create it. Else: pass because it already exists
                    _ = db[f'members_{self.server_name}']
                except:
                    # create dicts and list
                    self.members_dict = {}
                    self.id_to_name_dict = {}
                    self.member_names = []

                    # create dicts and list
                    for user in self.all_members:
                        if not user.bot:
                            self.members_dict[user.name] = 0
                            self.id_to_name_dict[user.id] = user.name
                            self.member_names.append(user.name)
                    
                    # create db
                    db[f'members_{self.server_name}'] = self.members_dict
                    db[f'admins_{self.server_name}'] = [int(ctx.guild.owner.id)]
                    db[f'opts_{self.server_name}'] = self.user_ids
                    db['bounties_{}'.format(ctx.guild.id)] = {}
                    db['weekly_tracker_{}'.format(self.server_name)] = {memberID: {'helped_someone': 0, 'got_help': 0} for memberID in self.id_to_name_dict.keys()}
                    db['configurations_{}'.format(self.server_name)] = {"channel": None}

            async def leaderboard(self):
                # get list of all server members based on score
                member_info = []
                keys = db[f'members_{self.server_name}'].keys()
                for key in keys:
                    name = key
                    score = db[f'members_{self.server_name}'][key]
                    member_info.append([name, score])
                # put all members into descending order by points
                member_info = GlobalsAndDefaults.Sort_by_pointsNum(member_info)
                # get leaderboard
                body = ''
                for member in member_info:
                    name = member[0]
                    score = member[1]
                    body += f'**{name}**: {score}\n'
                # send leaderboard
                await ctx.channel.send(
                    embed=discord.Embed(timestamp=datetime.utcnow(), title='{} Leaderboard'.format(self.server_name), description=body, color=0x429ef5).set_footer(text="Leaderboard", icon_url=bburl))

        # GET DATA
        data = Data(ctx)

        # check bounties
        for ID in db[f'bounties_{ctx.guild.id}']:
          try:
            if not db[f'bounties_{ctx.guild.id}'].get(ID).get('running'):
              # get original user:
              user = bot.get_user(int(ID))
              channel = bot.get_channel(db[f'bounties_{ctx.guild.id}'].get(ID).get('channelID'))

              # construct embeds
              desc = "Nobody claimed your bounty within 24 hours of its creation. It's been deleted"
              user_embed = discord.Embed(title='Bounty Over', color=error, timestamp=datetime.utcnow(), description=desc)
              user_embed.add_field(name='Message Link', value=db[f'bounties_{ctx.guild.id}'].get(ID).get('link'), inline=False)
              user_embed.add_field(name='Bounty Amount', value=db[f'bounties_{ctx.guild.id}'].get(ID).get('amount'), inline=True)
              user_embed.add_field(name="Note", value="Bounty money will not be returned", inline=True)
              user_embed.set_footer(text='Bounty Over', icon_url=bburl)

              desc = desc.replace('your', f"**{user.name}'s**")
              channel_embed = discord.Embed(title='Bounty Over', color=error, timestamp=datetime.utcnow(), description=desc)
              channel_embed.add_field(name='Message Link', value=db[f'bounties_{ctx.guild.id}'].get(ID).get('link'), inline=False)
              channel_embed.add_field(name='Bounty Amount', value=db[f'bounties_{ctx.guild.id}'].get(ID).get('amount'), inline=True)
              channel_embed.add_field(name="Note", value="Bounty money will not be returned", inline=True)
              channel_embed.set_footer(text='Bounty Over', icon_url=bburl)

              # delete bounty
              db[f'bounties_{ctx.guild.id}'].pop(str(ID))
              
              # notify EOB
              await channel.send(embed=channel_embed)
              await user.send(embed=user_embed)
          except:
            continue

        # GET MESSAGES
        Help.init_messages()

        '''Send Help Message'''
        # all
        if ctx.content.lower() == '!help':
          await ctx.channel.send(embed=discord.Embed(color=lb, timestamp=datetime.utcnow()).add_field(name='Reputation', value=Help.member.get('rep'), inline=False).add_field(name='Note', value='*send command as reply to the message you want to set a bounty on', inline=False).set_footer(text='BlueBerry Help', icon_url=bburl))
        elif ctx.content.lower() == '?help':
          await ctx.channel.send(embed=discord.Embed(color=lb, timestamp=datetime.utcnow()).add_field(name='Reputation', value=Help.admin.get('rep'), inline=False).add_field(name="Admin", value=Help.admin.get('admin'), inline=False).add_field(name="Other", value=Help.admin.get('other'), inline=False).set_footer(text="BlueBerry Admin Help", icon_url=bburl))

        # member
        elif ctx.content.startswith('!help'):
          helptype = ctx.content.lower().split()[1]

          if helptype == 'help':
            await ctx.channel.send(embed=discord.Embed(color=lb, timestamp=datetime.utcnow()).add_field(inline=False, name='Description', value=Help.help.get('desc')).add_field(inline=False, name='Command', value=Help.help.get('cmd')).add_field(inline=False, name='Permission', value=Help.help.get('perm')).set_footer(text='Help: {0}'.format(helptype.title()), icon_url=bburl))
          elif helptype == 'thanks' or helptype == 'thank':
            await ctx.channel.send(embed=discord.Embed(color=lb, timestamp=datetime.utcnow()).add_field(inline=False, name='Description', value=Help.thanks.get('desc')).add_field(inline=False, name='Command', value=Help.thanks.get('cmd')).add_field(inline=False, name='Permission', value=Help.thanks.get('perm')).set_footer(text='Help: {0}'.format(helptype.title()), icon_url=bburl))
          elif helptype == 'lb' or helptype == 'leaderboard':
            await ctx.channel.send(embed=discord.Embed(color=lb, timestamp=datetime.utcnow()).add_field(inline=False, name='Description', value=Help.lb.get('desc')).add_field(inline=False, name='Command', value=Help.lb.get('cmd')).add_field(inline=False, name='Permission', value=Help.lb.get('perm')).set_footer(text='Help: {0}'.format(helptype.title()), icon_url=bburl))
          elif helptype == 'bounty':
            await ctx.channel.send(embed=discord.Embed(color=lb, thanks=datetime.utcnow()).add_field(inline=False, name='Description', value=Help.bounty.get('desc')).add_field(inline=False, name='Command', value=Help.bounty.get('cmd')).add_field(inline=False, name='Permission', value=Help.bounty.get('perm')).set_footer(text='Help: {0}'.format(helptype.title()), icon_url=bburl).add_field(name='Note', value='*send command as reply to the message you want to set a bounty on', inline=False))
          elif helptype == 'opt':
            await ctx.channel.send(embed=discord.Embed(color=lb, timestamp=datetime.utcnow()).add_field(inline=False, name='Description', value=Help.opt.get('desc')).add_field(inline=False, name='Command', value=Help.opt.get('cmd')).add_field(inline=False, name='Permission', value=Help.opt.get('perm')).set_footer(text='Help: {0}'.format(helptype.title()), icon_url=bburl))
          elif helptype == 'award':  
            await ctx.channel.send(embed=discord.Embed(color=lb, timestamp=datetime.utcnow()).add_field(inline=False, name='Description', value=Help.award.get('desc')).add_field(inline=False, name='Command', value=Help.award.get('cmd')).add_field(inline=False, name='Permission', value=Help.award.get('perm')).set_footer(text='Help: {0}'.format(helptype.title()), icon_url=bburl))
          elif helptype == 'VALUE':
            await ctx.channel.send(embed=discord.Embed(color=lb, timestamp=datetime.utcnow()).add_field(inline=False, name='Description', value=Help.VALUE.get('desc')).add_field(inline=False, name='Command', value=Help.VALUE.get('cmd')).add_field(inline=False, name='Permission', value=Help.VALUE.get('perm')).set_footer(text='Help: {0}'.format(helptype.title()), icon_url=bburl))
          else:
            # command does not exist
            await ctx.channel.send(embed=discord.Embed(color=error, timestamp=datetime.utcnow()).add_field(inline=False, name='Command Not Found', value=f'Command {helptype} does not exist').set_footer(text="Invalid Command", icon_url=bburl))
        elif ctx.content.startswith('?help'):
          helptype = ctx.content.lower().split()[1]

          if helptype == 'help':
            await ctx.channel.send(embed=discord.Embed(color=lb, timestamp=datetime.utcnow()).add_field(inline=False, name='Description', value=Help.help.get('desc')).add_field(inline=False, name='Command', value=Help.help.get('cmd')).add_field(inline=False, name='Permission', value=Help.help.get('perm')).set_footer(text='Help: {0}'.format(helptype.title()), icon_url=bburl))
          elif helptype == 'add':
            await ctx.channel.send(embed=discord.Embed(color=lb, timestamp=datetime.utcnow()).add_field(inline=False, name='Description', value=Help.add.get('desc')).add_field(inline=False, name='Command', value=Help.add.get('cmd')).add_field(inline=False, name='Permission', value=Help.add.get('perm')).set_footer(text='Help: {0}'.format(helptype.title()), icon_url=bburl))
          elif helptype == 'remove':
            await ctx.channel.send(embed=discord.Embed(color=lb, timestamp=datetime.utcnow()).add_field(inline=False, name='Description', value=Help.remove.get('desc')).add_field(inline=False, name='Command', value=Help.remove.get('cmd')).add_field(inline=False, name='Permission', value=Help.remove.get('perm')).set_footer(text='Help: {0}'.format(helptype.title()), icon_url=bburl))
          elif helptype == 'reset':
            await ctx.channel.send(embed=discord.Embed(color=lb, timestamp=datetime.utcnow()).add_field(inline=False, name='Description', value=Help.reset.get('desc')).add_field(inline=False, name='Command', value=Help.reset.get('cmd')).add_field(inline=False, name='Permission', value=Help.reset.get('perm')).set_footer(text='Help: {0}'.format(helptype.title()), icon_url=bburl))
          elif helptype == 'promote':
            await ctx.channel.send(embed=discord.Embed(color=lb, timestamp=datetime.utcnow()).add_field(inline=False, name='Description', value=Help.promote.get('desc')).add_field(inline=False, name='Command', value=Help.promote.get('cmd')).add_field(inline=False, name='Permission', value=Help.promote.get('perm')).set_footer(text='Help: {0}'.format(helptype.title()), icon_url=bburl))
          elif helptype == 'admin':
            await ctx.channel.send(embed=discord.Embed(color=lb, timestamp=datetime.utcnow()).add_field(inline=False, name='Description', value=Help.promote.get('desc')).add_field(inline=False, name='Command', value=Help.promote.get('cmd')).add_field(inline=False, name='Permission', value=Help.promote.get('perm')).set_footer(text='Help: {0}'.format(helptype.title()), icon_url=bburl))
          elif helptype == 'demote':
            await ctx.channel.send(embed=discord.Embed(color=lb, timestamp=datetime.utcnow()).add_field(inline=False, name='Description', value=Help.demote.get('desc')).add_field(inline=False, name='Command', value=Help.demote.get('cmd')).add_field(inline=False, name='Permission', value=Help.demote.get('perm')).set_footer(text='Help: {0}'.format(helptype.title()), icon_url=bburl))
          elif helptype == 'list':
            await ctx.channel.send(embed=discord.Embed(color=lb, timestamp=datetime.utcnow()).add_field(inline=False, name='Description', value=Help.list.get('desc')).add_field(inline=False, name='Command', value=Help.list.get('cmd')).add_field(inline=False, name='Permission', value=Help.list.get('perm')).set_footer(text='Help: {0}'.format(helptype.title()), icon_url=bburl))
          elif helptype == 'admins':
            await ctx.channel.send(embed=discord.Embed(color=lb, timestamp=datetime.utcnow()).add_field(inline=False, name='Description', value=Help.list.get('desc')).add_field(inline=False, name='Command', value=Help.list.get('cmd')).add_field(inline=False, name='Permission', value=Help.list.get('perm')).set_footer(text='Help: {0}'.format(helptype.title()), icon_url=bburl))
          elif helptype == 'clear':
            await ctx.channel.send(embed=discord.Embed(color=lb, timestamp=datetime.utcnow()).add_field(inline=False, name='Description', value=Help.clear.get('desc')).add_field(inline=False, name='Command', value=Help.clear.get('cmd')).add_field(inline=False, name='Permission', value=Help.clear.get('perm')).set_footer(text='Help: {0}'.format(helptype.title()), icon_url=bburl))
          elif helptype == 'purge':
            await ctx.channel.send(embed=discord.Embed(color=lb, timestamp=datetime.utcnow()).add_field(inline=False, name='Description', value=Help.clear.get('desc')).add_field(inline=False, name='Command', value=Help.clear.get('cmd')).add_field(inline=False, name='Permission', value=Help.clear.get('perm')).set_footer(text='Help: {0}'.format(helptype.title()), icon_url=bburl))
          elif helptype == 'trans':
            await ctx.channel.send(embed=discord.Embed(color=lb, timestamp=datetime.utcnow()).add_field(inline=False, name='Description', value=Help.trans.get('desc')).add_field(inline=False, name='Command', value=Help.trans.get('cmd')).add_field(inline=False, name='Permission', value=Help.trans.get('perm')).set_footer(text='Help: {0}'.format(helptype.title()), icon_url=bburl))
          elif helptype == 'transcribe':
            await ctx.channel.send(embed=discord.Embed(color=lb, timestamp=datetime.utcnow()).add_field(inline=False, name='Description', value=Help.trans.get('desc')).add_field(inline=False, name='Command', value=Help.trans.get('cmd')).add_field(inline=False, name='Permission', value=Help.trans.get('perm')).set_footer(text='Help: {0}'.format(helptype.title()), icon_url=bburl))
          elif helptype == 'SAC':
            # SAC == set announcements channel
            await ctx.channel.send(embed=discord.Embed(color=lb, timestamp=datetime.utcnow()).add_field(inline=False, name='Description', value=Help.trans.get('desc')).add_field(inline=False, name='Command', value=Help.trans.get('cmd')).add_field(inline=False, name='Permission', value=Help.trans.get('perm')).set_footer(text='Help: {0}'.format(helptype.title()), icon_url=bburl))
          else:
            # command does not exist
            await ctx.channel.send(embed=discord.Embed(color=error, timestamp=datetime.utcnow()).add_field(inline=False, name='Command Not Found', value=f'Command {helptype} does not exist').set_footer(text="Invalid Command", icon_url=bburl))


        if ctx.content.startswith('?reset'):
            msg = ctx.content.split()
            try:
              victim = msg[1]
            except:
              await ctx.channel.send(embed=discord.Embed(color=error, description='Command Format: `?reset <@user>`'))
            if victim.startswith('<@!'):
                victim_id = int(victim[3:-1])
                if ctx.author.id in db[f'admins_{data.server_name}']:
                    if victim_id in data.id_to_name_dict.keys():
                        # get username
                        username = data.id_to_name_dict.get(victim_id)
                        # reset points
                        db[f'members_{data.server_name}'][username] = 0
                        await ctx.channel.send(
                            embed=discord.Embed(color=success, description="Reset points for {}".format(username)))
                        await data.leaderboard()
                    else:
                        await ctx.channel.send(
                            embed=discord.Embed(color=error, description="You can't reset the points of a bot"))
                else:
                    await ctx.channel.send(
                        embed=discord.Embed(color=error, description="You can't use this command"))
            else:
              if victim == 'all':
                    if ctx.author.id in db[f'admins_{data.server_name}']:
                          # reset points
                        for member_id in data.id_to_name_dict.keys():
                            db[f'members_{data.server_name}'][data.id_to_name_dict[member_id]] = 0
                        await ctx.channel.send(
                            embed=discord.Embed(color=success, description="Reset points for all members"))
                        await data.leaderboard()
                    else:
                        await ctx.channel.send(
                            embed=discord.Embed(color=error, description="You can't use this command"))
              else:
                  await ctx.channel.send(
                      embed=discord.Embed(color=error, description="Command format: `?reset <@user | all>`"))
        elif ctx.content.startswith("?set_announcement_channel"):
          arg = ctx.content.split()
          if len(arg) == 2 and arg[1].startswith('<#') and arg[1][-1] == '>':
            arg = int(arg[1][2:-1])
            if arg in [channel.id for channel in ctx.guild.channels]:
              db['configurations_{}'.format(ctx.guild.name)]['channel'] = arg
              await ctx.channel.send(embed=discord.Embed(color=success, description='Announcement channel set to `#{}`'.format(bot.get_channel(arg).name), timestamp=datetime.now()).set_footer(text='Channel Set', icon_url=bburl))
            else:
              await ctx.channel.send(embed=discord.Embed(color=error, description='Given channel must belong to server'))
          else:
            await ctx.channel.send(embed=discord.Embed(description="Command Format: `?set_announcement_channel <channel>`"))
        elif ctx.content.startswith("?remove"):
          msg = ctx.content.split()
          try:
            victim = msg[1]
            amount = msg[2]
            proceed = True
          except:
            await ctx.channel.send(embed=discord.Embed(color=error, description="Command format: `?remove @user <amount: int>`"))
            proceed = False
          if proceed:
            if victim.startswith('<@!'):
              victim_id = int(victim[3:-1])
              if amount.isdigit():
                if int(amount) > 0:
                  if ctx.author.id in db[f'admins_{data.server_name}']:
                    if victim_id in data.id_to_name_dict.keys():
                      # get username
                      username = data.id_to_name_dict.get(victim_id)
                      # remove points
                      if int(amount) > db[f'members_{data.server_name}'][username]:
                        previous_value = db[f'members_{data.server_name}'][username]
                        db[f'members_{data.server_name}'][username] = 0
                        await ctx.channel.send(embed=discord.Embed(color=success, description="Removed {} from {}".format(previous_value, username)))
                        await data.leaderboard()
                      else:
                        db[f'members_{data.server_name}'][username] -= int(amount)
                        await ctx.channel.send(embed=discord.Embed(color=success, description="Could only remove {} from {}".format(amount, username)))
                        await data.leaderboard()
                    else:
                      await ctx.channel.send(embed=discord.Embed(color=error, description="You can't remove the points of a bot"))
                  else:
                    await ctx.channel.send(embed=discord.Embed(color=error, description="You can't use this command"))
                else:
                  await ctx.channel.send(embed=discord.Embed(color=error, description="Amount to remove should be greater than one"))
              else:
                await ctx.channel.send(embed=discord.Embed(color=error, description="Command format: `?remove @user <amount: int>`"))
            else:
              await ctx.channel.send(embed=discord.Embed(color=error, description="Command format: `?remove @user <amount: int>`"))
        elif ctx.content.startswith("?add"):
          msg = ctx.content.split()
          try:
            victim = msg[1]
            amount = msg[2]
            proceed = True
          except:
            await ctx.channel.send(embed=discord.Embed(color=error, description="Command format: `?add @user <amount: int>`"))
            proceed = False
          if proceed:
            if victim.startswith('<@!'):
              victim_id = int(victim[3:-1])
              if amount.isdigit():
                if int(amount) > 0:
                  if ctx.author.id in db[f'admins_{data.server_name}']:
                    if victim_id in data.id_to_name_dict.keys():
                      # get username
                      username = data.id_to_name_dict.get(victim_id)
                      # add points
                      db[f'members_{data.server_name}'][username] += int(amount)
                      await ctx.channel.send(embed=discord.Embed(color=success, description="Added {} to {}".format(amount, username)))
                      await data.leaderboard()
                    else:
                      await ctx.channel.send(embed=discord.Embed(color=error, description="You can't add points to a bot"))
                  else:
                    await ctx.channel.send(embed=discord.Embed(color=error, description="You can't use this command"))
                else:
                  await ctx.channel.send(embed=discord.Embed(color=error, description="Amount to add should be greater than one"))
              else:
                await ctx.channel.send(embed=discord.Embed(color=error, description="Command format: `?add @user <amount: int>`"))
            else:
              await ctx.channel.send(embed=discord.Embed(color=error, description="Command format: `?add @user <amount: int>`"))
        if ctx.content.startswith('?promote') or ctx.content.startswith('?admin'):
          if ctx.author.id in db[f'admins_{data.server_name}']:
            msg = ctx.content.split()
            if len(msg) == 2:
              victim = msg[1]
              if victim.startswith('<@!'):
                victim_id = int(victim[3:-1])
                if victim_id in data.id_to_name_dict.keys():
                  if victim_id not in db[f'admins_{data.server_name}']:
                    # promote user
                    db[f'admins_{data.server_name}'].append(victim_id)
                    await ctx.channel.send(embed=discord.Embed(color=success, title='**{}** was promoted to admin\n\n'.format(data.id_to_name_dict.get(victim_id)), timestamp=datetime.utcnow()).add_field(name='Current Admins', value="{}".format(('\n' + ''.join((('{}\n'.format(data.id_to_name_dict.get(db['admins_{}'.format(data.server_name)][i]))) for i in range(len(db['admins_{}'.format(data.server_name)]))))))).set_footer(text="User Promoted", icon_url=bburl))
                  else:
                    await ctx.channel.send(embed=discord.Embed(color=error, description="User is already admin"))
                else:
                  await ctx.channel.send(embed=discord.Embed(color=error, description="You can't promote a bot"))
              else:
                await ctx.channel.send(embed=discord.Embed(color=error, description="Command format: `?<promote | admin> <@user>`"))
            else:
              await ctx.channel.send(embed=discord.Embed(color=error, description="Command format: `?<promote | admin> <@user>`"))
          else:
            await ctx.channel.send(embed=discord.Embed(color=error, description="You can't use this command"))
        elif ctx.content.lower() == "?list":
          await ctx.channel.send(embed=discord.Embed(color=success, timestamp=datetime.utcnow()).add_field(name='Current Admins', value="{}".format(('\n' + ''.join((('{}\n'.format(data.id_to_name_dict.get(db['admins_{}'.format(data.server_name)][i]))) for i in range(len(db['admins_{}'.format(data.server_name)]))))))).set_footer(text="All Admins", icon_url=bburl)) 
        elif ctx.content.startswith('?demote'):
          if ctx.author.id in db[f'admins_{data.server_name}']:
            msg = ctx.content.split()
            if len(msg) == 2:
              victim = msg[1]
              if victim.startswith('<@!'):
                victim_id = int(victim[3:-1])
                if victim_id in data.id_to_name_dict.keys():
                  if victim_id in db[f'admins_{data.server_name}']:
                    # demote user
                    db[f'admins_{data.server_name}'].remove(victim_id)
                    await ctx.channel.send(embed=discord.Embed(color=success, title='**{}** was demoted\n\n'.format(data.id_to_name_dict.get(victim_id)), timestamp=datetime.now()).add_field(name='Current Admins', value="{}".format(('\n' + ''.join((('{}\n'.format(data.id_to_name_dict.get(db['admins_{}'.format(data.server_name)][i]))) for i in range(len(db['admins_{}'.format(data.server_name)]))))))).set_footer(text="User Demoted", icon_url=bburl))
                  else:
                    await ctx.channel.send(embed=discord.Embed(color=error, description="User is not admin"))
                else:
                  await ctx.channel.send(embed=discord.Embed(color=error, description="You can't demote a bot"))
              else:
                await ctx.channel.send(embed=discord.Embed(color=error, description="Command format: `?demote <@user>`"))
            else:
              await ctx.channel.send(embed=discord.Embed(color=error, description="Command format: `?demote <@user>`"))
          else:
            await ctx.channel.send(embed=discord.Embed(color=error, description="You can't use this command"))

        elif ctx.content.lower() == '?trans' or ctx.content.lower() == '?transcribe':
          if ctx.author.id in db[f'admins_{data.server_name}']:
            await ctx.channel.send(embed=discord.Embed(description="Transcribing '{}'...".format(ctx.channel.name)))
            transcript = f"{ctx.channel.name}.txt"
            with open(transcript, "w") as file:
              async for msg in ctx.channel.history(limit=None):
                file.write(f"{msg.created_at} - {msg.author.display_name}: {msg.clean_content}\n")
            await ctx.channel.send(file=discord.File(transcript))
          else:
            await ctx.channel.send(embed=discord.Embed(color=error, description="You can't use this command"))
        elif ctx.content.startswith('?clear') or ctx.content.startswith("?purge"):
          if ctx.author.id in db[f'admins_{data.server_name}']:
            msg = ctx.content.split()
            await ctx.delete()
            amount = int(msg[1])
            await ctx.channel.purge(limit=amount)
          else:
            await ctx.channel.send(embed=discord.Embed(color=error, description="You can't use this command"))

        # Allow @bot.command
        await bot.process_commands(ctx)

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    await ctx.channel.send(delete_after=7, embed=discord.Embed(description=f'This command is on cooldown! Try again in {math.floor(error.retry_after / 60)}:{(error.retry_after % 60):.0f}', color=0xdb0a0a, timestamp=datetime.utcnow()).set_footer(text="Cooldown", icon_url=bburl))  


async def bounty_tracker(ctx, ID, amount, link, idList, prompt, REF):
  # create bounty
  db[f'bounties_{ctx.guild.id}'][str(ID)] = {'amount': amount, 'link': link, 'running': True, 'channelID': ctx.channel.id, 'guild': ctx.guild.id, 'authorID': ctx.author.id, 'idList': idList, 'prompt': prompt, 'REF': REF, 'bounty_trackerID': ID}

  # set timer (24 hour)
  for _ in range(86400):
    if db['THREAD{}'.format(ctx.author.id)]:
      time.sleep(1)
    else:
      # delete bounty
      db[f'bounties_{ctx.guild.id}'].pop(str(ID))
      return

  # change state to finished
  db[f'bounties_{ctx.guild.id}'][str(ID)]['running'] = False
  

def between(ctx, ID, amount, link, idList, prompt, REF):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(bounty_tracker(ctx, ID, amount, link, idList, prompt, REF))
    loop.close()


class Rep:
  @classmethod
  def get_data(cls, ctx):
    try:
      # get server info
      cls.admins = []
      cls.all_members = ctx.guild.members
      cls.server_name = ctx.guild.name.replace(" ", "_")
      cls.user_ids = []

      # get ids
      for member in cls.all_members:
          if not member.bot:
              cls.user_ids.append(member.id)
      cls.id_to_name_dict = {}

      # get names
      for member in cls.all_members:
        if not member.bot:
          cls.id_to_name_dict[member.id] = member.name

      # if dict does not exit, create it. Else: pass because it already exists
      _ = db[f'members_{cls.server_name}']
    except:
      # create dicts and DB
      cls.members_dict = {}
      cls.id_to_name_dict = {}

      # create dicts
      for user in cls.all_members:
        if not user.bot:
          cls.members_dict[user.name] = 0
          cls.id_to_name_dict[user.id] = user.name

      db[f'members_{cls.server_name}'] = cls.members_dict
      db[f'admins_{cls.server_name}'] = [549456138698227712]
      db[f'opts_{cls.server_name}'] = cls.all_members
      db['bounties_{}'.format(ctx.guild.id)] = {}
      db['weekly_tracker_{}'.format(self.server_name)] = {memberID: {'helped_someone': 0, 'got_help': 0} for memberID in self.id_to_name_dict.keys()}
      db['configurations_{}'.format(self.server_name)] = {"channel": None}
      
  
  @classmethod
  async def leaderboard(cls, ctx):
    # get list of all server members based on score
    member_info = []
    keys = db[f'members_{cls.server_name}'].keys()
    for key in keys:
        name = key
        score = db[f'members_{cls.server_name}'][key]
        member_info.append([name, score])
    # put all members into descending order by points
    member_info = GlobalsAndDefaults.Sort_by_pointsNum(member_info)
    # get leaderboard
    body = ''
    for member in member_info:
        name = member[0]
        score = member[1]
        body += f'**{name}**: {score}\n'
    # send leaderboard
    await ctx.channel.send(
        embed=discord.Embed(timestamp=datetime.utcnow(), title='{} Leaderboard'.format(cls.server_name), description=body, color=0x429ef5).set_footer(text="Leaderboard", icon_url=bburl))
  
  @staticmethod
  @bot.command(name='opt')
  @commands.cooldown(1, 86400, commands.BucketType.member)
  async def toggle_opt(ctx):
    # remove
    if ctx.author.id in db[f'opts_{ctx.guild.name.replace(" ", "_")}']:
      db[f'opts_{ctx.guild.name.replace(" ", "_")}'].remove(ctx.author.id)
      await ctx.channel.send(embed=discord.Embed(color=success, timestamp=datetime.utcnow(), description='You have **opted-out** of the Bounty Notice list.\n\nType `!opt` to opt back in').set_footer(text='Opt Out', icon_url=bburl))
    elif ctx.author.id not in db[f'opts_{ctx.guild.name.replace(" ", "_")}']:
      # add
      db[f'opts_{ctx.guild.name.replace(" ", "_")}'].append(ctx.author.id)
      await ctx.channel.send(embed=discord.Embed(color=success, timestamp=datetime.utcnow(), description='You have **opted-in** to the Bounty Notice list.\n\nType `!opt` to opt back out').set_footer(text='Opt In', icon_url=bburl))

  @staticmethod
  @bot.command(aliases=['leaderboard'])
  async def lb(ctx):
    Rep.get_data(ctx)
    await Rep.leaderboard(ctx)

  @staticmethod
  @bot.command(aliases=['thank'])
  @commands.cooldown(1, 300, commands.BucketType.member) # once every 5 minutes per user
  async def thanks(ctx, target=None):
    # init data
    Rep.get_data(ctx)

    if target == None:
      await ctx.channel.send(embed=discord.Embed(color=0xdb0a0a, timestamp=datetime.utcnow(), description='Command Format: `!<thanks | thank> <@user>`'))
      ctx.command.reset_cooldown(ctx)

    if target.startswith('<@!'):
      user_id = int(target[3:-1])
      if user_id != ctx.author.id:
        if user_id in Rep.user_ids:
          # get username
          username = Rep.id_to_name_dict.get(user_id)
          # add one point
          db[f'members_{Rep.server_name}'][username] += 1
          
          # add weekly tracker points for target and author
          db['weekly_tracker_{}'.format(Rep.server_name)][str(ctx.author.id)]['got_help'] += 1
          db['weekly_tracker_{}'.format(Rep.server_name)][str(user_id)]['helped_someone'] += 1

          # tell user it worked
          await ctx.channel.send(embed=discord.Embed(timestamp=datetime.now(), description='Added 1 point to **{}**'.format(username), color=success).set_footer(text='Point Added', icon_url=bburl))
        else:
          await ctx.channel.send(embed=discord.Embed(title='Invalid User', description='{} is not in server'.format(f'<@!{user_id}>'), color=error))
      else:
        await ctx.channel.send(embed=discord.Embed(description="You can't give points to yourself", color=error))
        ctx.command.reset_cooldown(ctx)

  @staticmethod
  @bot.command()
  @commands.cooldown(1, 10800, commands.BucketType.member) # once every 3 hours per user
  async def bounty(ctx, amount: int, *extra):
    # check to see if message has reply
    if ctx.message.reference is not None:
      # get id
      ID = ctx.message.reference.message_id
      REF = ID

      # check amount
      if amount < 5:
        await ctx.channel.send(embed=discord.Embed(description='Bounty amount must be at least 5', timestamp=datetime.utcnow(), color=error).set_footer(text='Broke-Ass 😤', icon_url=bburl))
        ctx.command.reset_cooldown(ctx)
      else:
        if db['members_{}'.format(ctx.guild.name.replace(' ', '_'))][ctx.author.name] >= amount:
          # send notice
          await ctx.channel.send(delete_after=7, embed=discord.Embed(color=error, timestamp=datetime.utcnow(), title='Notice', description="If the ID you entered was not from a message in this channel or does not correspond to a plain text message the command won't work. If no success message appears, the command failed.").set_footer(text="Notice", icon_url=bburl))

          try:
            # check ID and get message
            # command will exit if ID does not exist
            message = await ctx.channel.fetch_message(ID)
            message = message.content
          except:
            ctx.command.reset_cooldown(ctx)
            return

          # make sure message is not embed or img
          if message == '':
            await ctx.channel.send(delete_after=7, embed=discord.Embed(color=error, timestamp=datetime.utcnow(), title='Bounty Failed', description='Given ID must be the ID of a text message (can not be image, embed, etc.)').set_footer(text='Bounty Failed', icon_url=bburl))
            ctx.command.reset_cooldown(ctx)
            return

          # get message link
          link = "https://discord.com/channels/{0}/{1}/{2}".format(ctx.guild.id, ctx.channel.id, ID)

          embed = discord.Embed(color=0x429ef5, timestamp=datetime.utcnow())
          embed.add_field(name="Message", value=message, inline=False)
          embed.add_field(name='Message Link', value=link, inline=False)
          embed.add_field(name='From', value=ctx.author.name, inline=True)
          embed.add_field(name='Award', value=f'{amount} rep', inline=True)
          embed.add_field(name='Time', value='24 Hours', inline=True)
          
          # add additional info if given
          if len(extra) != 0:
            abc = " ".join(extra)
            embed.add_field(name='Additional Information', value=abc, inline=False)
          
          # set footer
          embed.set_footer(text="Bounty Notice", icon_url=bburl)

          recipients = [bot.get_user(user_id) for user_id in (db[f'opts_{ctx.guild.name.replace(" ", "_")}'])]

          # remove rep
          db['members_{}'.format(ctx.guild.name.replace(' ', '_'))][ctx.author.name] -= amount

          idList = []

          # dm all opts
          for member in recipients:
            try:
              one = await member.send(embed=embed)
              two = await member.send("To stop recieving Bounty Notices, type `!opt` in the server you want to stop recieving notices from.")
              idList.append([one.id, two.id])
            except Exception as e:
              print("\033[31m", e, f'FROM: {member.name}\033[0m')

          # set bounty tracker
          bt = Thread(daemon=True, target=between, args=(ctx, ctx.author.id, amount, link, idList, message, REF))
          bt.name = str(ctx.author.id)
          bt.start()

          db['THREAD{}'.format(ctx.author.id)] = True

          body_text = "A Bounty Notice has been sent out to the following members with an award of **{}** Rep:\n\n**{}**\n\nYou have **{}** Rep left after creating this bounty\n\nWhen someone answers your question, you will be sent a DM with their answer. React to that message to accept or decline it.".format(amount, ", ".join(user.name for user in recipients), db['members_{}'.format(ctx.guild.name.replace(' ', '_'))][ctx.author.name])

          # confirmation
          await ctx.channel.send(embed=embed)
          await ctx.channel.send(embed=discord.Embed(title='Bounty Created', color=success, timestamp=datetime.utcnow(), description=body_text).set_footer(text="Bounty Created", icon_url=bburl))
        else:
          # insufficient funds error message
          await ctx.channel.send(delete_after=7, embed=discord.Embed(color=error, title='Bounty Failed', description="You don't have enough rep to create a bounty for this amount: {}".format(amount), timestamp=datetime.utcnow()).set_footer(text="Bounty Failed", icon_url=bburl))
          ctx.command.reset_cooldown(ctx)
    else:
      try:
        embed = discord.Embed(delete_after=7, color=error, timestamp=datetime.utcnow(), title='Command Error', description='You must reply to the message you want to set a bounty on!').set_footer(text="Command Error", icon_url=bburl)
        await ctx.channel.send(embed=embed)
        ctx.command.reset_cooldown(ctx)
      except Exception as e:
        print(e)


class Extra:

  @staticmethod
  @bot.command()
  async def laugh(ctx):
    await ctx.channel.send("https://cdn.discordapp.com/attachments/680928395399266314/851702440625438741/lol-1.mp4")

  @staticmethod
  @bot.command()
  async def dance(ctx):
    await ctx.channel.send("https://cdn.discordapp.com/attachments/874447411144171610/875769944225222706/video1.mp4")

  # mini motorways
  @staticmethod
  @bot.command()
  async def mini_motorway(ctx):
    await ctx.author.send(
      "Here's a quick preview of the game:\nhttps://media.discordapp.net/attachments/742932318137876615/912959901519732766/header.png\nhttps://media.discordapp.net/attachments/742932318137876615/912960033548025886/ss_a4db48bc510aa79f01147e1137d1137143b2ca6d.png?width=1014&height=676\nhttps://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DRHX0CfcgOas&psig=AOvVaw24j9YS5dshtdsf9VyKAZ-A&ust=1637823426180000&source=images&cd=vfe&ved=0CA0Q3YkBahcKEwiAxKXttbD0AhUAAAAAHQAAAAAQCQ"
      )
    await ctx.author.send(
      "**If you're interested, you can download Mini Motorways for free here:** https://drive.google.com/uc?export=download&id=15I4qy5tUCJLdULv0z-6gPZbplaIpuisR"
    )
    await ctx.channel.send(embed=discord.Embed(title="Success", color=success, description="Mini Motorways preview sent to direct messages"))

  # mini motorways
  @staticmethod
  @bot.command()
  async def mini_motorways(ctx):
    await ctx.author.send(
      "Here's a quick preview of the game:\nhttps://media.discordapp.net/attachments/742932318137876615/912959901519732766/header.png\nhttps://media.discordapp.net/attachments/742932318137876615/912960033548025886/ss_a4db48bc510aa79f01147e1137d1137143b2ca6d.png?width=1014&height=676\nhttps://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DRHX0CfcgOas&psig=AOvVaw24j9YS5dshtdsf9VyKAZ-A&ust=1637823426180000&source=images&cd=vfe&ved=0CA0Q3YkBahcKEwiAxKXttbD0AhUAAAAAHQAAAAAQCQ"
      )
    await ctx.author.send(
      "**If you're interested, you can download Mini Motorways for free here:** https://drive.google.com/uc?export=download&id=15I4qy5tUCJLdULv0z-6gPZbplaIpuisR"
    )
    await ctx.channel.send(embed=discord.Embed(title="Success", color=success, description="Mini Motorways preview sent to direct messages"))

  @staticmethod
  @bot.command()
  async def ping(ctx):
    await ctx.channel.send(embed=discord.Embed(description=f"🐧Pingu time: **{round(bot.latency * 1000)}ms**"))

  @staticmethod
  @bot.command()
  async def kick(ctx):
    await ctx.channel.send("https://cdn.discordapp.com/attachments/742932318137876615/913560066328768542/beatkill.mp4")

def rep_stats_manager():
  print("\033[1;32;40mRepStatsManager: started\033[0m")
  time.sleep(10)
  
  while True:
    time.sleep(10)
    # check for end of week
    if datetime.today().weekday() == 6: # 6 is sunday, 0 is monday
      print("\033[33mRepStatsManager Event: endOfWeek\033[0m")

      for guild in bot.guilds:
        try:
          # get member stats
          recieved = sorted([(value.get("got_help"), key) for key, value in db["weekly_tracker_{}".format(guild.name)].items()], key=lambda x: x[0], reverse=True)
          gave = sorted([(value.get("helped_someone"), key) for key, value in db["weekly_tracker_{}".format(guild.name)].items()], key=lambda x: x[0], reverse=True)

          # get the top three of each category
          recieved_the_most_help = "\n".join([f'**{(bot.get_user(int(INFO[1]))).name}**: {INFO[0]}' for INFO in recieved[:(len(recieved) - 3)]])

          gave_the_most_help = "\n".join([f'**{(bot.get_user(int(INFO[1]))).name}**: {INFO[0]}' for INFO in gave[:(len(gave) - 3)]])

          # reset dictionary
          for member in db['weekly_tracker_{}'.format(guild)]:
            db['weekly_tracker_{}'.format(guild)][member] = {'helped_someone': 0, 'got_help': 0}

          # make embed
          embed = discord.Embed(timestamp=datetime.utcnow()).set_footer(text='{} Stats'.format(guild.name), icon_url=bburl).add_field(inline=True, name='__**Recieved Help The Most**__', value=recieved_the_most_help).add_field(inline=True, name='__**Gave Help The Most**__', value=f'\n{gave_the_most_help}')
          CHANNEL = bot.get_channel(db['configurations_{}'.format(guild.name)].get('channel'))
          if CHANNEL is None:
            print('channel is none')
            for channel12 in guild.text_channels:
              if channel12.permissions_for(guild.me).send_messages:
                  CHANNEL = channel12
                  break
          try:
            bot.loop.create_task(CHANNEL.send(embed=embed))
          except:
            print('\033[31m{} StatMessage Failed: Could not send embed'.format(guild.name))
        except:
          print('\033[31m{} StatMessage Failed: DB does not exist'.format(guild.name))

if __name__ == '__main__':
  # GlobalsAndDefaults.reset_testingDBs()
  # GlobalsAndDefaults.reset_serverDBs('Hoopla', 838622489739001906)

  # print(db.keys())

  rep_stats_manager_thread = Thread(target=rep_stats_manager, daemon=True)
  rep_stats_manager_thread.start()

  # start bot
  to_import()
  bot.run(os.environ['TOKEN'])
