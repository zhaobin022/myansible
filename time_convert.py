import datetime
import time
def string2timestamp(strValue):  
  
    try:          
        d = datetime.datetime.strptime(strValue, "%Y-%m-%d %H:%M:%S.%f")  
        t = d.timetuple()  
        timeStamp = int(time.mktime(t))  
        timeStamp = float(str(timeStamp) + str("%06d" % d.microsecond))/1000000  
        print timeStamp  
        return timeStamp  
    except ValueError as e:  
        print e  
        d = datetime.datetime.strptime(strValue, "%Y-%m-%d %H:%M:%S")  
        t = d.timetuple()  
        timeStamp = int(time.mktime(t))  
        timeStamp = float(str(timeStamp) + str("%06d" % d.microsecond))/1000000  
        print timeStamp  
        return timeStamp  


string2timestamp('2016-6-1 18:00:00')
