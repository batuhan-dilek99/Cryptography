import random

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

    
    def generateIntermediateFirst(self, g, p):
        val = pow(g, self.secretKey) % p
        print("Generating first intermediate values for " + self.name + " :")
        print(str(g) + "^" + str(self.secretKey) + " mod " + str(p) + " = " + str(val) + "\n")
        self.interValFirst = val
        return val
    
    def generateIntermediateSecond(self, otherVal, g, p):
        val = pow(otherVal, self.secretKey) % p
        print("Generating second intermediate values for " + self.name + " :")
        print(str(g) + "^" + str(self.secretKey) + " mod " + str(p) + " = " + str(val) + "\n")
        self.interValSecond = val
        return val
    
    def generateKey(self, otherVal):
        
        print("Key generation for " + self.name + " :")
        key = pow(otherVal, self.secretKey) % p
        print(str(otherVal) + "^" + str(self.secretKey) + " mod " + str(p))
        self.sharedKey = key
        return key
    
    def stringify(self):
        print("Name : " + self.name)
        print("-----------------")
        print("Secret Key : " + str(self.secretKey))
        print("First intermediate value : " + str(self.interValFirst))
        print("Second intermediate value : " + str(self.interValSecond))
        print("Shared key : " + str(self.sharedKey))
        print()

alice = Person("Alice")
bob = Person("Bob")
charlie = Person("Charlie")



primes = [i for i in range (2,10000) if alice.isPrime(i)]
p = random.choice(primes)
g = random.choice(primes)

print("P value is (randomly generated) : " + str(p))
print("G value is (randomly generated) : " + str(g))
print()

alice.generateSecretKey()
bob.generateSecretKey()
charlie.generateSecretKey()

alice.generateIntermediateFirst(g, p)
bob.generateIntermediateFirst(g, p)
charlie.generateIntermediateFirst(g, p)

bob.generateIntermediateSecond(alice.interValFirst, g, p)
charlie.generateIntermediateSecond(bob.interValFirst, g, p)
alice.generateIntermediateSecond(charlie.interValFirst, g, p)

alice.generateKey(charlie.interValSecond)
bob.generateKey(alice.interValSecond)
charlie.generateKey(bob.interValSecond)

people = [alice,bob,charlie]

print("\n")
for person in people:
    person.stringify()