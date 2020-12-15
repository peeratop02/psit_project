##___________Receptionist | A discord bot____________##
##____©2020 LnwBotZaFamily007 All Rights Reserved____##

import discord  #-Import Discord Library
import asyncio  #-Import Asyncio Library
import wavelink #-Import Wavelink Library
import os       #-Import OS
import urllib   #-Import Url Converter Library

from time import sleep                  #-Import Time Library
from discord.ext import commands, tasks #-Import more Discord Library
from discord.utils import get           #-Import more Discord Library
from googletrans import Translator      #-Import Google Translate Library

#---List Contain Channel That Bot Is Connected--#
channels = []

#---List Contain Language Settings---#
lang=[]


#---Bot Default Settings---#
class Bot(commands.Bot):


    #---Set Bot Command Prefix---#
    def __init__(self):
        super(Bot, self).__init__(command_prefix=['/'])

        self.add_cog(Music(self))
        self.add_cog(context(self))


    #---Set Bot Status---#
    async def on_ready(self):
        print(f'Logged in as {self.user.name} | {self.user.id}')
        await self.change_presence(status=discord.Status.online, activity=discord.Game(name = 'EZ-VPS.CO'))


#---Bot action---#
class Music(commands.Cog):


    #---__init__---#
    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = wavelink.Client(bot=self.bot)

        self.bot.loop.create_task(self.start_nodes())
        self.bot.remove_command("help")


    #---Setting For Connection To application.yml---#
    async def start_nodes(self):
        await self.bot.wait_until_ready()

        await self.bot.wavelink.initiate_node(host='127.0.0.1',
                                              port=80,
                                              rest_uri='http://127.0.0.1:80',
                                              password='testing',
                                              identifier='TEST',
                                              region='us_central')


    #---/Connect Command---#
    @commands.command(name='connect')
    async def connect_(self, ctx, *, channel: discord.VoiceChannel = None):

        player = self.bot.wavelink.get_player(ctx.guild.id)
        channel = ctx.author.voice.channel
        await player.connect(channel.id)

    #---Disconnect Command---#
    @commands.command(aliases=['leave'])
    async def disconnect(self, ctx):

        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.disconnect()


    #---Member Action Section---#
    @commands.Cog.listener()

    #---Member Interaction Section---#
    async def on_voice_state_update(self, member, before, after):

        #---Get Channel ID---#
        member_channel=member.guild.id

        #---Get Language From Lang---#
        def get_language(id :int):
            for item in lang:
                if str(item[:18])== str(member_channel):
                    return str(item[19:])


        #---Get Player ID---#
        player = self.bot.wavelink.get_player(member.guild.id)


        #---Player Join---#
        if before.channel is None and after.channel is not None:
            channel = member.voice.channel
            #print(member.activities)
            if not player.is_connected:
                await player.connect(channel.id)
                channels.append(channel.id)


        #---Call People With ID Or Not---#
            if int(member.id) == 1: #change id here#
                url = r"sound\baka.mp3"
                track1 = await self.bot.wavelink.get_tracks(url)
                await player.play(track1[0])


        #---Default Join Setting---#
            else:
                name = member.name
                language=get_language(int(member.guild.id))

                #---Japanese Language---#
                if language=='ja':
                    jap = f'{name} ははいります'
                    speed = '1.2'
                    text = urllib.parse.quote_plus(jap)

                #---English Language---#
                elif language=='en':
                    speed = '1.2'
                    text = f'{name}%20has%20joined%20your%20channel'

                #---Thai Language---#
                else:
                    thai = f'{name} ได้เข้าช่องสนทนานี้แล้ว'
                    text = urllib.parse.quote_plus(thai)
                    speed = '2'
                    language = 'th'

                #---Play File From URL---#
                url = f'https://translate.google.com/translate_tts?ie=UTF-8&q={text}&tl={language}&ttsspeed={speed}&total=1&idx=0&client=tw-ob&textlen=5&tk=316070.156329'
                track1 = await self.bot.wavelink.get_tracks(url)
                await player.play(track1[0])


        #---Custom Player Sound---#
        elif before.channel is not None and after.channel is None and int(member.id) == 372762649118638082:
            url = r"/home/diswave/NaiNuey.m4a"
            track1 = await self.bot.wavelink.get_tracks(url)
            await player.play(track1[0])


        #---Not working---#
        elif before.channel is not None and after.channel is None and int(member.id) == 336144056260231179: 
            await player.disconnect


        #---Player Mute---#
        elif before.self_mute is False and after.self_mute is True:
            """mute function"""
            name = member.name

            language = get_language(int(member.guild.id))


            if language=='ja':
                
                jap = f'{name} のこえをミュートです'
                speed = '1.5'
                text = urllib.parse.quote_plus(jap)


            elif language=='en':
                
                speed = '1.5'
                text = f'{name}%20has%20muted%20their%20voice'


            else:
                thai = f'{name} ได้ปิดเสียงตัวเอง'
                speed = '2'
                text = urllib.parse.quote_plus(thai)
                language = 'th'



        #---Player Unmute---#
        elif before.self_mute is True and after.self_mute is False:
            """unmute function"""
            name = member.name

            language = get_language(int(member.guild.id))

            
            if language=='ja':
                jap = f'{name} のこえをアンミュートです'
                speed = '1.5'
                text = urllib.parse.quote_plus(jap)


            elif language=='en':
                speed = '1.5'
                text = f'{name}%20has%20unmuted%20their%20voice'

            else:
                thai = f'{name} ได้เปิดเสียงตัวเองกลับแล้ว'
                speed = '2'
                text = urllib.parse.quote_plus(thai)
                language = 'th'



        #---Player Deaf---#
        elif before.self_deaf is False and after.self_deaf is True:
            """deaf function"""
            name = member.name

            language=get_language(int(member.guild.id))

            if language=='ja':
                jap = f'{name} はこえがきこえないになります'
                speed = '1.2'
                text = urllib.parse.quote_plus(jap)


            elif language=='en':
                speed = '1.2'
                text = f'{name}%20has%20become%20deaf%20mute'

            else:
                thai = f'{name} ได้ปิดการได้ยินตัวเอง'
                speed = '2'
                text = urllib.parse.quote_plus(thai)
                language = 'th'



        #---Player Undeaf---#
        elif before.self_deaf is True and after.self_deaf is False:
            """undeaf function"""
            name = member.name

            language=get_language(int(member.guild.id))

            if language=='ja':
                jap = f'{name} はこえがきこえます'
                speed = '1.2'
                text = urllib.parse.quote_plus(jap)


            elif language=='en':
                speed = '1.2'
                text = f'{name}%20has%20become%20normal'

            else:
                thai = f'{name} ได้เปิดการได้ยินกลับแล้ว'
                speed = '2'
                text=urllib.parse.quote_plus(thai)
                language = 'th'



        #---Play Sound From URL---#
        url = f'https://translate.google.com/translate_tts?ie=UTF-8&q={text}&tl={language}&ttsspeed={speed}&total=1&idx=0&client=tw-ob&textlen=5&tk=316070.156329'
        track1 = await self.bot.wavelink.get_tracks(url)
        await player.play(track1[0])    


    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.activities is not None and after.activities is not None:
            print(after.activities)


#---Custom Command Section---#

class context(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #---Clear Messages---#
    @commands.command(aliases=['cl'])
    async def clear(self, ctx):
        channel = ctx.message.channel
        async for message in channel.history(limit=50):
            await message.delete()


    #---Play Text Command---#
    @commands.command(aliases=['pt'])
    async def playtext(self, ctx, *, text :str):

        def get_language(id :int):
            for item in lang:
                if str(item[:18])== str(member_channel):
                    return str(item[19:])
        
        member_channel=ctx.guild.id

        player = self.bot.wavelink.get_player(ctx.guild.id)
        name = ctx.author.name


        language = get_language(int(ctx.guild.id))


        if language=='ja':
            jap = f'{name} は {text} といった'
            speed = '1.2'
            text=urllib.parse.quote_plus(jap)


        elif language=='en':
            eng = f'{name} say {text}'
            speed = '1.2'
            text = urllib.parse.quote_plus(eng)

        else:
            thai = f'{name} พูดว่า {text}'
            speed = '2'
            text=urllib.parse.quote_plus(thai)
            language = 'th'


        url = f'https://translate.google.com/translate_tts?ie=UTF-8&q={text}&tl={language}&ttsspeed={speed}&total=1&idx=0&client=tw-ob&textlen=5&tk=316070.156329'
        track1 = await self.bot.wavelink.get_tracks(url)
        await player.play(track1[0])


    #---Role Change Annoucement---#
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


    #---Add Role Function---#
    @commands.command()
    async def addrole(self, ctx, *, name: str):
        member = ctx.message.author
        role = get(member.guild.roles, name=name)
        await member.add_roles(role)


    #---Change language to english and japan Command---#
    @commands.command(aliases=['lg'])
    async def changelanguge(self, ctx, *, text :str):
        global lang
        player = self.bot.wavelink.get_player(ctx.guild.id)
        name = ctx.author.name
        member_channel=ctx.guild.id
        

        def get_language(id :int):
            for item in lang:
                if str(item[:18])== str(member_channel): #
                    return str(item[19:])


        #---Change language to English---#
        if text == "en":
            if get_language(int(member_channel)) is not None:
                for i in range(len(lang)):
                    if lang[i][:18] == str(member_channel):
                        lang[i] = f'{member_channel}:en'

            else:
                lang.append(f'{str(member_channel)}:en')


            en = name + "has changed voice to english"
            speed = '1.2'
            word = urllib.parse.quote_plus(en)
            url=f"https://translate.google.com/translate_tts?ie=UTF-8&q={word}&tl=en&ttsspeed={speed}&total=1&idx=0&client=tw-ob&textlen=5&tk=316070.156329"
            track1 = await self.bot.wavelink.get_tracks(url)
            await player.play(track1[0])


        #---Change language to Japan---#
        elif text == "ja":

            if get_language(int(member_channel)) is not None:
                for i in range(len(lang)):
                    if lang[i][:18] == str(member_channel):
                        lang[i] = f'{member_channel}:ja'
                        
                        print(lang)


            else:
                lang.append(f'{str(member_channel)}:ja')

            ja= name + 'はにほんごをかわります'
            speed = '1.2'
            word = urllib.parse.quote_plus(ja)

            url=f"https://translate.google.com/translate_tts?ie=UTF-8&q={word}&tl=ja&ttsspeed={speed}&total=1&idx=0&client=tw-ob&textlen=5&tk=316070.156329"
            track1 = await self.bot.wavelink.get_tracks(url)
            await player.play(track1[0])
            print(lang)


        #---Change language to Thai---#
        elif text == "th":

            if get_language(int(member_channel)) is not None:
               for i in range(len(lang)):
                    if lang[i][:18] == str(member_channel):
                        lang[i] = f'{member_channel}:th'

            else:
                lang.append(f'{str(member_channel)}:th')


            thai = f'{name} ได้เปลี่ยนภาษาเป็นภาษาไทย'
            speed = '1.8'
            word = urllib.parse.quote_plus(thai)


            url=f"https://translate.google.com/translate_tts?ie=UTF-8&q={word}&tl=th&ttsspeed={speed}&total=1&idx=0&client=tw-ob&textlen=5&tk=316070.156329"
            track1 = await self.bot.wavelink.get_tracks(url)
            await player.play(track1[0])


#---Translate Language---#
    @commands.command(aliases=['tr'])
    async def translate_langugae(self, ctx, *, text :str):


        def get_language(id :int):
            for item in lang:
                if str(item[:18]) == str(member_channel):
                    return str(item[19:])

        member_channel = ctx.guild.id

        player = self.bot.wavelink.get_player(ctx.guild.id)

        language = get_language(int(ctx.guild.id))


        def trans_lang(text, **kwargs):
            lang = None
            translator = Translator()
            while lang == None:
                try:
                    lang = translator.translate(text, **kwargs)
                except Exception as error:
                    translator = Translator()
                    sleep(0.2)
                    pass

            return lang

        if language == 'ja':
            jap_lang = trans_lang(text, dest='ja').text
            speed = 1.2
            text = urllib.parse.quote_plus(jap_lang)

        elif language == 'en':
            eng_lang = trans_lang(text, dest='en').text
            speed = 1.2
            text = urllib.parse.quote_plus(eng_lang)
        
        else:
            language == 'th'
            th_lang = trans_lang(text, dest='th').text
            speed = 2
            text = urllib.parse.quote_plus(th_lang)

        url = f'https://translate.google.com/translate_tts?ie=UTF-8&q={text}&tl={language}&ttsspeed={speed}&total=1&idx=0&client=tw-ob&textlen=5&tk=316070.156329'
        track1 = await self.bot.wavelink.get_tracks(url)
        await player.play(track1[0])

    #---Play Sound---$
    @commands.command(aliases=['ps'])
    async def playsound(self, ctx, *, text :str):

        player = self.bot.wavelink.get_player(ctx.guild.id)

        url = r"sound\%s.mp3" %text

        """
        Example Sound
        - yeet      | play Yeet sfx
        - blackpink | play blackpink sound
        - kratuk    | play professor daeng dhamma word
        - dia da    | KONO DIO DA!!!!!
        - bruh      | play bruh sfx
        and much more sfx you can find out!
        """

        track1 = await self.bot.wavelink.get_tracks(url)
        await player.play(track1[0])


#---Run---#
bot = Bot()
bot.run(input())
