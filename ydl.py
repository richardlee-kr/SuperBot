import youtube_dl
import os

mp3List = []

def ydl(url):
    #if os.path.isfile(file):
        #os.remove(file)

    ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
                }],
            'outtmpl': '%(title)s.%(ext)s',
            }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

def Scan():
    FILE = os.listdir("./")
    fileList = [file for file in FILE if file.endswith(".mp3")]
    if not fileList == None:
        for v in fileList:
            if v not in mp3List:
                mp3List.append(v)

def printList():
    #print("현재 재생목록")
    for i in range(0,len(mp3List)):
        print(i, "." + mp3List[i])

def returnList():
    return mp3List

def deleteFile():
    os.remove(mp3List[0])
