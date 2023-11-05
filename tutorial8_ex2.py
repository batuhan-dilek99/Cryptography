#-------------------------------
# COMP.SEC.220 Tutorial 8 Exercise 2
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


def dbSseQuery(keyword):
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="tutorial8",
		password="tutorial8",
		database="tutorial8"
    )
    cursor = mydb.cursor()
    cursor.execute("SELECT sse_keyword_numfiles, sse_keyword_numsearch FROM sse_keywords WHERE sse_keyword = '" + keyword + "' ;")
    result = cursor.fetchall()
    mydb.close()
    return result

def dbCspQuery(address):
    mydb = mysql.connector.connect(
        host="localhost",
        user="tutorial8",
        password="tutorial8",
        database="tutorial8"
    )
    cursor = mydb.cursor()
    cursor.execute("SELECT csp_keyvalue FROM sse_csp_keywords WHERE csp_keywords_address = '" + address + "' ;")
    result = cursor.fetchall()
    mydb.close()
    return result


def unpad(s):
        return s[:-ord(s[len(s)-1:])]

def decrypt(enc, key):
        iv = enc[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')


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

def getKey(password):
	hasher = SHA256.new(password.encode('utf-8'))
	return hasher.hexdigest()

def main():
    bobWord = input("Hey Bob! what do you want to search for today? : ")
    bobWordHash = getKey(bobWord)
    print("Hashed version of your word is : " + bobWordHash)

    sseQuery = dbSseQuery(bobWordHash)
    numfiles = str(sseQuery[0][0])
    numsearch = str(sseQuery[0][1])
    print("numfile and numsearch values are : " + numfiles + " and " + numsearch)
    Kw = getKey(bobWordHash + str(numsearch))
    csp_address = getKey(Kw + str(numfiles))
    print("You are looking for the hash value : " + csp_address)
    cspQuery = dbCspQuery(csp_address)
    csp_key = cspQuery[0][0]
    print(csp_key)
    value = bytes(csp_key, 'utf-8')
    encodedKey = "CdLpLk5cMND8loqrDtb9zmtGOwQX2Wpg".encode('utf-8')
    print(str(os.sys.getsizeof(encodedKey)))
    fileName = decrypt(value, encodedKey)
    print(fileName)

if __name__ == "__main__":
     main()