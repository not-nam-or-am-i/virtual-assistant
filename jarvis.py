from tkinter import *
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
import threading
import bs4, requests
import sys
import subprocess
from local_time import *
from browser import *
from youtube import *
from wakeup import *
from wiki import *
from vietnam_news import *
from game import *

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

def asynchronous_speak(text, filename='voice.mp3'):
    os.remove(filename)
    tts = gTTS(text=text, lang='vi')
    tts.save(filename)       
    playsound.playsound(filename) 
    
def takeCommand():
    r = sr.Recognizer()
    query=""
    with sr.Microphone() as source:
        var.set("Đang nghe...")
        window.update()
        print("Listening...")        
        audio = r.adjust_for_ambient_noise(source, duration=0.5) # listen 0.5s for recognizing noise , listen for 0.5 second to calibrate the energy threshold for ambient noise levels
        audio = r.listen(source, timeout=7, phrase_time_limit=10)        
        try:
            var.set("Đang nhận diện...")
            window.update()
            print("Đang nhận diện...")
            query = r.recognize_google(audio, language='vi-VN')
        except Exception as e:
            print('exception in google recognizing ...')
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

# 
def respond_to_user(ans: str):
    var.set(ans)
    window.update()
    speak(ans)    

def respond_to_user_asynchronous(ans:str):
    var.set(ans)
    window.update()
    asynchronous_speak(ans)        
###    
def _play():    
    btn2['state'] = 'disabled'    
    btn1.configure(bg = 'orange')         
          
        
    text = takeCommand().lower()
    # text = "hôm nay có tin tức gì  ?"

    tem1, _ = get_news(text)
    tem2, ans2 = play_hangman(text)

    if tem2 != "false": # choi game
        respond_to_user(ans2)
    elif 'kết thúc' in text:
        goodbye()
        window.destroy()      
          
    elif 'thức dậy' in text:
        best_time = get_wakeup_time()
        var.set(f"{best_time[0].hour}:{best_time[0].minute} hoặc {best_time[1].hour}:{best_time[1].minute}")
        window.update()
        speak(f"Bạn nên dậy vào {best_time[0].hour} giờ {best_time[0].minute} phút hoặc {best_time[1].hour} giờ {best_time[1].minute} phút")  
            

    elif get_location(text) != "false":
        respond_to_user(""+get_location(text))

    elif get_day(text) != "false":
        respond_to_user(""+get_day(text))
    
    elif get_time(text) != "false" :
        respond_to_user(""+get_time(text))

    elif tem1 != "false":  # get news
        _, news_list = get_news(text)
        for i in range(len(news_list)):
            ans = news_list[i]
            respond_to_user_asynchronous(ans)

    elif 'tìm trên youtube' in text:
        end_speech = search_youtube(text)
        respond_to_user(end_speech)
        
    elif 'tìm' in text:
        end_speech = search_google(text)
        respond_to_user(end_speech)
    #bật video trên youtube
    elif 'bật' in text:
        end_speech = play(text)
        respond_to_user(end_speech)

        # break    
    elif 'xin chào' in text:
        hello()
    elif 'gọi tôi là' in text:
        id_end = text.find("gọi tôi là") + len("gọi tôi là ")
        show_name(text[id_end:])
    elif 'thời tiết' in text:            
        weather_description = get_weather()
        respond_to_user(weather_description)
        #open browser
    elif 'mở trình duyệt' in text:
        end_speech = open_browser()
        respond_to_user(weather_description)

    elif 'máy ảnh' in text:
        var.set("Mở máy ảnh")
        window.update()        
        subprocess.run('start microsoft.windows.camera:', shell=True)
        speak('Mở máy ảnh')

    elif 'là ai' in text or 'là gì' in text or 'là cái gì' in text:
        end_speech = answer_wiki(text)
        respond_to_user(end_speech)

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