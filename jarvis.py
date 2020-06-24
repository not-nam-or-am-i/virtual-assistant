from tkinter import *
#from pydub import AudioSegment
#from pydub.playback import play
from gtts import gTTS
import speech_recognition as sr
import webbrowser
import os
import random
import smtplib
import requests
import json
import playsound
from googlesearch import search
from youtube_search import YoutubeSearch
import subprocess
from datetime import datetime, timedelta

DEFAULT_MUSIC = 'https://www.youtube.com/watch?v=3jWRrafhO7M'

numbers = {'hundred':100, 'thousand':1000, 'lakh':100000}
a = {'name':'your email'}

window = Tk()

global var
global var1

var = StringVar()
var1 = StringVar()

def speak(text, filename='voice.mp3'):
    tts = gTTS(text=text, lang='vi')
    tts.save(filename)
    playsound.playsound(filename)
    #sound = AudioSegment.from_mp3(filename)
    #play(sound)
    
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
        speak("xin chào người dùng. Jarvis vẫn chưa biết tên của bạn. Bạn muốn được gọi là gì ?", 'greeting1.mp3')       
    else:
        speak(f"xin chào {user_name}. Jarvis có thể giúp gì cho bạn.", 'greeting2.mp3')        
    
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
    speak(f"tạm biệt {user_name}", 'bye.mp3')

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

def get_wakeup_time():
    current_time = datetime.now()
    #14 minutes to fall asleep and 5-6 cycles for good sleep
    #each cycle typically last 90 minutes    
    time1 = current_time + timedelta(minutes=14+90*5)
    time2 = current_time + timedelta(microsoft=14+90*6)
    return (time1, time2)    
###    
def _play():    
    btn2['state'] = 'disabled'    
    btn1.configure(bg = 'orange')         
          
        # btn1.configure(bg = 'orange')
    text = takeCommand().lower()
    if 'kết thúc' in text:
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
        speak(weather_description, 'weather.mp3')        
    elif 'máy ảnh' in text:
        var.set("Bật máy ảnh")
        window.update()        
        subprocess.run('start microsoft.windows.camera:', shell=True)
    elif 'thức dậy' in text:
        best_time = get_wakeup_time()
        var.set(f"{best_time[0].hour}:{best_time[0].minute} hoặc {best_time[1].hour}:{best_time[1].minute}")
        window.update()
        speak(f"Bạn nên dậy vào {best_time[0].hour} giờ {best_time[0].minute} phút hoặc {best_time[1].hour} giờ {best_time[1].minute} phút")          
        
        #open browser
    elif 'mở trình duyệt' in text:
        url='google.com'
        webbrowser.open(url, autoraise=False)
        var.set('mở trình duyệt')
        window.update()
        speak('mở trình duyệt', 'browser.mp3')

    #search: mở link đầu tiên trên tab mới
    elif 'tìm' in text:
        #get query string
        pos = text.find('tìm')
        query = text[pos+len('tìm'):].strip()

        #mở link đầu tiên trên trình duyệt
        url = next(search(query, tld='com', lang='en', num=1, domains= ['com', 'org', 'vn'], start=0, stop=None, pause=2))
        # print(url)
        webbrowser.open(url, autoraise=False)
        end_speech = 'tìm kiếm ' + query
        var.set(end_speech)
        window.update()
        speak(end_speech, 'search.mp3')

    #open music on youtube
    elif 'bật' in text:
        # subprocess.call(r'C:\Users\Acer\AppData\Roaming\Spotify/Spotify.exe')
        #get query string
        pos = text.find('bật')
        query = text[pos+len('bật'):].strip()
        if query == 'nhạc' or query == 'nhạc đi':
            webbrowser.open(DEFAULT_MUSIC, autoraise=False)
            var.set('bật nhạc')    
            window.update()
            speak('bật nhạc', 'music.mp3')
        else:
            ytsearch = YoutubeSearch(query, max_results=1).to_dict()
            if len(ytsearch) > 0:
                results = ytsearch[0]
                url = 'youtube.com' + results.get('link')
                print(url)
                webbrowser.open(url, autoraise=False)    #autoraise=false không hoạt động ở windows
                end_speech = 'mở bài ' + query
                var.set(end_speech)
                window.update()
                speak(end_speech, 'music.mp3')
            else:
                var.set('Jarvis không tìm thấy bài ' + query)
                window.update()
                speak('Jarvis không tìm thấy bài ' + query, 'sorry.mp3')        
    else:
        var.set('Jarvis không hiểu bạn')
        window.update()
        speak('Javis không hiểu bạn nói gì', "not_understand.mp3")    

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
    window.bind("<Key>", key)
    window.after(600, speak, 'hãy ấn bắt đầu hoặc nhấn phím cách để khởi động trợ lý ảo', 'greeting0.mp3')
    window.mainloop()
    # speak('hãy ấn bắt đầu để khởi động trợ lý ảo', 'greeting0.mp3')
    
