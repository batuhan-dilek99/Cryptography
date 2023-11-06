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
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend
import base64

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
    # cursor.execute("UPDATE sse_keywords SET sse_keyword_numsearch = sse_keyword_numsearch + 1 WHERE sse_keyword = '" + keyword +"';" )
    # mydb.commit()
    mydb.close()
    return result
    

def getKey(password):
	hasher = SHA256.new(password.encode('utf-8'))
	return hasher.hexdigest()


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


def unpad(plain_text):
    last_character = plain_text[len(plain_text) - 1:]
    bytes_to_remove = ord(last_character)
    return plain_text[:-bytes_to_remove]

def decrypt(ciphertext, key):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    decodedciphertext = base64.b64decode(ciphertext)
    padded_data = decryptor.update(decodedciphertext) + decryptor.finalize()
    unpadder = PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_data) + unpadder.finalize()
    return plaintext


def decryptFile(key, filename):
    chunksize = 64*1024
    outputFile = filename[3:]

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



def main():
    keyFile = open("key.txt", "rb")
    key = keyFile.read()
    bobWord = input("Hey Bob! what do you want to search for today? : ")
    
    startTime = time.time()
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
    print("AES key is : ",csp_key)
    #Not working
    fileName = decrypt(bytes(csp_key), key)
    print("File name is : ",fileName.decode()[:-1])
    newFileName = str("ENC" + fileName.decode()[:-1])
    decryptFile(key, newFileName)

    endTime = time.time()
if __name__ == "__main__":
     main()