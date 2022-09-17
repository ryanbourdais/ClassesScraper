from bs4 import BeautifulSoup
import requests
import csv

url = 'https://appl101.lsu.edu/booklet2.nsf/All/F2FEE3EFC721745E862588020031B067?OpenDocument'
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')
resultList = soup.find_all('pre')
resultList = str(resultList)
splitList = resultList.split(' ')

result = []
for item in splitList:
    if item.strip():
        result.append(item)

badWords = ['[<pre>\n', 'COURSE', 'HR', 'TIME', 'DAYS', 'SPECIAL\nAVL', 'CNT', 'ABBR', 'NUM', 'TYPE', 'NUM', 'COURSE',
            'TITLE', 'CR', 'BEGIN-END', 'MTWTFS', 'ROOM', 'BUILDING', 'ENROLLMENT',
            'INSTRUCTOR\n----------------------------------------------------------------------------------------------------------------------------------\n']

print(result)
for x in range(1, 23, 1):
    result.pop(0)

y = True
while y:
    index = len(result) - 1
    if (result[index]).find("Fall") != -1:
        result.pop()
        y = False
    else:
        result.pop()

Courses = {}
tempArray = []
key = 0
for x in range(0, len(result)):
    tempArray.append(result[x])
    if result[x].find("\n") != -1:
        Courses.update({key: tempArray})
        tempArray = []
        key = key + 1
    else:
        continue

print(Courses)

for value in Courses.values():
    initialX = 0
    finalX = 0
    creditHours = 0
    section = 0
    newArray = []
    xFound = False
    for x in range(len(value) - 1, 0, -1):
        if value[x].find(".") != -1:
            initialX = x
            creditHours = value[initialX]
            print("initial x = " + value[x])
        elif value[x].find("1-12") != -1:
            initialX = x
            creditHours = value[initialX]
            print("initial x = " + value[x])
        elif value[x].find("1-3") != -1:
            initialX = x
            creditHours = value[initialX]
            print("initial x = " + value[x])
        elif value[x].find("1-9") != -1:
            initialX = x
            creditHours = value[initialX]
            print("initial x = " + value[x])
        if x < initialX and value[x].isdigit() and not xFound:
            xFound = True
            finalX = x
            section = value[finalX]
            print("finalX = " + value[x])

        if finalX != 0 and initialX != 0:
            for y in range(finalX, initialX, 1):
                if y > finalX:
                    newArray.append(value[y])
                value.pop(finalX)
                title = " ".join(newArray)
                value.insert(finalX, title)
            titleLen = initialX - finalX
            for z in range(0, titleLen, 1):
                value.pop(finalX + 1)
            value.insert(4, section)
            value.insert(6, creditHours)
            initialX = 0
            finalX = 0
            xFound = False

for value in Courses.values():
    for x in range(len(value) - 1, 0, -1):
        if value[x] == '100%' or value[x] == 'WEB' or value[x] == 'BASED' or value[x] == 'PERMIS' or value[x] == 'OF' \
                or value[x] == 'DEPT' or value[x] == 'CI-WRITTEN&amp;SPOK':
            value.pop(x)
        if value[x] == 'TAYLOR' or value[x] == 'HALL' or value[x] == 'RUSSEL':
            if value[x] == 'TAYLOR':
                value.insert(x + 1, 'PATRICK TAYLOR')
            elif value[x] == 'HALL':
                value.insert(x + 1, 'TUREAUD HALL')
            else:
                value.insert(x + 1, "HOWE RUSSEL")
            value.pop(x)
            value.pop(x - 1)
    if value[4] != "LAB" or value[4] != "RES" or value[4] != "IND" or value[4] != "SEM":
        value.insert(4, '')
    if not value[1].isdigit():
        value.insert(0, 'F')
    if len(value) >= 10:
        if value[9] == "M":
            if value[10] == "W":
                if value[11] == "F":
                    value.pop(9)
                    value.pop(9)
                    value.pop(9)
                    value.insert(9, "M W F")
                else:
                    value.pop(9)
                    value.pop(9)
                    value.insert(9, "M W")
        if value[9] == "T" and value[10] == "TH":
            value.pop(9)
            value.pop(9)
            value.insert(9, "T TH")

Course_info = ['AVL', 'ENRL', 'ABBR', 'NUM', 'TYPE', 'SEC', 'TITLE', 'CR', 'TIME', 'DAYS', 'ROOM', 'BUILDING', 'INSTR']
Courses_dict = []
for value in Courses.values():
    newValues = value
    newDict = dict(zip(Course_info, newValues))
    Courses_dict.append(newDict)
print(Courses_dict)

for value in Courses_dict:
    if len(value.values()) < 12:
        del value

csv_file = "Courses.csv"

with open(csv_file, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=Course_info)
    writer.writeheader()
    for data in Courses_dict:
        writer.writerow(data)
