from bs4 import BeautifulSoup as bs
import urllib.request as request
import re
import numpy as np
# url = 'http://www.chem.utoronto.ca/cgi-bin/Calcium40_cni.pl?Op=ShowIt&CalendarName=ESEM__STEM'

url = 'http://www.chem.utoronto.ca/cgi-bin/Calcium40_cni.pl?CalendarName=ESEM__STEM&Op=ShowIt&Amount=Week&NavType=Absolute&Type=TimePlan&DayViewStart=8&DayViewHours=16&DayViewIncrement=2'
day_list = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
config = open('config.txt','r')
########
config.close()
old_timetable = np.loadtxt('old_timetable.txt',delimiter=',')
# print(old_timetable)

html = request.urlopen(url).read()
soup = bs(html,'html.parser')
table = soup.find("table",class_="EventCells")
row = table.find_all("tr",class_=re.compile(""))
# for i in row:
#     print (i.prettify())
new_timetable = np.zeros((32,7),np.uint8)
for i,time in enumerate(row):
    # i=0 8am; i=1 8:30am
    # print ([k for k in time.children if k != ' ' and 'colspan' in k.attrs])
    empty_slot = []
    for j in range(7):
        if new_timetable[i,j] == 0:
            empty_slot.extend(str(j))
    for j,slot in enumerate([k for k in time.children if k != ' ' and 'colspan' in k.attrs]):
        # j=0 Mon j=1 Tue
        if 'rowspan' in slot.attrs:
            # duration=1 0.5h
            duration = int(slot['rowspan'])

            new_timetable[i:i + duration,int(empty_slot[j])] += 1

# print (new_timetable)

# for j in range(7):
#     for i in range(30):
#         if new_timetable[i,j] == 1:
#             print (day_list[j],8 + i / 2)

if (new_timetable == old_timetable).all():
    print ('yes')

np.savetxt('old_timetable.txt', new_timetable, delimiter=',',fmt='%i')