from datetime import datetime as dt
from random import randint as rd
from OrderManagement import models

def getSysTime(*index):
    get = []
    now = dt.now()
    time = [now.year, now.month, now.day, now.hour, now.minute, now.second]
    for i in index:
        get.append(time[i])
    return get

def getDate():
    now = dt.now()
    date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
    return date

def getOid():
    now = dt.now()
    # count = models.OrderTable.objects.filter(date=today).count()
    '''id date part'''
    idDatePart = str(now.year)
    if now.month < 10:
        idDatePart += '0' + str(now.month)
    else:
        idDatePart += str(now.month)
    if now.day < 10:
        idDatePart += '0' + str(now.day)
    else:
        idDatePart += str(now.day)
    '''check if the first'''
    OrderLast = models.OrderTable.objects.last()
    try:
        if str(OrderLast.oid)[6:8] != str(now.day):
            raise Exception()
        else:
            count = int(str(OrderLast.oid)[8:])
            count += 1
            '''id count part'''
            if count < 10:
                oid = idDatePart + '0' + str(count)
            else:
                oid = idDatePart + str(count)
            return int(oid)
    except:
        oid = idDatePart + '01'
        return int(oid)

def getRid():
    productLast = models.Product.objects.last()
    count = productLast.rid - 9000
    count += 1
    if count < 10:
        rid = '900' + str(count)
    elif 10 < count < 100:
        rid = '90' + str(count)
    else:
        rid = '9' + str(count)
    return int(rid)

def getCid():
    count = models.Customer.objects.all().count()
    count += 1
    if count < 10:
        cid = '800' + str(count)
    elif 10 < count < 100:
        cid = '80' + str(count)
    else:
        cid = '8' + str(count)
    return int(cid)
    
if __name__ == '__main__':
    print(getOid())