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