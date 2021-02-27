import asyncio, discord, time 
from ydl import *
from game import *
from user import *
from discord.ext import commands

bot = commands.Bot(command_prefix="!")
token = open("token.txt", "r").readline()


@bot.event
async def on_ready():
    print("I have logged in as {0.user}\n".format(bot))

@bot.command()
async def 안녕(ctx):
    await ctx.send("안녕")

@bot.command()
async def 도움(ctx):
    embed = discord.Embed(title = "Super Bot", description = "만능 봇이 될 예정", color = 0x6E17E3) 
    embed.add_field(name = bot.command_prefix + "도움", value = "도움말을 봅니다", inline = False)
    embed.add_field(name = bot.command_prefix + "주사위", value = "주사위를 굴려 봇과 대결합니다", inline = False)
    embed.add_field(name = bot.command_prefix + "회원가입", value = "각종 컨텐츠를 즐기기 위한 회원가입을합니다", inline = False)
    embed.add_field(name = bot.command_prefix + "내정보", value = "자신의 정보를 확인합니다", inline = False)
    embed.add_field(name = bot.command_prefix + "정보 [대상]", value = "멘션한 [대상]의 정보를 확인합니다", inline = False)
    embed.add_field(name = bot.command_prefix + "송금 [대상] [돈]", value = "멘션한 [대상]에게 돈을 보냅니다", inline = False)
    embed.add_field(name = bot.command_prefix + "홀짝 [예상] [돈]", value = "홀짝게임에 [돈]을 겁니다. [예상]과 일치하면 1.5배의 수익, [돈]을 올인하면 2배의 수익을 얻습니다.", inline = False)
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
async def 홀짝(ctx, face, money):
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)
    forecast = coin()
    result = ""
    betting = 0
    _color = 0x000000
    if userExistance:
        print("DB에서 ", ctx.author.name, "을 찾았습니다.")
        if face == "홀" or face == "짝":
            #print("매개변수 홀짝 확인")
            if forecast == face:
                result = "성공"
                _color = 0x00ff56
                print(result)

                if money == "올인":
                    #print("올인함")
                    betting = getMoney(ctx.author.name, userRow)
                    print("배팅금액: ", betting)
                    print("")

                    modifyMoney(ctx.author.name, userRow, betting)
                else:
                    #print("올인 안함")
                    betting = int(money)
                    print("배팅금액: ", betting)
                    print("")

                    modifyMoney(ctx.author.name, userRow, 0.5*betting)
            else:
                #print("실패함")
                result = "실패"
                _color = 0xFF0000
                print(result)

                if money == "올인":
                    #print("올인함")
                    betting = getMoney(ctx.author.name, userRow)
                    print("배팅금액: ", betting)
                    print("")
                else:
                    betting = int(money)
                    print("배팅금액: ", betting)
                    print("")

                modifyMoney(ctx.author.name, userRow, -int(betting))
                addLoss(ctx.author.name, userRow, int(betting))

            #print("결과 도출")
            embed = discord.Embed(title = "홀짝게임 결과", description = result, color = _color)
            #print("embed 추가")
            embed.add_field(name = "배팅금액", value = betting, inline = False)
            #print("배팅 금액 추가")
            embed.add_field(name = "현재 자산", value = getMoney(ctx.author.name, userRow), inline = False)
            #print("현재 자산 추가")

            await ctx.send(embed=embed)

        else:
            print("잘못된 매개변수: ", face)
            await ctx.send("홀 또는 짝을 입력하세요")
    else:
        print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
        await ctx.send("홀짝게임은 회원가입 후 이용 가능합니다.")

    print("------------------------------\n")


@bot.command()
async def 회원가입(ctx):
    #print(ctx.author.name)
    #print(ctx.author.id)
    print("회원가입이 가능한지 확인합니다.")
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)
    if userExistance:
        print("DB에서 ", ctx.author.name, "을 찾았습니다.")
        print("------------------------------\n")
        await ctx.send("이미 가입하셨습니다.")
    else:
        print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
        print("")

        Signup(ctx.author.name, ctx.author.id)

        print("회원가입이 완료되었습니다.")
        print("------------------------------\n")
        await ctx.send("회원가입이 완료되었습니다.")

@bot.command()
async def 탈퇴(ctx):
    print("탈퇴가 가능한지 확인합니다.")
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)
    if userExistance:
        DeleteAccount(userRow)
        print("탈퇴가 완료되었습니다.")
        print("------------------------------\n")

        await ctx.send("탈퇴가 완료되었습니다.")
    else:
        print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
        print("------------------------------\n")

        await ctx.send("등록되지 않은 사용자입니다.")
        

@bot.command()
async def 내정보(ctx):
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)

    if not userExistance:
        print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
        print("------------------------------\n")
        await ctx.send("회원가입 후 자신의 정보를 확인할 수 있습니다.")
    else:
        level, money, loss = userInfo(userRow)
        print("------------------------------\n")
        embed = discord.Embed(title="유저 정보", description = ctx.author.name, color = 0x62D0F6)
        embed.add_field(name = "레벨", value = level)
        embed.add_field(name = "보유 자산", value = money)
        embed.add_field(name = "도박으로 날린 돈", value = loss, inline = False)

        await ctx.send(embed=embed)

@bot.command()
async def 정보(ctx, user: discord.User):
    userExistance, userRow = checkUser(user.name, user.id)

    if not userExistance:
        print("DB에서 ", user.name, "을 찾을 수 없습니다")
        print("------------------------------\n")
        await ctx.send(user.name  + " 은(는) 등록되지 않은 사용자입니다.")
    else:
        money, level = userInfo(userRow)
        print("------------------------------\n")
        embed = discord.Embed(title="유저 정보", description = user.name, color = 0x62D0F6)
        embed.add_field(name = "레벨", value = level)
        embed.add_field(name = "보유 자산", value = money)
        await ctx.send(embed=embed)

@bot.command()
async def 송금(ctx, user: discord.User, money):
    print("송금이 가능한지 확인합니다.")
    senderExistance, senderRow = checkUser(ctx.author.name, ctx.author.id)
    receiverExistance, receiverRow = checkUser(user.name, user.id)

    if not senderExistance:
        print("DB에서", ctx.author.name, "을 찾을수 없습니다")
        print("------------------------------\n")
        await ctx.send("회원가입 후 송금이 가능합니다.")
    elif not receiverExistance:
        print("DB에서 ", user.name, "을 찾을 수 없습니다")
        print("------------------------------\n")
        await ctx.send(user.name  + " 은(는) 등록되지 않은 사용자입니다.")
    else:
        print("송금하려는 돈: ", money)

        s_money = getMoney(ctx.author.name, senderRow)
        r_money = getMoney(user.name, receiverRow)

        if s_money >= int(money) and int(money) != 0:
            print("돈이 충분하므로 송금을 진행합니다.")
            print("")

            remit(ctx.author.name, senderRow, user.name, receiverRow, money)

            print("송금이 완료되었습니다. 결과를 전송합니다.")

            embed = discord.Embed(title="송금 완료", description = "송금된 돈: " + money, color = 0x77ff00)
            embed.add_field(name = "보낸 사람: " + ctx.author.name, value = "현재 자산: " + str(getMoney(ctx.author.name, senderRow)))
            embed.add_field(name = "→", value = ":moneybag:")
            embed.add_field(name="받은 사람: " + user.name, value="현재 자산: " + str(getMoney(user.name, receiverRow)))
                    
            await ctx.send(embed=embed)
        elif int(money) == 0:
            await ctx.send("0원을 보낼 필요는 없죠")
        else:
            print("돈이 충분하지 않습니다.")
            print("송금하려는 돈: ", money)
            print("현재 자산: ", s_money)
            await ctx.send("돈이 충분하지 않습니다. 현재 자산: " + str(s_money))

        print("------------------------------\n")


@bot.command()
async def reset(ctx):
    _reset()

@bot.command()
async def add(ctx, money):
    user, row = checkUser(ctx.author.name, ctx.author.id)
    addMoney(row, int(money))
    print("ch")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("명령어를 찾지 못했습니다. !도움을 입력하여 명령어를 확인하세요.")

bot.run(token)
