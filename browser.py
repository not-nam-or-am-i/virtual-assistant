import webbrowser

def search_google(text):
    #get query string
    pos = text.find('tìm')
    query = text[pos+len('tìm'):].strip()
    webbrowser.open('https://google.com/?#q=' + query, autoraise=False)
    return 'tìm kiếm ' + query

def open_browser():
    webbrowser.open('google.com', autoraise=False)
    return 'mở trình duyệt'