from openpyxl import load_workbook, Workbook

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
def saveFile():
    wb.save("userDB.xlsx")
    wb.close()

def checkUserNum():
    loadFile()

    count = 0

    for row in range(2, ws.max_row+1):
        if ws.cell(row,c_name).value != None:
            count = count+1
        else:
            count = count
    return count
def checkRow():
    loadFile()
    print("첫번쨰 빈 곳을 탐색")
    for row in range(2, ws.max_row + 1):
        if ws.cell(row,1).value is None:
            return row
            break
    _result = ws.max_row+1
    saveFile()

    return _result

def findRow(_name, _id):
    print(_name,"<",_id,">의 존재 여부 확인")
    loadFile()

    print("등록된 유저수: ", checkUserNum())
    print("")

    print("이름과 고유번호 탐색")
    for row in range(2, ws.max_row+2):
        #print(row, "번째 줄 name: ", ws.cell(row,c_name).value)
        #print("입력된 name: ", _name)
        #print("이름과 일치 여부: ", ws.cell(row, c_name).value == _name)

        #print(row,"번째 줄 id: ", ws.cell(row,c_id).value)
        #print("입력된 id: ", hex(_id))
        #print("고유번호정보와 일치 여부: ", ws.cell(row, c_id).value == hex(_id))
        #print("")

        if ws.cell(row, c_name).value == _name and ws.cell(row,c_id).value == hex(_id):
            print("등록된  이름과 고유번호를 발견")
            print("등록된  값의 위치: ",  row, "번째 줄")
            print("")

            saveFile()

            return row
            break
        else:
            print("등록된 정보를 탐색 실패, 재탐색 실시")

    saveFile()

    return None

def getMoney(_name, _id):
    loadFile()

    print("유저의 돈을 탐색중")

    userRow = findRow(_name, _id)
    if not userRow == None:
        print(_name,"의 보유 자산: ", ws.cell(userRow,c_money).value)
        result = ws.cell(userRow, c_money).value

        saveFile()

        return result
    else:
        saveFile()

        return 0
        
#======================================================================================

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

    saveFile()

    print("데이터 추가 완료")

def userInfo(_name, _id):
    loadFile()

    userRow = findRow(_name, _id)

    if not userRow == None:
        print("사용자 정보 발견, 보유 자산과 레벨을 반환")
        print("보유자산: ", ws.cell(userRow,c_money).value, "레벨: ", ws.cell(userRow,c_lvl).value)
        return ws.cell(userRow,c_money).value, ws.cell(userRow,c_lvl).value
    else:
        #사용자 정보 없음
        return None, None

    saveFile()

def remit(sender, s_id, receiver, r_id, _amount):
    loadFile()
    
    print("지정된 유저의 보유 자산 탐색")
    print("보내는 사람: ", sender)
    print("받는 사람: ", receiver)
    print("보내는 돈: ", _amount)

    receiver_row = findRow(receiver, r_id)
    sender_row = findRow(sender, s_id)

    print(receiver, "의 자산:" + str(ws.cell(receiver_row, c_money).value))
    print(sender, "의 자산:" + str(ws.cell(sender_row, c_money).value))
    
    ws.cell(receiver_row, c_money).value += int(_amount)
    ws.cell(sender_row, c_money).value -= int(_amount)

    print("자산 데이터 수정 완료")
    print(receiver, "의 자산: ", ws.cell(receiver_row, c_money).value)
    print(sender, "의 자산: ", ws.cell(sender_row, c_money).value)

    saveFile()

def delete():
    loadFile()

    print("유저 데이터를 삭제")

    ws.delete_rows(2,ws.max_row)
    saveFile()

    print("데이터 삭제 완료")

