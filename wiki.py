import wikipedia

def answer_wiki(text):
    #get query string
    wikipedia.set_lang('vi')
    return wikipedia.summary(text, sentences=1)