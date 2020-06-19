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
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    playsound.playsound(filename)

#speech to string
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ''

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print('Exception: ' + str(e))

    return said

speak('Jarvis is listening', 'greeting.mp3')
text = get_audio()

if 'hello' in text:
    speak('hi there, how are you?', 'hi.mp3')

if 'bye' in text:
    speak('goodbye', 'bye.mp3')

#open browser
if 'open browser' in text:
    url='google.com'
    webbrowser.open(url, autoraise=False)
    speak('open browser', 'browser.mp3')

#search: mở link đầu tiên trên tab mới
if 'search' in text:
    #get query string
    pos = text.find('search')
    query = text[pos+len('search'):].strip()

    #mở link đầu tiên trên trình duyệt
    url = next(search(query, tld='com', lang='vi', num=1, start=0, stop=None, pause=2))
    # print(url)
    webbrowser.open(url, autoraise=False)
    end_speech = 'search for ' + query
    speak(end_speech, 'search.mp3')

#open music on youtube
if 'play' in text:
    # subprocess.call(r'C:\Users\Acer\AppData\Roaming\Spotify/Spotify.exe')
    #get query string
    pos = text.find('play')
    query = text[pos+len('play'):].strip()
    if query == 'music' or query == 'some music' or query == 'music please' or query == 'some music please':
        webbrowser.open(DEFAULT_MUSIC, autoraise=False)    
        speak('play music', 'music.mp3')
    else:
        if len(YoutubeSearch(query, max_results=1).to_dict()) > 0:
            results = YoutubeSearch(query, max_results=1).to_dict()[0]
            url = 'youtube.com' + results.get('link')
            print(url)
            webbrowser.open(url, autoraise=False)    #autoraise=false không hoạt động ở windows
            end_speech = 'play ' + query
            speak(end_speech, 'music.mp3')
        else:
            speak('sorry, i could not find ' + query, 'sorry.mp3')