### ================================ Base implementation for Tutorial 9 ================= ###
### ====================== Implements Point addition and Scalar Multiplication ========== ###

from dataclasses import dataclass
from re import I
from random import randint
import string
import random
from Cryptodome.Hash import SHA256
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend
import base64
import os
from Cryptodome.Cipher import AES
from Cryptodome.Cipher import Salsa20

@dataclass
class PrimeGaloisField:
    prime: int

    def __contains__(self, field_value: "FieldElement") -> bool:
        return 0 <= field_value.value < self.prime


@dataclass
class FieldElement:
    value: int
    field: PrimeGaloisField

    def __repr__(self):
        return "0x" + f"{self.value:x}".zfill(64)
        
    @property
    def P(self) -> int:
        return self.field.prime
    
    def __add__(self, other: "FieldElement") -> "FieldElement":
        return FieldElement(
            value=(self.value + other.value) % self.P,
            field=self.field
        )
    
    def __sub__(self, other: "FieldElement") -> "FieldElement":
        return FieldElement(
            value=(self.value - other.value) % self.P,
            field=self.field
        )

    def __rmul__(self, scalar: int) -> "FieldValue":
        return FieldElement(
            value=(self.value * scalar) % self.P,
            field=self.field
        )

    def __mul__(self, other: "FieldElement") -> "FieldElement":
        return FieldElement(
            value=(self.value * other.value) % self.P,
            field=self.field
        )
        
    def __pow__(self, exponent: int) -> "FieldElement":
        return FieldElement(
            value=pow(self.value, exponent, self.P),
            field=self.field
        )

    def __truediv__(self, other: "FieldElement") -> "FieldElement":
        other_inv = other ** -1
        return self * other_inv


@dataclass
class EllipticCurve:
    a: int
    b: int

    field: PrimeGaloisField

    def __contains__(self, point: "ECCPoint") -> bool:
        x, y = point.x, point.y
        return y ** 2 == x ** 3 + self.a * x + self.b

    def __post_init__(self):
        # Encapsulate the int parameters in FieldElement
        self.a = FieldElement(self.a, self.field)
        self.b = FieldElement(self.b, self.field)

        # Whether the members of the curve parameters are in the field
        if self.a not in self.field or self.b not in self.field:
            raise ValueError

inf = float("inf")

# Representing an ECC Point using the curve equation yˆ2 = xˆ3 + ax + b
@dataclass
class ECCPoint:
    x: int
    y: int

    curve: EllipticCurve

    def __post_init__(self):
        if self.x is None and self.y is None:
            return
        
        # Encapsulate x and y in FieldElement
        self.x = FieldElement(self.x, self.curve.field)
        self.y = FieldElement(self.y, self.curve.field)

        # Ensure the ECCPoint satisfies the curve equation
        if self not in self.curve:
            raise ValueError

    ##  ======== Point addition P1 + P2 = P3 ============== ##
    def __add__(self, other):
        if self == I:                       # I + P2 = P2
            return other

        if other == I:
            return self                     # P1 + I = P1

        if self.x == other.x and self.y == (-1 * other.y):
            return I                        # P + (-P) = I

        if self.x != other.x:
            x1, x2 = self.x, other.x
            y1, y2 = self.y, other.y

            out = (y2 - y1) / (x2 - x1)
            x3 = out ** 2 - x1 - x2
            y3 = out * (x1 - x3) - y1

            return self.__class__(
                x = x3.value,
                y = y3.value,
                curve = curve256k1
            )

        if self == other and self.y == inf:
            return I

        if self == other:
            x1, y1, a = self.x, self.y, self.curve.a

            out = (3 * x1 ** 2 + a) / (2 * y1)
            x3 = out ** 2 - 2 * x1
            y3 = out * (x1 - x3) - y1

            return self.__class__(
                x = x3.value,
                y = y3.value,
                curve = curve256k1
            )

    ##  ======== Scalar Multiplication x * P1 = P1 ============== ##
    def __rmul__(self, scalar: int) -> "ECCPoint":
        inPoint = self
        outPoint = I

        while scalar:
            if scalar & 1:
                outPoint = outPoint + inPoint
            inPoint = inPoint + inPoint
            scalar >>= 1
        return outPoint


# Using the secp256k1 elliptic curve equation: yˆ2 = xˆ3 + 7
# Prime of the finite field
# Necessary parameters for the cryptographic operations
P: int = (
    0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
)

field = PrimeGaloisField(prime=P)

A: int = 0
B: int = 7

curve256k1 = EllipticCurve(
    a=A,
    b=B,
    field=field
)   

I = ECCPoint(x = None, y = None, curve = curve256k1)    # where I is a point at Infinity

# Generator point of the chosen group
G = ECCPoint(
    x = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    y = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
    curve = curve256k1
)

# Order of the group generated by G, such that nG = I
q = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141


## ==================== Start your implementation below this line ============================== ##
## ==================== Feel free to pull the parameters into another file if you wish ========= ##
## ==================== If you notice any bugs, kindly draw our attention to it ================ ##


class Person:
    def __init__(self, char):
        self.username = "ID_" + char
        self.xi = randint(0,q)
        self.pi = G.__rmul__(self.xi)
        self.ri = randint(0,q)
        self.Ri = G.__rmul__(self.ri)
    
    def setDi(self, di):
        self.di = di


    def generateUandV(self):
        self.l = randint(0,q)
        self.h = randint(0,q)
        self.U = G.__rmul__(self.l)
        self.V = G.__rmul__(self.h)
    
    def calculateSessionKey(self):
        # hasher = SHA256.new()
        # hasher.update(val.encode('utf-8'))
        #selfKab = 
        print()



class Server:
    def __init__(self):
        self.x = randint(0,q)
        self.pubP = G.__rmul__(self.x)
        self.users = []
        self.userDict = {}
        self.aesKey = os.urandom(16)

    #Using Cantor pairing in order to 
    
    
    
    def calculateDi(self, ID, ri, Pi):
        hasher = SHA256.new()
        val = str(ID) + str(ri) + str(Pi)
        hasher.update(val.encode('utf-8'))
        result = str(ri) + hasher.hexdigest()
        return result

    
    def encrypt(self, key, plaintext):
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(plaintext) + padder.finalize()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        encodedciphertext = base64.b64encode(ciphertext)
        return encodedciphertext


    def registerUsers(self, item):
        self.users.append(item)

    def calculateKeys(self, di, xi, Ri, Pi, username, object):
        sk = self.encrypt(self.aesKey, str(di + str(xi)).encode())
        Pk = self.encrypt(self.aesKey, str(str(Ri) + str(Pi)).encode())
        object.sk = sk
        object.pk = Pk
        self.registerUsers(object)
        return (sk, Pk)

    def calculateSessionKey(self, by, to):
        hasher = SHA256.new()
        #Calculation of values h and l for both users and storing it in a dictionary
        self.la = randint(0,q)
        self.ha = randint(0,q)
        self.Ua = G.__rmul__(self.la)
        self.Va = G.__rmul__(self.ha)
        for user in self.users:
            if user.username == to:
                #getting first 8 bytes of PB to be able to multiply it with Ppub
                byteArrayofPk = bytearray(user.pk)
                first8bytesToInt = int.from_bytes(bytes(byteArrayofPk[0:8]))
                #-----------
                #Converting the username value to a int value in order to be able to multiply it with Ppub
                encodedUsername = user.username.encode("utf-8")
                intValueOfusername = int.from_bytes(encodedUsername)
                #-----------
                #Calculation of the Value Y
                #Multiplying the above values with pubP
                ECCUsername = self.pubP.__rmul__(intValueOfusername)
                ECCPk8byte = self.pubP.__rmul__(first8bytesToInt)
                #Forging the hash
                val2beHashed = str(ECCPk8byte.x) + str(ECCUsername.y)
                hasher.update(val2beHashed.encode())
                hashRes = hasher.hexdigest()
                Y = str(user.Ri) + hashRes + str(user.pi)
                intValofY = int.from_bytes(Y.encode())
                self.T = self.ha * intValofY
                #-----------
                #Calculate Kab
                kabhash = str(Y) + str(self.Va) + str(self.T) + user.username +str(user.pi.x) + str(user.pi.y)
                hasher.update(kabhash.encode())
                finalHash = hasher.hexdigest()
                print("\nKab hash : " + finalHash)
                self.sessionKeyHexDigest = finalHash
                self.sessionKeyDigest = hasher.digest()
                #-----------
            
    def sendMessage(self, by, to, message):
        encryptedMessage = self.encrypt(self.sessionKeyDigest, message.encode())
        print("Encrypted ciphertext : ", encryptedMessage.decode())
        return encryptedMessage
    
    def encapsulate(self, by,to,message):
        #"by" is where does the message originated from, and "to" is where will the message be recieved
        encryptedMessage = self.sendMessage(by,to,message)
        hasher = SHA256.new()
        #H(U,CAB,T,IDA,IDB,PA,PB) the items PA and PB are ECCPoints 
        #I summed them up in a variable
        #I summed up IDA and IDB into a IDX variable.
        PAB = by.pi.__add__(to.pi)
        intIDA = int.from_bytes(by.username.encode())
        intIDB = int.from_bytes(to.username.encode())
        #-----------------------------------
        val2beHashed = str(self.Ua.x) + str(self.Ua.y) + encryptedMessage.decode() + str(self.T) + str(intIDA) + str(intIDB)
        hasher.update(val2beHashed.encode())
        H = hasher.digest()
        HhexDigest = hasher.hexdigest()

        #Calculating the W by changing every value to an int and performing the operations
        da = int.from_bytes(by.di.encode())
        hashInt = int.from_bytes(H)
        W = da + (self.la * hashInt) + (by.xi * hashInt)
        print("\nW value : " + "\n" + str(W))


    


    

def main():

    server = Server()
    #Alice and Bob set their public values in their constructors.
    alice = Person("A")
    bob = Person("B")

#Exercise 1-------------------------------------------------------------
    #Calculating and setting di value
    alice.setDi(server.calculateDi(alice.username, alice.ri, alice.pi))
    bob.setDi(server.calculateDi(bob.username, bob.ri, bob.pi))

    #Calculating sk and PK
    server.calculateKeys(alice.di,alice.xi,alice.Ri,alice.pi, alice.username, alice)
    server.calculateKeys(bob.di,bob.xi,bob.Ri,bob.pi,bob.username, bob)
    #alice.setPKandSK(server.calculateKeys(alice.di,alice.xi,alice.Ri,alice.pi, alice.username, alice))
    #bob.setPKandSK(server.calculateKeys(bob.di,bob.xi,bob.Ri,bob.pi,bob.username, bob))

    print(str(alice.username) + "\n------------------------")
    print("SK : \n "+ str(alice.sk) + "\n")
    print("PK : \n" + str(alice.pk)) 
    print("\n\n" + str(bob.username) + "\n------------------------")
    print("SK : \n "+ str(bob.sk) + "\n")
    print("PK : \n" + str(bob.pk)) 
#-----------------------------------------------------------------------

#Exercise 2-------------------------------------------------------------
    server.calculateSessionKey(alice.username, bob.username)
    #send message to bob
    server.encapsulate(alice,bob,"Hey Bob! I am Alice!")


#-----------------------------------------------------------------------

if __name__ == "__main__":
    main()




