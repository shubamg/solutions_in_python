a = 4

def f1(x, ba=a):
    return ba


a += 1


def f2(x, ba=a):
    return ba


print(f1(0), f2(0))
