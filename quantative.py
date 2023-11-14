import os


f = open("finaloutput.txt", "r")

fileData = f.read()
lines = fileData.splitlines()

splittedLines = []
for line in lines:
    tempLine = line.split("?")
    splittedLines.append(tempLine)


allCategories = []
for line in splittedLines:
    if len(line) <= 2:
        continue
    else: 
        allCategories.append(line[1])

#Maximum Average
max = 0.0
for line in splittedLines:
    if len(line) <= 2:
        continue
    elif float(line[2]) < 2:
        continue
    elif (float(line[3]) > float(max)):
        max = line[3]
        maxItem = line

#Min Average
min = 999999
for line in splittedLines:
    if len(line) <= 2:
        continue
    elif float(line[2]) < 2:
        continue
    elif (float(line[3]) < float(max)):
        min = line[3]
        minItem = line

#max product
maxP = 0
for line in splittedLines:
    if len(line) <= 2:
        continue
    elif float(line[2]) < 2:
        continue
    elif (float(line[2]) > float(maxP)):
        maxP = line[2]
        maxpItem = line

for line in splittedLines:
    if len(line) <= 2:
        continue
    elif (float(line[2]) == float(100)):
        love = 1

# print(maxItem)
# print(minItem)
# print(maxpItem)

print(allCategories)