import rsa
import sys
import os
import time
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES, PKCS1_OAEP
class Person():

    def __init__(self, name):
        #(self.publicKey, self.privateKey) = rsa.newkeys(512)
        key = RSA.generate(2048)

        
        #this is private key
        self.privateKey = key.export_key(passphrase=name, pkcs=8, protection="scryptAndAES128-CBC")
        
        #this is public key
        self.publicKey = key.public_key().export_key()


    def encrypt(self, message):
        
        timeStart = time.perf_counter()
        rsa_public_key = RSA.importKey(self.otherPubKey)
        rsa_public_key = PKCS1_OAEP.new(rsa_public_key)
        encryptedMessage = rsa_public_key.encrypt(message)
        print("your encrypted text is : {}".format(encryptedMessage))
        timeEnd = time.perf_counter()
        os.system("touch message.txt")
        
        f = open("message.txt", "wb")
        f.write(encryptedMessage)
        f.close()
        return timeEnd - timeStart

    def decrypt(self):
        f = open("message.txt", "rb")
        message = f.read()
        f.close()
        timeStart = time.perf_counter()
        rsa_private_key = RSA.importKey(self.privateKey, 'Bob')
        rsa_private_key = PKCS1_OAEP.new(rsa_private_key)
        decrypted = rsa_private_key.decrypt(message)
        timeEnd = time.perf_counter()

        #decrypted = rsa.decrypt(message, self.privateKey)
        print("\n\nDecrypted text is : {}".format(decrypted))
        return timeEnd - timeStart

    def fetchOtherKey(self, key):
        self.otherPubKey = key
    
    def getPublicKey(self):
        return self.publicKey


alice = Person(input("Enter passphrase for alice : "))
bob = Person("Bob")

alice.fetchOtherKey(bob.getPublicKey())
bob.fetchOtherKey(alice.getPublicKey())

aliceSays = input("Enter Alices' message to send it to Bob : ")
#alice.encrypt(str.encode(aliceSays))

timerStart = time.perf_counter()
timeEnc = alice.encrypt(str.encode(aliceSays))
timeDec = bob.decrypt()
timerEnd = time.perf_counter()

print("Encryption time : %.4f" % float(timeEnc))
print("Decryption time : %.4f" % float(timeDec))
print("Whole calculation took %.4f" % float(timerEnd-timerStart), " seconds")
os.system("rm message.txt")