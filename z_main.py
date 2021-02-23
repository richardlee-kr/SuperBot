import asyncio, discord, time
from ydl import *
from dice import *
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

mp3List = returnList()

@bot.event
async def on_ready():
    print("I have logged in as {0.user}".format(bot))

@bot.command()
async def 안녕(ctx):
    await ctx.send("안녕")

@bot.command()
async def 도움(ctx):
    embed = discord.Embed(title = "Super Bot", description = "만능 봇이 될 예정", color = 0x6E17E3) 
    embed.add_field(name = "도움말", value = bot.command_prefix + "도움", inline = False)
    embed.add_field(name = "만든 놈 ", value = "[http://lektion-von-erfolglosigkeit.tistory.com/](<http://lektion-von-erfolglosigkeit.tistory.com/>)", inline = False)
    await ctx.send(embed=embed)

@bot.command()
async def 주사위(ctx):
    result, _color, bot1, bot2, user1, user2, a, b = dice()

    embed = discord.Embed(title = "주사위 게임 결과", description = None, color = _color)
    embed.add_field(name = "Super Bot의 숫자 " + bot1 + "+" + bot2, value = ":game_die: " + a, inline = False)
    embed.add_field(name = ctx.author.name+"의 숫자 " + user1 + "+" + user2, value = ":game_die: " + b, inline = False)
    embed.set_footer(text="결과: " + result)
    await ctx.send(embed=embed)

#@bot.command()
#async def join(ctx):
    #if ctx.author.voice and ctx.author.voice.channel:
    #    channel = ctx.author.voice.channel
    #    await channel.connect()
    #else:
    #    await ctx.send("음성채널 없음")

#@bot.command()
#async def leave(ctx):
    #voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    #if voice.is_connected():
    #    await voice.disconnect()
    #else:
    #    await ctx.send("음성채널 없음")
    
    #await bot.voice_clients[0].disconnect()

@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("재성중인 곡 없음")

@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("일시정지 아님")

@bot.command()
async def leave(ctx):
    mp3List = []
    await bot.voice_clients[0].disconnect()
    #voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    #if voice.is_connected():
    #    await voice.disconnect()

@bot.command()
async def skip(ctx):
    voice.stop()

    #if len(mp3List) > 1:

    #    printList()
    #    delelteFile()
    #    del mp3List[0]
    #    printList()
    #else:
    #    printList()
    #    deleteFile()
    #    printList()
    #    print("채널에서 나갑니다.")
    #    await bot.voice_clients[0].disconnect()

    #voice.stop()
    #try:
    #    deleteFile()
    #    del mp3List[0]
    #    print(mp3List[0] + "스킵")
    #except:
    #    print("error: 삭제 실패 (스킵)")
    #finally:
    #    delelteFile()
    #    del mp3List[0]
    #    printList()

    #    if mp3List == None:
    #        await bot.voice_clients[0].disconnect()
    #    else:
    #        voice.play(discord.FFmpegPCMAudio(executable = './ffmpeg/bin/ffmpeg.exe', source=mp3List[0]))

    #voice.stop()
    #print("정지")
    #printList()
    #deleteFile()
    #del mp3List[0]
    #print("스킵")
    #printList()

@bot.command()
async def play(ctx, url):
    #사용자의 음성채널에 접속
    channel = ctx.message.author.voice.channel
    global voice
    voice = await channel.connect()

    ydl(url) #음원 다운
    Scan() #mp3파일 스캔 후 mp3List에 추가
    print("현재 재생목록")
    printList() #재생목록 확인


    voice.play(discord.FFmpegPCMAudio(executable = './ffmpeg/bin/ffmpeg.exe', source=mp3List[0]))


    while voice.is_playing() and mp3List != None:
        await asyncio.sleep(.1)
    print("끝")

    while len(mp3List) > 1:
        print("재생목록이 남아있습니다.")
        voice.stop()

        print("삭제전 재생목록")
        printList()

        print("[0] 파일 삭제")
        try:
            delelteFile()
        except:
            print("error:파일삭제 실패")

        print("[0] list 삭제")
        del mp3List[0]

        print("삭제 후 재생목록")
        printList() 

        print("다음 곡 재생")
        voice.play(discord.FFmpegPCMAudio(executable = './ffmpeg/bin/ffmpeg.exe', source=mp3List[0]))
        while voice.is_playing() and mp3List != None:
            await asyncio.sleep(.1)

    print("남아있는 재생목록 없음")
    print("삭제 전 재생목록")
    printList()

    try:
        deleteFile()
    except:
        print("error:파일삭제 실패")

    print("[0] list 삭제")
    del mp3List[0]

    print("삭제 후 재생목록")
    printList()

    print("삭제 완료")

    print("채널에서 나갑니다.")
    await bot.voice_clients[0].disconnect()


    #voice.stop()

    #try:
    #    delelteFile()
    #    del mp3List[0]
    #    print("재생" + mp3List[0])
    #except:
    #    print("error: 삭제 실패 (노래끝)")
    #finally:
    #    voice.stop()
    #    delelteFile()
    #    del mp3List[0]
    #    print("노래끝")
    #    printList()


    #    if mp3List == None:
    #        await bot.voice_clients[0].disconnect()
    #    else:
    #        voice.play(discord.FFmpegPCMAudio(executable = './ffmpeg/bin/ffmpeg.exe', source=mp3List[0]))



@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("명령어를 찾지 못했습니다")

bot.run("Nzk0NDMzMTgzNjYzMTI4NjE2.X-6vjg.40Wtu0bCgSRo_aE3Ojtj2vm8peI")
