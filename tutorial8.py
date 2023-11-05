#-------------------------------
# COMP.SEC.220 Tutorial 8
# Batuhan Dilek
# 152177373
#-------------------------------
import os
import random
import string
import struct
from Cryptodome.Cipher import AES
from Cryptodome import Random
from Cryptodome.Hash import SHA256
import mysql.connector
import codecs
import time

#CdLpLk5cMND8loqrDtb9zmtGOwQX2Wpg
def encryptFile(key, filename):
	chunksize = 64*1024
	outputFile = "ENC"+filename
	filesize = str(os.path.getsize(filename)).zfill(16)
	IV = Random.new().read(16)

	encryptor = AES.new(key, AES.MODE_CBC, IV)

	with open(filename, 'rb') as infile:#rb means read in binary
		with open(outputFile, 'wb') as outfile:#wb means write in the binary mode
			outfile.write(filesize.encode('utf-8'))
			outfile.write(IV)

			while True:
				chunk = infile.read(chunksize)

				if len(chunk) == 0:
					break
				elif len(chunk)%16 != 0:
					chunk += b' '*(16-(len(chunk)%16))

				outfile.write(encryptor.encrypt(chunk))

def decryptFile(key, filename):
	chunksize = 64*1024
	outputFile = filename[11:]

	with open(filename, 'rb') as infile:
		filesize = int(infile.read(16))
		IV = infile.read(16)

		decryptor= AES.new(key, AES.MODE_CBC, IV)

		with open(outputFile, 'wb') as outfile:
			while True:
				chunk = infile.read(chunksize)

				if len(chunk) == 0:
					break

				outfile.write(decryptor.decrypt(chunk))

			outfile.truncate(filesize)
			

def pad(plain_text):
    number_of_bytes_to_pad = AES.block_size - len(plain_text) % AES.block_size
    ascii_string = chr(number_of_bytes_to_pad)
    padding_str = number_of_bytes_to_pad * ascii_string
    padded_plain_text = plain_text + padding_str
    return padded_plain_text

def encrypt(key,plainText):
    padedPlainText = pad(plainText)
    IV = Random.new().read(16)
    mode = AES.MODE_CBC
    encrypt = AES.new(key, mode, IV=IV)
    cipherText = encrypt.encrypt(padedPlainText.encode('utf-8'))
    return cipherText

def getKey(password):
	hasher = SHA256.new(password.encode('utf-8'))
	return hasher.hexdigest()

def utf8len(s):
    return len(s.encode('utf-8'))


def dbSseQuery(keyword, numfile, numsearch):
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="tutorial8",
		password="tutorial8",
		database="tutorial8"
    )
    cursor = mydb.cursor()
    cursor.execute("INSERT INTO sse_keywords (sse_keyword, sse_keyword_numfiles, sse_keyword_numsearch) VALUES (" + "'"+ keyword + "'" + "," + str(numfile) + "," + str(numsearch) + ");")
    mydb.commit()
    mydb.close()

def dbCspQuery(address, keyvalue):
	mydb = mysql.connector.connect(
        host="localhost",
        user="tutorial8",
		password="tutorial8",
		database="tutorial8"
    )
	cursor = mydb.cursor()
	cursor.execute("INSERT INTO sse_csp_keywords (csp_keywords_address, csp_keyvalue) VALUES (" + "'" + address + "'" + "," + "'" + keyvalue + "'" + ");")
	mydb.commit()
	mydb.close()


def main():
    listOfClearText = []
    listOfEncryptedText = []
    #random key generator
    key = ''.join(random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=32))
    print("Generated key for the user : ",key)
    encodedKey = key.encode("utf-8")
    #iterate each file and extract the content
    startTime = time.time()
    for filename in os.listdir():
        txtFileName = os.path.join("", filename)
        if(".txt" in txtFileName):
            if ("ENC" in txtFileName):
                continue
            #open the file in read mode
            f = open(txtFileName, "r")
            content = f.read()
            clearText = content
            listOfClearText.append(clearText)

            #Encrypting files 
            encryptFile(encodedKey, txtFileName)
		
            #removing the unencrypted txt files
			
            #initializing numfile, numsearch and hash
            numfile = 0
            numsearch = 0
            for word in listOfClearText:
                if(clearText == word):
                    numfile += 1
                
            sse_keyword = getKey(clearText)
            dbSseQuery(sse_keyword,numfile,numsearch)
            Kw = getKey(sse_keyword + str(numsearch))
            address = getKey(Kw + str(numfile))
            dbCspQuery(address, str(encrypt(encodedKey, txtFileName + str(numfile)))[1:].strip("'"))
			
            os.system("rm " + txtFileName)
    endTime = time.time()
    print("All files are encrypted and plain ones are deleted " + "[" + str(u'\u2713') + "]")
    print("Data is inserted into sse_keywords table " + "[" + str(u'\u2713') + "]")
    print("Data is inserted into sse_csp_keywords table " + "[" + str(u'\u2713') + "]")
    
    elapsedTime = endTime - startTime
	
    print("Elapsed time for to encrypt 25 files and creating a dictionary %.4f: " % elapsedTime + " seconds")

        
    

if __name__ == "__main__":
    main()

#iterate each file and extract the content
#Encrypt the file using AES

#For extracted words
