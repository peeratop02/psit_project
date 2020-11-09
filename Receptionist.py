import discord
import asyncio
import wavelink
from time import sleep
from discord.ext import commands, tasks

import pyttsx3
import os


from discord.utils import get

channels = []

#---Set narrator language---#

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


        #---Player Join---#
        if before.channel is None and after.channel is not None:
            channel = member.voice.channel
            #print(member.activities)
            if not player.is_connected:
                await player.connect(channel.id)
                channels.append(channel.id)

            
            name = member.name
            text = f'{name} を入ります。'
            engine.save_to_file(text , f'sound\{name}_join.mp3')
            engine.runAndWait()
            save = f"{name}_join.mp3"

            url = r"sound\{}".format(save)
            track1 = await self.bot.wavelink.get_tracks(url)
            await player.play(track1[0])
            while player.is_playing:
                await sleep(1)
            os.system(f'del /f "{save}"')


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
            text = f'{name} の声をミュート。'
            engine.save_to_file(text , f'sound\{name}_mute.mp3')
            engine.runAndWait()
            save = f"{name}_mute.mp3"

            url = r"sound\{}".format(save)
            track1 = await self.bot.wavelink.get_tracks(url)
            await player.play(track1[0])
            while player.is_playing:
                await sleep(1)
            os.system(f'del /f "\sound\{save}"')
        
        
        #---Player Unmute---#
        elif before.self_mute is True and after.self_mute is False:
            """unmute function"""
            name = member.name
            text = f'{name} の声をアンミュート。'
            engine.save_to_file(text , f'sound\{name}_unmute.mp3')
            engine.runAndWait()
            save = f"{name}_unmute.mp3"

            url = r"sound\{}".format(save)
            track1 = await self.bot.wavelink.get_tracks(url)
            await player.play(track1[0])
            while player.is_playing:
                await sleep(1)
            os.system(f'del /f "sound\{save}"')
        
        
        #---Player Deaf---#
        elif before.self_deaf is False and after.self_deaf is True:
            """deaf function"""
            name = member.name
            text = f'{name} わ声が聞こえないになりました。'
            engine.save_to_file(text , f'sound\{name}_deaf.mp3')
            engine.runAndWait()
            save = f"{name}_deaf.mp3"

            url = r"sound\{}".format(save)
            track1 = await self.bot.wavelink.get_tracks(url)
            await player.play(track1[0])
            while player.is_playing:
                await sleep(1)
            os.system(f'del /f "sound\{save}"')
        

        #---Player Undeaf---#
        elif before.self_deaf is True and after.self_deaf is False:
            """undeaf function"""
            name = member.name
            text = f'{name} わ声が聞こえます。'
            engine.save_to_file(text , f'sound\{name}_undeaf.mp3')
            engine.runAndWait()
            save = f"{name}_undeaf.mp3"

            url = r"sound\{}".format(save)
            track1 = await self.bot.wavelink.get_tracks(url)
            await player.play(track1[0])
            while player.is_playing:
                await sleep(1)
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

        word = name + ' わ ' + text + 'と言った。'
        engine.save_to_file(word, f'sound\{name}_type.mp3')
        engine.runAndWait()

        save = f'{name}_type.mp3'

        url = r"sound\{}".format(save)
        track1 = await self.bot.wavelink.get_tracks(url)
        await player.play(track1[0])
        while player.is_playing:
            await sleep(1)
        os.system(f'del /f "{save}"')
    
    
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


bot = Bot()
bot.run(input())
