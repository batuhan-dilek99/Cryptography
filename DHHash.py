import random
from Cryptodome.Hash import SHA256, MD5
from Cryptodome.Util import Padding
from Cryptodome.Cipher import AES
from Cryptodome import Random
import base64
import hashlib
import os
class Person: 

    def __init__(self,name):
        self.name = name

    
    def isPrime(self, num):
        if num > 1:
            for i in range(2, int(num/2)+1):
                if (num % i) == 0:
                    return False
                    break
            else:
                return True
        else:
            return False
        

    def generateSecretKey(self):
        
        primes = [i for i in range (2,10000) if self.isPrime(i)]
        self.secretKey = random.choice(primes)

    
    def generateIntermediate(self, g, p):
        val = pow(g, self.secretKey) % p
        print("Generating first intermediate values for " + self.name + " :")
        print(str(g) + "^" + str(self.secretKey) + " mod " + str(p) + " = " + str(val) + "\n")
        self.interVal = val
        return val
    
    def generateKey(self, otherVal):
        
        print("Key generation for " + self.name + " :")
        key = pow(otherVal, self.secretKey) % p
        print(str(otherVal) + "^" + str(self.secretKey) + " mod " + " = " + str(key))
        self.sharedKey = key
        return key
    
    def hashKey(self):
        #hash = SHA256.new()
        #paddedBytes = bytes(Padding.pad(str(self.sharedKey).encode("utf-8"), 16))
        #hash.update(paddedBytes)
        #print(len(hash.hexdigest()))
        #print("Created a " + str(len((hash.digest())) ) + " bit hashed key")
        #self.hashedKey = hash.hexdigest()
        print("\nHashing using MD5...")
        hash = MD5.new()
        paddedBytes = bytes(Padding.pad(str(self.sharedKey).encode("utf-8"), block_size=MD5.block_size))
        hash.update(paddedBytes)
        print("The key for " + self.name + " is : " + hash.hexdigest())
        print("Generated hash is " + str(len(hash.digest())) + " bytes long")
        print("Generated hash is " + str(len(hash.digest()) * 8)  + " bites long \n")
        self.hashedKeyHex = hash.hexdigest()
        self.hashedKeyBin = hash.digest()

    def stringify(self):
        print("Name : " + self.name)
        print("-----------------")
        print("Secret Key : " + str(self.secretKey))
        print("First intermediate value : " + str(self.interVal))
        print("Commmon computed key : " + str(self.sharedKey))
        print("Hashed commmon computed key : " + self.hashedKeyHex)
        print()


    def encrypt(self, raw):
        print("\nEncrypting the message using common computed key for " + self.name + "...")
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.hashedKeyBin, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))
    
    def decrypt(self, enc):
        print("\nDecrypting the message using common computed key for " + self.name + "...")
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.hashedKeyBin, AES.MODE_CBC, iv)
        return Person._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])] 


alice = Person("Alice")
bob = Person("Bob")

g = 5
p = 37

alice.generateSecretKey()
bob.generateSecretKey()

alice.generateIntermediate(g,p)
bob.generateIntermediate(g,p)

alice.generateKey(bob.interVal)
bob.generateKey(alice.interVal)

alice.hashKey()
bob.hashKey()

people = [alice, bob]

for person in people:
    person.stringify()


message = input("Enter Alice's message : ")
aliceEnc = alice.encrypt(message)
print("Encrypted message of alice using AES : " + str(aliceEnc))
bobDec = bob.decrypt(aliceEnc)
print("Bob decrypted the message and the message is : " + str(bobDec))