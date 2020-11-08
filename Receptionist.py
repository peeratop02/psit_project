from typing import Text
import discord
import subprocess
import asyncio
import wavelink
from discord.ext import commands, tasks

from gtts import gTTS
import pyttsx3
import os


from discord.utils import get

channels = []

class Language:


    def __init__(self):
        self.engine = self.pyttsx3.init() #pyttsx3 init
        self.rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', self.rate-30)

    def jp_type(self, name, text):
        self.name = name
        self.text = text
        self.word = self.name + ' わ ' + self.text + 'と言った。'
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if voice.name == 'Microsoft Haruka Desktop - Japanese':
                self.engine.setProperty('voice', voice.id)
        
        
        self.engine.save_to_file(self.word, f'sound\{name}_typing.mp3')
        self.engine.runAndWait()

    def jp_join(self,name):
        self.name=name

        text = f'{name} を入ります。'
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if voice.name == 'Microsoft Haruka Desktop - Japanese':
                self.engine.setProperty('voice', voice.id)

        self.engine.save_to_file(text , f'{name}_join.mp3')
        self.engine.runAndWait()
    
    def en_lang(self, name, word):
        self.name = name
        self.word = word
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if voice.name == 'Microsoft David Desktop - English':
                self.engine.setProperty('voice', voice.id)

        self.engine.save_to_file(word, f'sound\{name}_typing.mp3')
        self.engine.runAndWait()
    
    def th_lang(self, name, word):
        self.name = name
        self.word = word
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if voice.name == 'Microsoft Pattara Desktop - Thai':
                self.engine.setProperty('voice', voice.id)

        self.engine.save_to_file(word, f'sound\{name}_typing.mp3')
        self.engine.runAndWait()
            

class Bot(commands.Bot):

    

    def __init__(self):
        super(Bot, self).__init__(command_prefix=['/'])

        self.add_cog(Music(self))
        self.add_cog(context(self))

    async def on_ready(self):
        print(f'Logged in as {self.user.name} | {self.user.id}')
        await self.change_presence(status=discord.Status.online, activity=discord.Game('/connect'))


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = wavelink.Client(bot=self.bot)

        self.bot.loop.create_task(self.start_nodes())
        self.bot.remove_command("help")

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        await self.bot.wavelink.initiate_node(host='127.0.0.1',
                                              port=80,
                                              rest_uri='http://127.0.0.1:80',
                                              password='testing',
                                              identifier='TEST',
                                              region='us_central')

    @commands.command(name='connect')
    async def connect_(self, ctx, *, channel: discord.VoiceChannel = None):

        player = self.bot.wavelink.get_player(ctx.guild.id)
        channel = ctx.author.voice.channel
        await player.connect(channel.id)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        player = self.bot.wavelink.get_player(member.guild.id)
        if before.channel is None and after.channel is not None:
            channel = member.voice.channel
            #print(member.activities)
            if not player.is_connected:
                await player.connect(channel.id)
                channels.append(channel.id)

            
            name = member.name
            
            Language.jp_join(name)

            url = r"C:\Users\ASUS G14\Documents\psit_project\sound\{}".format(save)
            track1 = await self.bot.wavelink.get_tracks(url)
            await player.play(track1[0])
            while player.is_playing:
                await asyncio.sleep(1)
            os.system(f'del /f "sound\{save}"')
        elif before.channel is not None and after.channel is None and int(member.id) == 372762649118638082:
            url = r"/home/diswave/NaiNuey.m4a"
            track1 = await self.bot.wavelink.get_tracks(url)
            await player.play(track1[0])

        elif before.channel is not None and after.channel is None and int(member.id) == 755072422738133113:
            await player.disconnect()
        elif before.self_mute is False and after.self_mute is True:
            name = member.name
            text = f'{name} の声をミュート。'
            engine.save_to_file(text , f'sound\{name}_mute.mp3')
            engine.runAndWait()
            save = f"{name}_mute.mp3"

            url = r"C:\Users\ASUS G14\Documents\psit_project\sound\{}".format(save)
            track1 = await self.bot.wavelink.get_tracks(url)
            await player.play(track1[0])
            while player.is_playing:
                await asyncio.sleep(1)
            os.system(f'del /f "sound\{save}"')
        elif before.self_deaf is False and after.self_deaf is True:
            name = member.name
            text = f'{name} has become a deaf mute'
            engine.save_to_file(text , f'sound\{name}_deaf.mp3')
            engine.runAndWait()
            save = f"{name}_deaf.mp3"

            url = r"C:\Users\ASUS G14\Documents\psit_project\sound\{}".format(save)
            track1 = await self.bot.wavelink.get_tracks(url)
            await player.play(track1[0])
            os.system(f'del /f "sound\{save}"')

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.activities is not None and after.activities is not None:
            print(after.activities)


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

    @commands.command(aliases=['pt'])
    async def playtext(self, ctx, *, text :str):

        player = self.bot.wavelink.get_player(ctx.guild.id)
        name = ctx.author.name
        
        Language.jp_type(self, name, text)

        save = f"{name}_typing.mp3"

        url = r"C:\Users\ASUS G14\Documents\psit_project\sound\{}".format(save)
        track1 = await self.bot.wavelink.get_tracks(url)
        await player.play(track1[0])
        os.system(f'del /f "sound\{save}"')

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


bot = Bot()
bot.run(input())
