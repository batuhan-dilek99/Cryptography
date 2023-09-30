g = int(input("Enter g value : "))
p = int(input("Enter p value : "))

x = int(input("Enter exchanged value X : "))
y = int(input("Enter exchanged value Y : "))

val = 0
for i in range(0,47):
    if ((pow(g,i) % p) == y):
        val = i
        break

print("Secret key for Y : " + str(val))
key = pow(99, val) % p
print("Final key : " + str(key))
