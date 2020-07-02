from tkinter import *
# from pydub import AudioSegment
# from pydub.playback import play
from gtts import gTTS
import datetime
import speech_recognition as sr
import webbrowser
import os
import random
import smtplib
import requests
import json
import playsound
# from googlesearch import search
# from youtube_search import YoutubeSearch
import threading
import bs4, requests
import sys
import subprocess
from browser import *
from youtube import *
from wakeup import *

numbers = {'hundred':100, 'thousand':1000, 'lakh':100000}
a = {'name':'your email'}

window = Tk()

global var
global var1

var = StringVar()
var1 = StringVar()

def speak(text, filename='voice.mp3'):
    os.remove(filename)
    tts = gTTS(text=text, lang='vi')
    tts.save(filename)
    threading.Thread(target=playsound.playsound, args=(filename,)).start()
    
def takeCommand():
    r = sr.Recognizer()
    query=""
    with sr.Microphone() as source:
        var.set("Đang nghe...")
        window.update()
        print("Listening...")        
        audio = r.listen(source)
        try:
            var.set("Đang nhận diện...")
            window.update()
            print("Recognizing")
            query = r.recognize_google(audio, language='vi-VN')
        except Exception as e:
            print('zxcvzxcv')
            return "None"
    var1.set(query)
    window.update()
    return query

#id = 77 to start hello
frames = [PhotoImage(file='Assistant.gif',format = 'gif -index %i' %(i)) for i in range(1,100)]



def get_user_name():
    if(not os.path.exists("name.txt")):
        return ""
    file = open("name.txt","r")
    content = file.readline()
    content = content.strip()
    file.close()
    return content

user_name = get_user_name()


ind = 0
def update():
    global ind
    if(ind == 70):        
        ind = 0
    frame = frames[ind]
    ind = (ind + 1)%len(frames)
    # print(ind)
    label.configure(image=frame)       
    window.after(100, update)
    
##task function:
def hello():
    global user_name
    var.set(f"Xin chào {user_name}")
    window.update()
    global ind
    ind = 77
    if(user_name==""):                
        speak("xin chào người dùng. Jarvis vẫn chưa biết tên của bạn. Bạn muốn được gọi là gì ?")       
    else:
        speak(f"xin chào {user_name}. Jarvis có thể giúp gì cho bạn.")        
    
def show_name(name):
    global user_name
    user_name = name
    #Add name
    file = open("name.txt","w")
    file.write(user_name)
    file.close()
    #Run hello again:
    hello()
    
def goodbye():
    var.set(f"Tạm biệt {user_name}")
    btn1.configure(bg = '#5C85FB')
    btn2['state'] = 'normal'     
    window.update()
    global ind
    ind = 77
    speak(f"tạm biệt {user_name}")

def get_weather():
    # Enter your API key here 
    api_key = "4aab97e9a184c620fba4f7f1c7ae3959"
      
    # base_url variable to store url 
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
      
    # Give city name 
    city_name = "hanoi"

    # complete_url variable to store 
    # complete url address 
    complete_url = base_url + "q=" + city_name +"&appid=" + api_key +"&units=metric"+"&lang=vi"
    response = requests.get(complete_url) 
    x = response.json()     
    city = x["name"]
    descr = x["weather"][0]["description"]
    temp = x["main"]["temp"]
    humid = x["main"]["humidity"]
    content = f"Thời tiết {city} {descr}. Nhiệt độ {temp} độ. Độ ẩm {humid} phần trăm."
    return content

###    
def _play():    
    btn2['state'] = 'disabled'    
    btn1.configure(bg = 'orange')         
          
        # btn1.configure(bg = 'orange')
    text = takeCommand().lower()
    if 'tìm trên youtube' in text:
        end_speech = search_youtube(text)
        var.set(end_speech)
        window.update()
        speak(end_speech)
        
    elif 'tìm' in text:
        end_speech = search_google(text)
        var.set(end_speech)
        window.update()
        speak(end_speech)
    #bật video trên youtube
    elif 'bật' in text:
        end_speech = play(text)
        var.set(end_speech)
        window.update()
        speak(end_speech)

    elif 'kết thúc' in text:
        goodbye()
        window.destroy()
        # break    
    elif 'xin chào' in text:
        hello()

    elif 'gọi tôi là' in text:
        id_end = text.find("gọi tôi là") + len("gọi tôi là ")
        show_name(text[id_end:])
    elif 'thời tiết' in text:            
        weather_description = get_weather()
        var.set(weather_description)    
        window.update()        
        speak(weather_description)

        #open browser
    elif 'mở trình duyệt' in text:
        end_speech = open_browser()
        var.set(end_speech)
        window.update()
        speak(end_speech)

    elif 'máy ảnh' in text:
        var.set("Mở máy ảnh")
        window.update()        
        subprocess.run('start microsoft.windows.camera:', shell=True)
        speak('Mở máy ảnh')

    elif 'thức dậy' in text:
        best_time = get_wakeup_time()
        var.set(f"{best_time[0].hour}:{best_time[0].minute} hoặc {best_time[1].hour}:{best_time[1].minute}")
        window.update()
        speak(f"Bạn nên dậy vào {best_time[0].hour} giờ {best_time[0].minute} phút hoặc {best_time[1].hour} giờ {best_time[1].minute} phút")  

    else:
        var.set('Jarvis không hiểu bạn')
        window.update()
        speak('Javis không hiểu bạn nói gì')
        
#Press space
def key(event):    
    if (repr(event.char)=="' '"):
        _play()

if __name__ == '__main__':
    label2 = Label(window, textvariable = var1, bg = '#FAB60C')
    label2.config(font=("Courier", 20))
    var1.set('Người dùng nói:')
    label2.pack()

    label1 = Label(window, textvariable = var, bg = '#ADD8E6')
    label1.config(font=("Courier", 20))
    var.set('Hãy ấn bắt đầu để khởi động trợ lý ảo')
    
    label1.pack()

    window.title('JARVIS')

    label = Label(window, width = 500, height = 500)
    label.pack()
    window.after(0, update)

    btn1 = Button(text = 'Bắt đầu',width = 20,command = _play, bg = '#5C85FB')
    btn1.config(font=("Courier", 12))
    btn1.pack()
    btn2 = Button(text = 'Kết thúc',width = 20, command = window.destroy, bg = '#5C85FB')
    btn2.config(font=("Courier", 12))
    btn2.pack()
    window.after(600, speak, 'hãy ấn bắt đầu để khởi động trợ lý ảo')
    window.bind("<Key>", key)
    window.mainloop()