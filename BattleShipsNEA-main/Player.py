for x in range(1000000):
    b = int("1" + str(x))
    if 3*b == int(str(x) + "1"):
        print(x)
