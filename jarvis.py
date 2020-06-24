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
from googlesearch import search
from youtube_search import YoutubeSearch
import time
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd 

DEFAULT_MUSIC = 'https://www.youtube.com/watch?v=3jWRrafhO7M'

numbers = {'hundred':100, 'thousand':1000, 'lakh':100000}
a = {'name':'your email'}

window = Tk()

global var
global var1

var = StringVar()
var1 = StringVar()

def speak(text):
    tts = gTTS(text=text, lang='vi')
    tts.save("dtth.mp3")
    playsound.playsound("dtth.mp3")


def takeCommand():
    r = sr.Recognizer()
    query=""
    with sr.Microphone() as source:
        var.set("Đang nghe...")
        window.update()
        print("Listening...")        
        audio = r.adjust_for_ambient_noise(source, duration=0.5) # listen for 1 second to calibrate the energy threshold for ambient noise levels
        audio = r.listen(source, timeout=5, phrase_time_limit=10)
        
        try:
            var.set("Đang nhận diện...")
            window.update()
            print("Đang nhận diện...")
            query = r.recognize_google(audio, language='vi-VN')
        except Exception as e:
            print('exception52')
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
        speak("xin chào người dùng. Mai Thúy vẫn chưa biết tên của bạn. Bạn muốn được gọi là gì ?")       
    else:
        speak(f"xin chào {user_name}. Mai Thúy có thể giúp gì cho bạn.")        
    
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


def get_time(ques: str):
    list_ques = ["mấy giờ", "thời gian"] 
    flag = 0
    for i in list_ques:
        if i in ques:
            flag = 1
    if flag == 1 :        
        seconds = time.time()
        # local_time = time.ctime(seconds)
        res = time.localtime(seconds)
        hour = res.tm_hour
        # year = res.tm_year
        minute = res.tm_min
        ans = "Hiện tại là, " + str(hour) + " giờ," + str(minute) + " phút"
        var.set(ans)
        speak(ans )
        print(ans)
        return True
    return False
    

def get_location(ques: str) : # answer user's location , city, country, longtitude, latitude.
    list_ques = ["ở đâu", "chỗ nào", "vị trí"] 
    flag = 0
    for i in list_ques:
        if i in ques:
            flag = 1
    if flag == 1 :
        send_url = "http://api.ipstack.com/check?access_key=e7c7c4dd6664f61df983df6ac60d4265"
        geo_req = requests.get(send_url)
        geo_json = json.loads(geo_req.text)
        lat = geo_json['latitude']
        
        longi = geo_json['longitude']
        country = geo_json['country_name']
        cit = geo_json['city']
        if cit.lower() == "hanoi":
            cit = " Hà Nội "
        location_ = "bạn đang ở thành phố: " + cit + ". Quốc gia: " + country 
        var.set(location_)
        speak(location_)
        print(location_)
        return True
    return False

def get_day(ques: str):
    list_ques = ["thứ mấy", "ngày bao nhiêu", "ngày nào"] 
    flag = 0
    for i in list_ques:
        if i in ques:
            flag = 1
    if flag == 1 :        
        dt = datetime.datetime.today()
        year = dt.year
        month = dt.month
        day = dt.day
        weekday = dt.weekday()
        weekday += 2
        if weekday == 8 :
            weekday = "chủ nhật"
        else :
            weekday = "thứ " + str(weekday)
        ans = "Hôm nay là " + str(weekday) + ", ngày " + str(day) + " , tháng : " + str(month)
        var.set(ans)
        speak(ans )
        print(ans)           
        return True
    return False 


def get_news(ques: str):
    list_ques = ["tin tức", "tin chính", "thời sự"] 
    flag = 0
    for i in list_ques:
        if i in ques:
            flag = 1
    if flag == 1 :      
        # url definition
        url = "https://vnexpress.net/thoi-su"

        # Request
        r1 = requests.get(url)
        r1.status_code

        # We'll save in coverpage the cover page content
        coverpage = r1.content

        # Soup creation
        soup1 = BeautifulSoup(coverpage, 'html.parser')

        # News identification
        coverpage_news = soup1.find_all('h3', class_='title-news')
        ans = len(coverpage_news)
        print("total news: ", ans)
        speak("Hôm nay có " + str(ans) + " tin tức")
        var.set("Hôm nay có " + str(ans) + " tin tức")
        flag = 0
        if ans > 5 :
            ans = 5
        speak("Sau đây là " + str(ans) + " tin đầu tiên ")
        for news in coverpage_news:
            flag+=1
            # print(news)
            # print(news.find('a')['href'])
            print(news.find('a').getText())
            # print("*"*20)
            var.set(news.find('a').getText())
            speak("Tin số " + str(flag))
            speak( news.find('a').getText())
            if flag == 5 :
                break
        return True
    return False




###    
def _play():    
    btn2['state'] = 'disabled'    
    btn1.configure(bg = 'orange')         
          
    text = takeCommand().lower()
    print("text: ", text)

    if 'kết thúc' in text:
        goodbye()
        window.destroy()
        # break    
    elif get_location(text):
        pass
    elif get_day(text):
        pass
    elif get_time(text):
        pass
    elif get_news(text):
        pass
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
        url='https://google.com'
        webbrowser.get("google-chrome").open(url)
        var.set('mở trình duyệt')
        window.update()
        speak('mở trình duyệt')

    #search: mở link đầu tiên trên tab mới
    elif 'tìm' in text:
        #get query string
        pos = text.find('tìm')
        query = text[pos+len('tìm'):].strip()

        #mở link đầu tiên trên trình duyệt
        print("question: ", query)
        url = next(search(query, tld='com', lang='en', num=1, domains= ['com', 'org', 'vn'], start=0, stop=None, pause=2))
        # print(url)
        webbrowser.open(url, autoraise=False)
        end_speech = 'tìm kiếm ' + query
        var.set(end_speech)
        window.update()
        speak(end_speech)

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
            speak('bật nhạc')
        else:
            ytsearch = YoutubeSearch(query, max_results=1).to_dict()
            print("youtube search: ", ytsearch)
            print("query: ", query)
            if len(ytsearch) > 0:
                results = ytsearch[0]
                url = 'https://youtube.com' + results.get('link')
                print(url)
                webbrowser.open(url, autoraise=False)    #autoraise=false không hoạt động ở windows
                end_speech = 'mở bài ' + query
                var.set(end_speech)
                window.update()
                speak(end_speech)
            else:
                temp = 'Mai Thúy không tìm thấy bài ' + query
                var.set(temp)
                window.update()
                speak(temp)

    else:
        var.set('Mai Thúy không biết câu trả lời ')
        window.update()
        speak('Mai Thúy không biết câu trả lời ')
        

if __name__ == '__main__':
    label2 = Label(window, textvariable = var1, bg = '#FAB60C')
    label2.config(font=("Courier", 20))
    var1.set('Người dùng nói:')
    label2.pack()

    label1 = Label(window, textvariable = var, bg = '#ADD8E6')
    label1.config(font=("Courier", 20))
    var.set('Hãy ấn bắt đầu để khởi động trợ lý ảo')
    
    label1.pack()

    window.title('Mai Thúy')

    label = Label(window, width = 500, height = 500)
    label.pack()
    window.after(0, update)

    btn1 = Button(text = 'Bắt đầu',width = 20,command = _play, bg = '#5C85FB')
    btn1.config(font=("Courier", 12))
    btn1.pack()
    btn2 = Button(text = 'Kết thúc',width = 20, command = window.destroy, bg = '#5C85FB')
    btn2.config(font=("Courier", 12))
    btn2.pack()
    window.after(600, speak, 'hãy ấn bắt đầu để khởi động trợ lý ảo', 'greeting0.mp3')
    window.mainloop()
    
    
