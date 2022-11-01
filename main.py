import tarfile
import io
import csv
from russian_names import RussianNames
import random
import datetime

# define value:
linesvalue = 50000
gendervalue = 0.5
visaormastervalue = 0.7 # 1 visa only
year = 2023
month = 1
mintravel = 1


# technical value
row0 = ['ФИО','Паспортные данные','Откуда','Куда','Дата отъезда','Дата приезда','Рейс','Вагон Место','Стоимость','Карта оплаты']
sapsanvag = ['1Р','1В','1С','2С','2В','2Е']
strigvag = ['1Е','1Р','2С']
fastvag = ['1С','1Р','1В','2Р','2Е']
othervag = ['3Э','2Э','1Б','1Л','1А','1И']
stations = []
visacards = []
mastercards = []
with io.open('stations', encoding='utf-8') as file:
     for line in file:
         stations.append(line[:-1:])
with open('visa',encoding='utf-8') as file:
    for line in file:
        visacards.append(line[:-1:])
with open('mastercard',encoding='utf-8') as file:
    for line in file:
        mastercards.append(line[:-1:])
nameindex = -1
trains = []
pasenger = []
lenstations = len(stations)
lenvisa = len(visacards)
lenmastercard = len(mastercards)
day = 1
Fio = RussianNames(count=linesvalue,gender=gendervalue, patronymic=True, transliterate=False).get_batch()
random.seed(version=2)

f = open('database.csv', 'w')
writer = csv.writer(f)
writer.writerow(row0)


def location():
    a = random.randint(0,lenstations-1)
    b = random.randint(0,lenstations-1)
    while a == b:
        b = random.randint(0, lenstations)
    return stations[a],stations[b]

def name():
    global nameindex
    nameindex+=1
    return Fio[nameindex]

def passid():
    a = random.randint(1000,9999)
    b = random.randint(100000,999999)
    return str(a) + ' ' + str(b)

def date(day):
    interval = random.randint(mintravel,7)
    x = datetime.datetime(2023, 1, day, random.randint(0, 23), random.randint(0, 59))
    y = datetime.datetime(year, month, day + interval, random.randint(0, 23), random.randint(0, 59))
    return x,y, interval

def bankcard():
    n = random.randint(0,9998)
    x = visaormastervalue * 100
    y = 100 - x
    a = random.choices([0 , 1], weights=[x, y])
    if a == 0:
        card = visacards[n]
    else:
        card = mastercards[n]
    return card

def traintype(type):
    match type:
        case 1:
            number = str(random.randint(1,150))
        case 2:
            number = str(random.randint(150, 298))
        case 3:
            number = str(random.randint(301, 450))
        case 4:
            number = str(random.randint(451, 598))
        case 5:
            number = str(random.randint(701, 750))
        case 6:
            number = str(random.randint(751, 788))

    return number

def vagon(type):

    if type == 1 or type == 2 or type == 3 or type == 4:
        a = random.randint(0,len(othervag)-1)
        vag = othervag[a]
    elif type == 5 :
        a = random.randint(0, len(fastvag )-1)
        vag = fastvag[a]
    else:
        a = random.random()
        if a == 1:
            a = random.randint(0, len(sapsanvag ) -1)
            vag = sapsanvag[a]
        else:
            a = random.randint(0, len(strigvag)- 1)
            vag = strigvag[a]
    if vag[:1] == '1': #коэффициент цены за 1 класс
        place = random.randint(1,24)
        costk = 3
    elif vag[:1] == '2':
        place = random.randint(1,36)
        costk = 2
    else:
        place = random.randint(1,54)
        costk = 1
    vagnumber = random.randint(1,15)
    return vag, costk , vagnumber, place

class train:
    def __init__(self,type,day):
        self.type = type
        self.number = traintype(type)
        self.From, self.To = location()
        self.startday, self.endday, self.interval = date(day)

    def display(self):
        print('type= ',self.type)
        print('number= ', self.number)
        print('From= ', self.From)
        print('To= ', self.To)
        print('Start day= ', self.startday)
        print('Endday= ', self.endday)

class passenger():
    def __init__(self,train):
        self.fio = name()
        self.id = passid()
        self.card = bankcard()
        self.From = train.From
        self.To = train.To
        self.type = train.type
        self.number = train.number
        self.startday = train.startday
        self.endday = train.endday
        self.interval = train.interval
        self.vag ,self.costk ,self.vagnumber, self.place = vagon(type)
        self.price = train.interval * self.costk * 1000
    def display(self):
        print('type= ',self.type)
        print('number= ', self.number)
        print('From= ', self.From)
        print('To= ', self.To)
        print('Start day= ', self.startday)
        print('Endday= ', self.endday)
        print('Fio= ',self.fio)
        print('id= ', self.id)
        print('card= ', self.card)
        print('vag=',self.vag,'costk=',self.costk,'vagnumber=',self.vagnumber,'place=',self.place)
        print('interval = ',self.interval, 'cost=',self.price)
        print()

for day in range(1,15):
    trains.append(train(1,day))
    trains.append(train(3,day))
    trains.append(train(5,day))
    trains.append(train(6,day))
    if day == 1 or day == 7:
        trains.append(train(2, day))
        trains.append(train(4,day))
lentrains = len(trains)


for i in range(linesvalue):
    x = random.randint(0,lentrains-1)
    a = passenger(trains[x])
    row = [a.fio,a.id,a.From,a.To,a.startday,a.endday,a.number,a.vag + ' ' +str(a.vagnumber) + '-'+ str(a.place),a.price,a.card]
    #print(row)
    writer.writerow(row)
