import os
import string
import random


for i in range(0,25):
    if (i / 10 >= 1.0):
        os.system("touch " + "f" + str(i) + ".txt")
    else:
        os.system("touch " + "f0" + str(i) + ".txt")

hardCodedFile = random.randint(0,24)
if (hardCodedFile / 10 >= 1.0):
     print("Hardcoded file will be f" + str(hardCodedFile))
else:
     print("Hardcoded file will be f0" + str(hardCodedFile))
     hardCodedFile = "0"+ str(hardCodedFile)

for filename in os.listdir():
        txtFileName = os.path.join("", filename)
        if(".txt" in txtFileName):
            if(txtFileName[:-4] == ("f" + str(hardCodedFile))):
                print(txtFileName)
                f = open(txtFileName, "w")
                text = "Thatisnomoon"
                f.write(text)
                print("The content is : " + text)
            else: 
                f = open(txtFileName, "w")
                rand = random.randint(10,32)
                text = ''.join(random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=rand))
                f.write(text)
            