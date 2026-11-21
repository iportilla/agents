#find prime numbers less 100

for num in range(2, 100):
    prime = True
    for i in range(2, num):
        if num % i == 0:
            prime = False
            break
    if prime:
        print(num)  



#now for a given n

n = int(input("Enter a number: "))
for num in range(2, n):
    prime = True
    for i in range(2, num):
        if num % i == 0:
            prime = False
            break
    if prime:
        print(num)

#optimized version for a given n
n = int(input("Enter a number: "))
for num in range(2, n):
    prime = True
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            prime = False
            break
    if prime:
        print(num)
#optimized version for a given n
n = int(input("Enter a number: "))
for num in range(2, n):
    prime = True
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            prime = False
            break
    if prime:
        print(num)