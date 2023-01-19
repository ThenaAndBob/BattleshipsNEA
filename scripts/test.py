<<<<<<< HEAD
int("A")
=======
def odd(n):
    return (3*n  + 1)//2

def even(n):
    return n//2

n = 20 ** 100000 + 53
while n != 1:
    if n % 2 ==0:
        n = even(n)
    else:
        n = odd(n)
    try:
        print(n)
    except:pass
>>>>>>> 9f0162c6071c29dc2d2cb05320a8d9665cf77d9e
