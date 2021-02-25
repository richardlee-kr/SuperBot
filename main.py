import asyncio, discord, time 
from ydl import *
from dice import *
from user import *
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print("I have logged in as {0.user}".format(bot))

@bot.command()
async def 안녕(ctx):
    await ctx.send("안녕")

@bot.command()
async def 도움(ctx):
    embed = discord.Embed(title = "Super Bot", description = "만능 봇이 될 예정", color = 0x6E17E3) 
    embed.add_field(name = bot.command_prefix + "도움", value = "도움말을 봅니다", inline = False)
    embed.add_field(name = bot.command_prefix + "주사위", value = "주사위를 굴려 봇과 대결합니다", inline = False)
    embed.add_field(name = bot.command_prefix + "회원가입", value = "게임에 참여하기 위해 회원가입을 합니다", inline = False)
    embed.add_field(name = bot.command_prefix + "내정보", value = "자신의 정보를 확인합니다", inline = False)
    embed.add_field(name = bot.command_prefix + "정보", value = "멘션한 사람의 정보를 확인합니다", inline = False)
    embed.add_field(name = bot.command_prefix + "송금", value = "멘션한 사람에게 돈을 보냅니다", inline = False)
    embed.add_field(name = bot.command_prefix + "만든 놈 ", value = "[http://lektion-von-erfolglosigkeit.tistory.com/](<http://lektion-von-erfolglosigkeit.tistory.com/>)", inline = False)
    await ctx.send(embed=embed)

@bot.command()
async def 주사위(ctx):
    result, _color, bot1, bot2, user1, user2, a, b = dice()

    embed = discord.Embed(title = "주사위 게임 결과", description = None, color = _color)
    embed.add_field(name = "Super Bot의 숫자 " + bot1 + "+" + bot2, value = ":game_die: " + a, inline = False)
    embed.add_field(name = ctx.author.name+"의 숫자 " + user1 + "+" + user2, value = ":game_die: " + b, inline = False)
    embed.set_footer(text="결과: " + result)
    await ctx.send(embed=embed)

@bot.command()
async def 회원가입(ctx):
    #print(ctx.author.name)
    #print(ctx.author.id)
    print("회원가입이 가능한지 확인합니다.")
    if findRow(ctx.author.name, ctx.author.id) == None:
        print("DB에 중복된 값이 없으므로 회원가입을 진행합니다")
        signup(ctx.author.name, ctx.author.id)
        print("회원가입이 완료되었습니다.")
        print("------------------------------\n")
        await ctx.send("회원가입이 완료되었습니다.")
    else:
        print("DB에서 중복된 값이 발견되었습니다.\n")
        print("------------------------------\n")
        await ctx.send("이미 가입하셨습니다.")

@bot.command()
async def 내정보(ctx):
    money, level = userInfo(ctx.author.name, ctx.author.id)
    
    if money == None or level == None:
        print("사용자 정보가 없습니다.")
        print("------------------------------\n")
        await ctx.send("등록되지 않은 사용자입니다.")
    else:
        print("사용자 정보 발견, 메세지를 보냅니다.")
        print("------------------------------\n")
        embed = discord.Embed(title="유저 정보", description = ctx.author.name, color = 0x62D0F6)
        embed.add_field(name = "레벨", value = level)
        embed.add_field(name = "보유 자산", value = money)
        await ctx.send(embed=embed)

@bot.command()
async def 정보(ctx, user: discord.User):
    money, level = userInfo(user.name, user.id)

    if money == None or level == None:
        print("사용자 정보가 없습니다.")
        print("------------------------------\n")
        await ctx.send("등록되지 않은 사용자입니다.")
    else:
        print("사용자 정보 발견, 메세지를 보냅니다.")
        print("------------------------------\n")
        embed = discord.Embed(title="유저 정보", description = user.name, color = 0x62D0F6)
        embed.add_field(name = "레벨", value = level)
        embed.add_field(name = "보유 자산", value = money)
        await ctx.send(embed=embed)

@bot.command()
async def reset(ctx):
    delete()

@bot.command()
async def 송금(ctx, user: discord.User, money):
    print("receiver가 존재하는지 확인합니다")
    if findRow(user.name, user.id) == None:
        print("지정된 유저는 DB에 존재하지 않습니다.")
        print("------------------------------\n")
        await ctx.send("등록되지 않는 사용자입니다.")
    else:
        print("지정된 유저를 DB에서 발견했습니다.")
        print("송금하려는 돈: ", money)

        s_money = getMoney(ctx.author.name, ctx.author.id)
        r_money = getMoney(user.name, user.id)

        if s_money >= int(money):
            print("돈이 충분하므로 송금을 진행합니다.")

            remit(ctx.author.name, ctx.author.id, user.name, user.id, money)
            print("송금이 완료되었습니다. 결과를 전송합니다.")

            embed = discord.Embed(title="송금 완료", description = "송금된 돈: " + money, color = 0x77ff00)
            embed.add_field(name = "보낸 사람: " + ctx.author.name, value = "현재 자산: " + str(getMoney(ctx.author.name, ctx.author.id)))
            embed.add_field(name = ":arrow_forward:", value = "")
            embed.add_field(name="받은 사람: " + user.name, value="현재 자산: " + str(getMoney(user.name, user.id)))
                    
            await ctx.send(embed=embed)
        else:
            print("돈이 충분하지 않습니다.")
            await ctx.send("돈이 충분하지 않습니다.")

        print("------------------------------\n")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("명령어를 찾지 못했습니다")

bot.run("your token here")

