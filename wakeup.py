from datetime import datetime, timedelta

def get_wakeup_time():
    current_time = datetime.now()
    #14 minutes to fall asleep and 5-6 cycles for good sleep
    #each cycle typically last 90 minutes    
    time1 = current_time + timedelta(minutes=14+90*5)
    time2 = current_time + timedelta(minutes=14+90*6)
    return (time1, time2)