import random
from Cryptodome.Hash import SHA256
from Cryptodome.Util import Padding
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
        print(str(otherVal) + "^" + str(self.secretKey) + " mod " + str(p))
        self.sharedKey = key
        return key
    
    def hashKey(self):
        hash = SHA256.new()
        paddedBytes = bytes(Padding.pad(str(self.sharedKey).encode("utf-8"), 64))
        #paddedBytes = bytes(str(self.sharedKey), "utf-8")
        hash.update(paddedBytes)
        print(len(hash.hexdigest()))
        #print(hash.__sizeof__())


    def stringify(self):
        print("Name : " + self.name)
        print("-----------------")
        print("Secret Key : " + str(self.secretKey))
        print("First intermediate value : " + str(self.interValFirst))
        print("Shared key : " + str(self.sharedKey))
        print()

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