import webbrowser
import bs4, requests

DEFAULT_MUSIC = 'https://www.youtube.com/watch?v=3jWRrafhO7M'

def play(text):
    #get query string
    pos = text.find('bật')
    query = text[pos+len('bật'):].strip()
    if query == 'nhạc' or query == 'nhạc đi':
        webbrowser.open(DEFAULT_MUSIC, autoraise=False)
        return 'bật nhạc'
    else:
        searchTerm = query.replace(' ', '+')
        text = requests.get('https://www.youtube.com/results?search_query='+searchTerm).text
        soup = bs4.BeautifulSoup(text, "html.parser")
        idpos = text.find('videoId')
        # print(idpos)
        urlpos = idpos + len("videoId") + 3
        url = text[urlpos: urlpos+11]
        # print(url)
        webbrowser.open('https://www.youtube.com/watch?v='+url)
        return 'mở ' + query

def search_youtube(text):
    pos = text.find('tìm trên youtube')
    query = text[pos+len('tìm trên youtube'):].strip()
    searchTerm = query.replace(' ', '+')
    webbrowser.open('https://www.youtube.com/results?search_query=' + searchTerm, autoraise=False)
    return 'tìm trên youtube ' + query