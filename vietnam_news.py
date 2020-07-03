import requests
from bs4 import BeautifulSoup

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
        news_list = []
        
        news_list.append("Hôm nay có " + str(ans) + " tin tức")
        flag = 0
        if ans > 5 :
            ans = 5
        
        news_list.append("Sau đây là " + str(ans) + " tin đầu tiên ")
        for news in coverpage_news:
            flag+=1
            print(news.find('a').getText())            
            news_list.append("Tin số " + str(flag))            
            news_list.append( news.find('a').getText())
            if flag == 5 :
                break
        return "true", news_list

    return "false", "none"
