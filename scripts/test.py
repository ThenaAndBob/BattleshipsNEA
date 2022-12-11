k = 5
d = 9

a5 = (k*d)%10
a4 = (k*a5)%10 + (k*d)//10
a3 = (k*a4)%10 + (a5*k)//10

n1 = (k*d)%10
n2 = (k*a5)%10 + (k*d)//10
print(d)
print(n1)
print(n2)
nextPrint = n2
while nextPrint != d:
    nextPrint = (k*n2)%10 + (k*n1)//10
    print(nextPrint)
    n1 = n2
    n2 = nextPrint
    input()
