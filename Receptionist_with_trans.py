from math import dist
import discord #-Import Discord Library
import asyncio #-Import Asyncio Library
import wavelink #-Import Wavelink Library
import os #-Import OS
import urllib #-Import Url Converter Library
import googletrans #Import Google


from discord.ext import commands, tasks
from discord.utils import get
from googletrans import Translator, constants
from time import sleep

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
            if int(member.id) == 195500932442750976: #change id here#
                url = r"sound\baka.mp3"
                track1 = await self.bot.wavelink.get_tracks(url)
                await player.play(track1[0])
            
            else:
                name = member.name
                language=get_language(int(member.guild.id))

                #---Japanese Language---#
                if language=='ja':
                    jap = f'{name} wahairimasu'
                    text = urllib.parse.quote_plus(jap)

                #---English Language---#
                elif language=='en':
                    text = f'{name}%20has%20joined%20your%20channel'

                #---Thai Language---#
                else:
                    thai = f'{name} ได้เข้าช่องสนทนานี้แล้ว'
                    text = urllib.parse.quote_plus(thai)
                    language = 'th'

                #---Play File From URL---#
                url = f'https://translate.google.com/translate_tts?ie=UTF-8&q={text}&tl={language}&ttsspeed=0.5&total=1&idx=0&client=tw-ob&textlen=5&tk=316070.156329'
                track1 = await self.bot.wavelink.get_tracks(url)
                await player.play(track1[0])



        #---Custom Player Sound---#
        elif before.channel is not None and after.channel is None and int(member.id) == 372762649118638082:
            url = r"/home/diswave/NaiNuey.m4a"
            track1 = await self.bot.wavelink.get_tracks(url)
            await player.play(track1[0])
        

        #---Not Working---#
        elif before.channel is None and after.channel is not None and int(member.id) == 336144056260231179:
            url = r"sound\baka.mp3"
            track1 = await self.bot.wavelink.get_tracks(url)
            await player.play(track1[0])


        #---Unknown---#
        elif before.channel is not None and after.channel is None and int(member.id) == 774307466720444446: 
            await player.disconnect()
        
        
        #---Player Mute---#
        elif before.self_mute is False and after.self_mute is True:
            """mute function"""
            name = member.name

            language = get_language(int(member.guild.id))


            if language=='ja':
                jap = f'{name} nokoewomyutodesu'
                text = urllib.parse.quote_plus(jap)


            elif language=='en':
                text = f'{name}%20has%20muted%20their%20voice'


            else:
                thai = f'{name} ได้ปิดเสียงตัวเอง'
                text = urllib.parse.quote_plus(thai)
                language = 'th'


            url = f'https://translate.google.com/translate_tts?ie=UTF-8&q={text}&tl={language}&ttsspeed=0.5&total=1&idx=0&client=tw-ob&textlen=5&tk=316070.156329'
            track1 = await self.bot.wavelink.get_tracks(url)
            await player.play(track1[0])
        
        
        #---Player Unmute---#
        elif before.self_mute is True and after.self_mute is False:
            """unmute function"""
            name = member.name

            language = get_language(int(member.guild.id))

            
            if language=='ja':
                jap = f'{name} nokoewoanmyutodesu'
                text=urllib.parse.quote_plus(jap)


            elif language=='en':
                text = f'{name}%20has%20unmuted%20their%20voice'

            else:
                thai = f'{name} ได้เปิดเสียงตัวเองกลับแล้ว'
                text=urllib.parse.quote_plus(thai)
                language = 'th'


            url = f'https://translate.google.com/translate_tts?ie=UTF-8&q={text}&tl={language}&ttsspeed=0.5&total=1&idx=0&client=tw-ob&textlen=5&tk=316070.156329'
            track1 = await self.bot.wavelink.get_tracks(url)
            await player.play(track1[0])
        
        
        #---Player Deaf---#
        elif before.self_deaf is False and after.self_deaf is True:
            """deaf function"""
            name = member.name

            language=get_language(int(member.guild.id))

            if language=='ja':
                jap = f'{name} wakoegakikoenaininarimashita'
                text=urllib.parse.quote_plus(jap)


            elif language=='en':
                text = f'{name}%20has%20become%20deaf%20mute'

            else:
                thai = f'{name} ได้ปิดการได้ยินตัวเอง'
                text=urllib.parse.quote_plus(thai)
                language = 'th'


            url = f'https://translate.google.com/translate_tts?ie=UTF-8&q={text}&tl={language}&ttsspeed=0.5&total=1&idx=0&client=tw-ob&textlen=5&tk=316070.156329'
            track1 = await self.bot.wavelink.get_tracks(url)
            await player.play(track1[0])
        

        #---Player Undeaf---#
        elif before.self_deaf is True and after.self_deaf is False:
            """undeaf function"""
            name = member.name

            language=get_language(int(member.guild.id))

            if language=='ja':
                jap = f'{name} wakoegakikoemasu'
                text=urllib.parse.quote_plus(jap)


            elif language=='en':
                text = f'{name}%20has%20become%20normal'

            else:
                thai = f'{name} ได้เปิดการได้ยินกลับแล้ว'
                text=urllib.parse.quote_plus(thai)
                language = 'th'


            url = f'https://translate.google.com/translate_tts?ie=UTF-8&q={text}&tl={language}&ttsspeed=0.5&total=1&idx=0&client=tw-ob&textlen=5&tk=316070.156329'
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


        language=get_language(int(ctx.guild.id))


        if language=='ja':
            jap = f'{name} wa {text} toitta'
            text=urllib.parse.quote_plus(jap)


        elif language=='en':
            eng = f'{name} say {text}'
            text = urllib.parse.quote_plus(eng)

        else:
            thai = f'{name} พูดว่า {text}'
            text=urllib.parse.quote_plus(thai)
            language = 'th'


        url = f'https://translate.google.com/translate_tts?ie=UTF-8&q={text}&tl={language}&ttsspeed=0.5&total=1&idx=0&client=tw-ob&textlen=5&tk=316070.156329'
        track1 = await self.bot.wavelink.get_tracks(url)
        await player.play(track1[0])



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
        global lang
        player = self.bot.wavelink.get_player(ctx.guild.id)
        name = ctx.author.name
        member_channel=ctx.guild.id

        def get_language(id :int):
            for item in lang:
                if str(item[:18])== str(member_channel): #
                    return str(item[19:])

        if text == "en":
            if get_language(int(member_channel)) is not None:
                for i in range(len(lang)):
                    if lang[i][:18] == str(member_channel):
                        lang[i] = f'{member_channel}:en'

            else:
                lang.append(f'{str(member_channel)}:en')

            
           
            en=name + "has changed voice to english"
            word = urllib.parse.quote_plus(en)
            url=f"https://translate.google.com/translate_tts?ie=UTF-8&q={word}&tl=en&ttsspeed=0.5&total=1&idx=0&client=tw-ob&textlen=5&tk=316070.156329"
            track1 = await self.bot.wavelink.get_tracks(url)
            await player.play(track1[0])
            print(lang)


        #---Change language to Japan Command---#
        elif text == "ja":

            if get_language(int(member_channel)) is not None:
                for i in range(len(lang)):
                    if lang[i][:18] == str(member_channel):
                        lang[i] = f'{member_channel}:ja'
                        
                        print(lang)

            else:
                lang.append(f'{str(member_channel)}:ja')

            ja= name + 'wanihongogakawarimashita'
            word =urllib.parse.quote_plus(ja)
            
            url=f"https://translate.google.com/translate_tts?ie=UTF-8&q={word}&tl=ja&ttsspeed=0.5&total=1&idx=0&client=tw-ob&textlen=5&tk=316070.156329"
            track1 = await self.bot.wavelink.get_tracks(url)
            await player.play(track1[0])
            print(lang)
        
        
        elif text == "th":

            if get_language(int(member_channel)) is not None:
               for i in range(len(lang)):
                    if lang[i][:18] == str(member_channel):
                        lang[i] = f'{member_channel}:th'

            else:
                lang.append(f'{str(member_channel)}:th')


            thai = f'{name} ได้เปลี่ยนภาษาเป็นภาษาไทย'
            word = urllib.parse.quote_plus(thai)
            url=f"https://translate.google.com/translate_tts?ie=UTF-8&q={word}&tl=th&ttsspeed=0.5&total=1&idx=0&client=tw-ob&textlen=5&tk=316070.156329"
            track1 = await self.bot.wavelink.get_tracks(url)
            await player.play(track1[0])


    #---Translate Language---#
    @commands.command(aliases=['tr'])
    async def translate_langugae(self, ctx, *, text :str):

        
        def get_language(id :int):
            for item in lang:
                if str(item[:18])== str(member_channel):
                    return str(item[19:])

        member_channel=ctx.guild.id

        player = self.bot.wavelink.get_player(ctx.guild.id)

        language=get_language(int(ctx.guild.id))


        def langTranslate(text,**kwargs):
            '''Translate Funtion'''
            translator = Translator()
            result = None
            lang = None
            
            while result == None:
                try:
                    result = translator.translate(text,**kwargs)

                except Exception as e:
                    translator = Translator()
                    sleep(0.1)
                    pass
                
            return result
            
            
        if language == 'ja':
            transLangtoEn = langTranslate(text, dist='ja')
            print(f'{transLangtoEn.text}')

        elif language == 'en':
            transLangtoEn = langTranslate(text, dist='en')
            print(f'{transLangtoEn.text}')

        else:
            language == 'th'
            transLangtoEn = langTranslate(text, dist='th')
            print(f'{transLangtoEn.text}')


    #---Play Sound---$
    @commands.command(aliases=['ps'])
    async def playsound(self, ctx, *, text :str):

        player = self.bot.wavelink.get_player(ctx.guild.id)

        if text == 'baka':
            url = r"sound\baka.mp3"

        elif text == 'hee':
            url = r"sound\hee.mp3"

        elif text == 'sawasdee':
            url = r"sound\sawasdee.mp3"

        elif text == 'senpai':
            url = r"sound\senpai_cut.mp3"

        elif text == 'dio da':
            url = r"sound\dio_da.mp3"
        
        elif text == 'wry':
            url = r"sound\wry.mp3"

        elif text == 'road roller':
            url = r"sound\road_roller.mp3"

        elif text == 'yes':
            url = r"sound\yes_yes.mp3"

        elif text == 'bruh':
            url = r"sound\bruh.mp3"

        elif text == 'simp':
            url = r"sound\davie_simp.mp3"

        elif text == 'kratuk':
            url = r"sound\kratuk_jit.mp3"

        elif text == 'dhee':
            url = r"sound\double_hee.mp3"

        elif text == 'nayok':
            url = r"sound\nayok.mp3"

        elif text == 'onii':
            url = r"sound\oniichan.mp3"

        elif text == 'fbi':
            url = r"sound\fbi.mp3"

        elif text == 'clap':
            url = r"sound\applause.mp3"
            
        elif text == 'Blackpink1':
            url = r"sound\blackpink1.mp3"
        
        elif text == 'Blackpink2':
            url = r"sound\blackpink2.mp3"

        elif text == 'Blackpink3':
            url = r"sound\blackpink3.mp3"
        
        elif text == 'Lovesick':
            url = r"sound\blackpink4.mp3"
        
        elif text == 'HYLT':
            url = r"sound\HYLT.mp3"

        elif text == 'ahh':
            url = r"sound\ahhh_1.mp3"

        track1 = await self.bot.wavelink.get_tracks(url)
        await player.play(track1[0])


bot = Bot()
bot.run(input())
