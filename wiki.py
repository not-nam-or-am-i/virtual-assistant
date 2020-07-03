import wikipedia

def answer_wiki(text):
    #get query string
    question = ['là ai', 'là gì', 'là cái gì']
    pos = text.find('là ai')
    i=1
    while pos == -1:
        pos = text.find(question[i])
        i+=1
    query = text[0:pos-1]
    wikipedia.set_lang('vi')
    try:
        return wikipedia.summary(query, sentences=1)
    except:
        return 'Jarvis không biết đáp án của câu hỏi'