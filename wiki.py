import wikipedia

def answer_wiki(text):
    #get query string
    wikipedia.set_lang('vi')
    try:
        return wikipedia.summary(text, sentences=1)
    except:
        return 'Jarvis không biết đáp án của câu hỏi'