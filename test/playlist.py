import os

def printList():
    for i in range(0,len(mp3List)):
        print(mp3List[i])

FILE = os.listdir("./")
fileList = [file for file in FILE if file.endswith(".mp3")]
mp3List = ['test.mp3']

printList()

if fileList != None:
    mp3List.extend(fileList)

printList()


