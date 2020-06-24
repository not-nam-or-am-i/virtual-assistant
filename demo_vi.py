import os
import time
import playsound
import speech_recognition as sr 
from gtts import gTTS
import subprocess
import webbrowser 
from googlesearch import search
from youtube_search import YoutubeSearch

#fpt api


#register firefox
# firefox_path="C:\Program Files\Mozilla Firefox/firefox.exe"
# webbrowser.register('firefox', None,webbrowser.BackgroundBrowser(firefox_path))
DEFAULT_MUSIC = 'https://www.youtube.com/watch?v=3jWRrafhO7M'

#text to speech
def speak(text, filename='voice.mp3'):
    tts = gTTS(text=text, lang='vi')
    tts.save(filename)
    playsound.playsound(filename)

#speech to string
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ''

        try:
            said = r.recognize_google(audio, language='vi-VN')
            print(said)
        except Exception as e:
            print('Exception: ' + str(e))

    return said

speak('Jarvis đang nghe', 'greeting.mp3')
text = get_audio()
text = text.lower()

#open browser
if 'mở trình duyệt' in text:
    url='google.com'
    webbrowser.open(url, autoraise=False)
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
    speak(end_speech, 'search.mp3')

#open music on youtube
elif 'bật' in text:
    # subprocess.call(r'C:\Users\Acer\AppData\Roaming\Spotify/Spotify.exe')
    #get query string
    pos = text.find('bật')
    query = text[pos+len('bật'):].strip()
    if query == 'nhạc' or query == 'nhạc đi':
        webbrowser.open(DEFAULT_MUSIC, autoraise=False)    
        speak('play music', 'music.mp3')
    else:
        ytsearch = YoutubeSearch(query, max_results=1).to_dict()
        if len(ytsearch) > 0:
            results = ytsearch[0]
            url = 'youtube.com' + results.get('link')
            print(url)
            webbrowser.open(url, autoraise=False)    #autoraise=false không hoạt động ở windows
            end_speech = 'mở bài ' + query
            speak(end_speech, 'music.mp3')
        else:
            speak('Jarvis không tìm thấy bài ' + query, 'sorry.mp3')