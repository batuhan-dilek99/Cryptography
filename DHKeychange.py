class Person: 

    def __init__(self, secretNum, g, p, name):
        self.secretNum = secretNum
        self.g, self.p = g, p
        self.name = name

    def generateIntermediate(self):
        val = pow(self.g, self.secretNum) % self.p
        print("\n\nGenerating intermediate values for " + self.name)
        print("-----------------------------------------------")
        print(str(self.g) + "^" + str(self.secretNum) + " mod " + str(self.p) + " = " + str(val) + "\n")

        return val
    
    def generateKey(self, otherVal):
        
        print("\n\nKey generation for " + self.name)
        print("----------------------------------")
        key = pow(otherVal, self.secretNum) % self.p
        print(str(otherVal) + "^" + str(self.secretNum) + " mod " + str(self.p))
        return key
    



g = int(input("Input g value : "))
p = int(input("Input p value : "))
aliceSecretValue = int(input("Enter alice's secret number : "))
bobSecretValue = int(input("Enter bob's secret number : "))
alice = Person(aliceSecretValue, g, p, "alice")
bob = Person(bobSecretValue, g, p, "bob")

alicePubVal = alice.generateIntermediate()
bobPubVal = bob.generateIntermediate()

aliceKey = str(alice.generateKey(bobPubVal))
bobKey = str(bob.generateKey(alicePubVal))

print("\n\nAlice's key : " + aliceKey + "\nBob's key : " + bobKey)

if (aliceKey == bobKey):
    print("Same key")

