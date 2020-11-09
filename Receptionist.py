import discord
import asyncio
import wavelink
from discord.ext import commands, tasks

import pyttsx3
import os


from discord.utils import get

channels = []

#---Set Default Narrator Language---#

engine = pyttsx3.init()#pyttsx3 init
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-30)
voices = engine.getProperty('voices')
for voice in voices:
    if voice.name == 'Microsoft Haruka Desktop - Japanese':
        engine.setProperty('voice', voice.id)

#---Set default command---#

class Bot(commands.Bot):

    
    def __init__(self):
        super(Bot, self).__init__(command_prefix=['/'])

        self.add_cog(Music(self))
        self.add_cog(context(self))

    async def on_ready(self):
        print(f'Logged in as {self.user.name} | {self.user.id}')
        await self.change_presence(status=discord.Status.online, activity=discord.Game('/connect'))

#---Bot action---#

class Music(commands.Cog):


    #---__init__---#
    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = wavelink.Client(bot=self.bot)

        self.bot.loop.create_task(self.start_nodes())
        self.bot.remove_command("help")


    #---Setting for connection to application.yml---#
    async def start_nodes(self):
        await self.bot.wait_until_ready()

        await self.bot.wavelink.initiate_node(host='127.0.0.1',
                                              port=80,
                                              rest_uri='http://127.0.0.1:80',
                                              password='testing',
                                              identifier='TEST',
                                              region='us_central')


    #---Unknown---#
    @commands.command(name='connect')
    async def connect_(self, ctx, *, channel: discord.VoiceChannel = None):

        player = self.bot.wavelink.get_player(ctx.guild.id)
        channel = ctx.author.voice.channel
        await player.connect(channel.id)


    #---Bot Narrator Section---#
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        player = self.bot.wavelink.get_player(member.guild.id)
        voice1 = engine.getProperty('voice')


        #---Player Join---#
        if before.channel is None and after.channel is not None:
            channel = member.voice.channel
            #print(member.activities)
            if not player.is_connected:
                await player.connect(channel.id)
                channels.append(channel.id)

        #---Call people with id---#
            if int(member.id) == 195500932442750976: #change id here#
                url = r"sound\baka.mp3"
                track1 = await self.bot.wavelink.get_tracks(url)
                await player.play(track1[0])
            else:
                name = member.name

                if voice.name == "Microsoft Haruka Desktop - Japanese":
                    text = f'{name} を入ります。'
                    print(voice.name)

                elif voice.name == "Microsoft Zira Desktop - English (United States)":
                    text = f'{name} has joined your channel.'
                    print(voice.name)
                    
                engine.save_to_file(text , f'sound\{name}_join.mp3')
                engine.runAndWait()
                save = f"{name}_join.mp3"

                url = r"sound\{}".format(save)
                track1 = await self.bot.wavelink.get_tracks(url)
                await player.play(track1[0])
            while player.is_playing:
                await asyncio.sleep(1)
            os.system(f'del /f "{save}"')


        #---Custom Player Sound---#
        elif before.channel is not None and after.channel is None and int(member.id) == 372762649118638082:
            url = r"/home/diswave/NaiNuey.m4a"
            track1 = await self.bot.wavelink.get_tracks(url)
            await player.play(track1[0])


        #---Unknown---#
        elif before.channel is not None and after.channel is None and int(member.id) == 774307466720444446: 
            await player.disconnect()
        
        
        #---Player Mute---#
        elif before.self_mute is False and after.self_mute is True:
            """mute function"""
            name = member.name
           

            if voice1 == "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_JA-JP_HARUKA_11.0":
                text = f'{name} の声をミュート。'

            elif voice1 == "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0":
                text = f'{name} has muted their voice.'
    
            engine.save_to_file(text , f'sound\{name}_mute.mp3')
            engine.runAndWait()
            save = f"{name}_mute.mp3"
       
            url = r"sound\{}".format(save)
            track1 = await self.bot.wavelink.get_tracks(engine.say('hello'))
            await player.play(track1[0])
            while player.is_playing:
                await asyncio.sleep(1)
            os.system(f'del /f "\sound\{save}"')
        
        
        #---Player Unmute---#
        elif before.self_mute is True and after.self_mute is False:
            """unmute function"""
            name = member.name
            if voice.name == "Microsoft Haruka Desktop - Japanese":
                text = f'{name} の声をアンミュート。'

            elif voice.name == "Microsoft Zira Desktop - English (United States)":
                text = f'{name} has unmuted their voice'

            engine.save_to_file(text , f'sound\{name}_unmute.mp3')
            engine.runAndWait()
            save = f"{name}_unmute.mp3"

            url = r"sound\{}".format(save)
            track1 = await self.bot.wavelink.get_tracks(url)
            await player.play(track1[0])
            while player.is_playing:
                await asyncio.sleep(1)
            os.system(f'del /f "sound\{save}"')
        
        
        #---Player Deaf---#
        elif before.self_deaf is False and after.self_deaf is True:
            """deaf function"""
            name = member.name

            if voice.name == "Microsoft Haruka Desktop - Japanese":
                text = f'{name} わ声が聞こえないになりました。'

            elif voice.name == "Microsoft Zira Desktop - English (United States)":
                text = f'{name} has become a deaf mute.'
                
            engine.save_to_file(text , f'sound\{name}_deaf.mp3')
            engine.runAndWait()
            save = f"{name}_deaf.mp3"

            url = r"sound\{}".format(save)
            track1 = await self.bot.wavelink.get_tracks(url)
            await player.play(track1[0])
            os.system(f'del /f "sound\{save}"')
        

        #---Player Undeaf---#
        elif before.self_deaf is True and after.self_deaf is False:
            """undeaf function"""
            name = member.name
            if voice.name == "Microsoft Haruka Desktop - Japanese":
                text = f'{name} わ声が聞こえます。'

            elif voice.name == "Microsoft Zira Desktop - English (United States)":
                text = f'{name} has become normal.'
                
            engine.save_to_file(text , f'sound\{name}_undeaf.mp3')
            engine.runAndWait()
            save = f"{name}_undeaf.mp3"

            url = r"sound\{}".format(save)
            track1 = await self.bot.wavelink.get_tracks(url)
            await player.play(track1[0])
            os.system(f'del /f "sound\{save}"')


    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.activities is not None and after.activities is not None:
            print(after.activities)


#---Custom Command Section---#

class context(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

   # @commands.command(aliases=['s', 'solve'])
   # async def solves(self, ctx, *, query: str):
   #     txt = ''
     #   for i in query:
     #       txt = query.replace('+', ' plus ')
    #    res = client.query(txt, scantimeout=6, podstate='Step-by-step solution', format='plaintext')

    #    await ctx.send(next(res.results).text)
        #    for i in l:
   #     #    if 'Solutions' or 'solutions' or 'solution' or 'Solution' in i:
        #       print(i)
 #       for pod in res.pods:
   #         for sub in pod.subpods:
    #            if sub.title == 'Possible intermediate steps':
      #              await ctx.send(f'Solutions: \n {sub.plaintext}')
#
    @commands.command(aliases=['cl'])
    async def clear(self, ctx):
        channel = ctx.message.channel
        async for message in channel.history(limit=50):
            await message.delete()


    #---Play Text Command---#
    @commands.command(aliases=['pt'])
    async def playtext(self, ctx, *, text :str):

        player = self.bot.wavelink.get_player(ctx.guild.id)
        name = ctx.author.name
        
        if voice.name == "Microsoft Haruka Desktop - Japanese":
            word = name + ' わ ' + text + 'と言った。'

        elif voice.name == "Microsoft Zira Desktop - English (United States)":
            word = name + ' say ' + text

        engine.save_to_file(word, f'sound\{name}_type.mp3')
        engine.runAndWait()

        save = f'{name}_type.mp3'

        url = r"sound\{}".format(save)
        track1 = await self.bot.wavelink.get_tracks(url)
        await player.play(track1[0])
        while player.is_playing:
                await asyncio.sleep(1)
        os.system(f'del /f "{save}"')



    @commands.command()
    async def moverole(self, ctx, role: discord.Role, position: int):
        try:
            await role.edit(position=position)
            await ctx.send("Role moved.")
        except discord.Forbidden:
            await ctx.send("You do not have permission to do that")
        except discord.HTTPException:
            await ctx.send("Failed to move role")
        except discord.InvalidArgument:
            await ctx.send("Invalid argument")

    @commands.command()
    async def addrole(self, ctx, *, name: str):
        member = ctx.message.author
        role = get(member.guild.roles, name=name)
        await member.add_roles(role)

    #---Change language to english and japan Command---#
    @commands.command(aliases=['lg'])
    async def changelanguge(self, ctx, *, text :str):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        name = ctx.author.name

        if text == "en":
            engine = pyttsx3.init()
            rate = engine.getProperty('rate')
            engine.setProperty('rate', rate)
            voices = engine.getProperty('voices')
            for voice in voices:
                if voice.name == 'Microsoft Zira Desktop - English (United States)':
                    engine.setProperty('voice', voice.id)
                    word = name + ' Just change language to English '
                    engine.save_to_file(word, f'sound\{name}_type.mp3')
                    engine.runAndWait()

        #---Change language to Japan Command---#
        elif text == "jp":
            engine = pyttsx3.init()#pyttsx3 init
            rate = engine.getProperty('rate')
            engine.setProperty('rate', rate)
            voices = engine.getProperty('voices')
            for voice in voices:
                if voice.name == 'Microsoft Haruka Desktop - Japanese':
                    engine.setProperty('voice', voice.id)
                    word = name + ' は日本語が変わりました。'
                    engine.save_to_file(word, f'sound\{name}_type.mp3')
                    engine.runAndWait()


        save = f'{name}_type.mp3'

        url = r"sound\{}".format(save)
        track1 = await self.bot.wavelink.get_tracks(url)
        await player.play(track1[0])
        while player.is_playing:
            await asyncio.sleep(1)
        os.system(f'del /f "{save}"')
        


bot = Bot()
bot.run(input())