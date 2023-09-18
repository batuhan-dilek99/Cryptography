import time
import os
from Cryptodome.Cipher import AES
from Cryptodome import Random
import base64
print("""                  ___  _____   __  
                 |__ \| ____| / /  
   __ _  ___  ___   ) | |__  / /_  
  / _` |/ _ \/ __| / /|___ \| '_ \ 
 | (_| |  __/\__ \/ /_ ___) | (_) |
  \__,_|\___||___/____|____/ \___/
                            By Batuhan Dilek""")



# AES-256 -> 256 bit -> 32 byte

class AESCipher():

    def __init__(self):
        self.bs = AES.block_size
        self.key = os.urandom(self.bs) 

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))
    
    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return AESCipher._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])] 



text = input("enter a string to encrypt : ")
a = AESCipher()
timeStart = time.perf_counter()
enc = a.encrypt(text)
print("\n\nEncrypted = ", enc)
timeEnd = time.perf_counter()
print("\nEncryption took %.5f seconds" % float(timeEnd-timeStart))

timeStart = time.perf_counter()
dec = a.decrypt(enc)
print("\n\nDecrypted = ",dec)
timeEnd = time.perf_counter()
print("\nDecryption took %.5f seconds" % float(timeEnd-timeStart))


binAry = []
for i in a.key:
    binAry.append(bin(int(str(i), base=16))[2:])
last = "".join(binAry)
print("\n\nThe generated key is : ")
print(last)


