from openpyxl import load_workbook, Workbook
import numpy as np

c_name = 1
c_id = 2
c_money = 3
c_lvl = 4

default_money = 10000

wb = load_workbook("userDB.xlsx")
ws = wb.active

def loadFile():
    wb = load_workbook("userDB.xlsx")
    ws = wb.active

def checkName(_name, _id):
    loadFile()

    print("등록된 유저수: ", ws.max_row-1)
    print("")

    print("이름과 고유번호 탐색")
    for row in range(2, ws.max_row+2):
        print(row, "번째 줄 name: ", ws.cell(row,c_name).value)
        print("입력된 name: ", _name)
        print("이름과 일치 여부: ", ws.cell(row, c_name).value == _name)

        print(row,"번째 줄 id: ", ws.cell(row,c_id).value)
        print("입력된 id: ", hex(_id))
        print("고유번호정보와 일치 여부: ", ws.cell(row, c_id).value == hex(_id))
        print("")

        if ws.cell(row, c_name).value == _name and ws.cell(row,c_id).value == hex(_id):
            print("등록된  이름과 고유번호를 발견")
            print("등록된  값의 위치: ",  row, "번째 줄")

            wb.save("userDB.xlsx")
            wb.close()

            return False
            break
        else:
            print("등록된 정보를 탐색 실패, 재탐색 실시")

    wb.save("userDB.xlsx")
    wb.close()

    return True

#def checkMoney(_name, _id, _money):
#    loadFile()
#
#    print("충분한 돈이 있는지 탐색")
#    print("송금하려는 돈: ",_money)
#    for row in range(2,ws.max_row+2):
#        if ws.cell(row,c_name).value == _name and ws.cell(row,c_id).value == _id:
#            print(_named,"의 보유 자산: ", ws.cell(row,c_money).value)
#            if ws.cell(row,c_money).value >= _money:
#                print("충분한 돈을 확인")
#                return True
#                break
#            else:
#                print("충분하지 않는 돈을 확인")
#                return False
#                break

def getMoney(_name, _id):
    loadFile()

    print("유저의 돈을 탐색중")

    for row in range(2,ws.max_row+2):
        print(row, "번째 줄 name: ", ws.cell(row,c_name).value)
        print("입력된 name: ", _name)
        print("이름과 일치 여부: ", ws.cell(row, c_name).value == _name)

        print(row,"번째 줄 id: ", ws.cell(row,c_id).value)
        print("입력된 id: ", hex(_id))
        print("고유번호정보와 일치 여부: ", ws.cell(row, c_id).value == hex(_id))
        print("")

        if ws.cell(row, c_name).value == _name and ws.cell(row,c_id).value == hex(_id):
            print(_name,"의 보유 자산: ", ws.cell(row,c_money).value)
            result = ws.cell(row,c_money).value

            wb.save("userDB.xlsx")
            wb.close()

            return result
            break
        else:
            print("재탐색")

    wb.save("userDB.xlsx")
    wb.close()

    return 0

def checkRow():
    loadFile()
    print("첫번쨰 빈 곳을 탐색")
    #for row in range(2, ws.max_row + 1):
    #    if ws.cell(row,1).value is None:
    #        return row
    #        break
    return ws.max_row+1

    wb.save("userDB.xlsx")
    wb.close()

def signup(_name, _id):
    loadFile()
    print("첫번째 빈곳: ", checkRow())
    _row = checkRow()

    print("데이터 추가 시작")
    ws.cell(row=_row, column=c_name, value=_name)
    print("이름 추가 | ",  ws.cell(_row,c_name).value)
    ws.cell(row=_row, column=c_id, value =hex(_id))
    print("고유번호 추가 | ", ws.cell(_row,c_id).value)
    ws.cell(row=_row, column=c_money, value = default_money)
    print("기본 자금 지급 | ", ws.cell(_row,c_money).value)
    ws.cell(row=_row, column=c_lvl, value = 1)
    print("초기 레벨 설정 | lvl:", ws.cell(_row,c_lvl).value)

    wb.save("userDB.xlsx")
    wb.close()

    print("데이터 추가 완료")

def userInfo(_name, _id):
    loadFile()
    if not checkName(_name, _id):
        print("사용자 정보 발견, 보유 자산과 레벨을 반환")
        for row in range(2, ws.max_row+2):
            if ws.cell(row,c_name).value == _name and ws.cell(row, c_id).value == hex(_id):
                print("보유자산: ", ws.cell(row,c_money).value, "레벨: ", ws.cell(row,c_lvl).value)
                return ws.cell(row,c_money).value, ws.cell(row,c_lvl).value
                break
    else:
        #사용자 정보 없음
        return None, None

    wb.save("userDB.xlsx")
    wb.close()

def delete():
    loadFile()
    print("유저 데이터를 삭제")

    ws.delete_rows(2,ws.max_row)
    #for row in ws['A2:D20']:
    #    for cell in row:
    #        cell.value = None
    wb.save("userDB.xlsx")
    wb.close()

    print("데이터 삭제 완료")

