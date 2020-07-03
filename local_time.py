import time
import datetime
import requests
import json

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
        return ans
    return "false"
    

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
        print(location_)

        return location_
    return "false"

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

        print(ans)           
        return ans
    return "false" 
