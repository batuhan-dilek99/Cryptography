import hashlib
import rsa
import sys
import os
import time
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.Signature.pkcs1_15 import PKCS115_SigScheme
class Person():

    def __init__(self, name):
        #(self.publicKey, self.privateKey) = rsa.newkeys(512)
        self.key = RSA.generate(2048)

        self.password = name
        #this is private key
        self.privateKey = self.key.export_key(passphrase=name, pkcs=8, protection="scryptAndAES128-CBC")
        
        #this is public key
        self.publicKey = self.key.publickey()

        #nd for private
        #ne for public

    def sign(self, fileName):

        blockSize = 65536

        SHA256.new()
        with open(fileName, 'rb') as f:
            fb = f.read(blockSize)
            while len(fb) > 0:
                fileHash = SHA256.new(fb)
                fb = f.read(blockSize)
        
        print(fileHash.hexdigest())
                
        signer = PKCS115_SigScheme(self.key)
        signature = signer.sign(fileHash)
        f.close()
        return signature

    def verify(self, fileName, signature):
        blockSize = 65536

        fileHash = hashlib.sha256()
        with open(fileName, 'rb') as f:
            fb = f.read(blockSize)
            while len(fb) > 0:
                fileHash = SHA256.new(fb)
                fb = f.read(blockSize)
        print(fileHash.hexdigest())
        
        f.close()

        verifier = PKCS115_SigScheme(self.otherPubKey)

        #print(verifier.verify(fileHash, signature))

        try:
            verifier.verify(fileHash, signature)
            print("Signature is valid!")
        except:
            print("Signature is invalid!")
        
        

        #decrypted = rsa.decrypt(message, self.privateKey)
        #print("\n\nDecrypted text is : {}".format(decrypted))
        #return timeEnd - timeStart

    def fetchOtherKey(self, key):
        self.otherPubKey = key
    
    def getPublicKey(self):
        return self.publicKey


alice = Person(input("Enter passphrase for alice : "))
bob = Person("Bob")

alice.fetchOtherKey(bob.getPublicKey())
bob.fetchOtherKey(alice.getPublicKey())


fileName = input("Enter the file name: ")

bob.verify(fileName, alice.sign(fileName))


#aliceSays = input("Enter Alices' message to send it to Bob : ")


#timerStart = time.perf_counter()
#timeEnc = alice.encrypt(str.encode(aliceSays))
##timeDec = bob.decrypt()
#timerEnd = time.perf_counter()

#print("Encryption time : %.4f" % float(timeEnc))
#print("Decryption time : %.4f" % float(timeDec))
#print("Whole calculation took %.4f" % float(timerEnd-timerStart), " seconds")
#os.system("rm message.txt")