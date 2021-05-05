def saveId(id):
    f = open("userId.txt", "w")
    f.write(str(id))
    f.close()


def read():
    f = open("userId.txt", "r")
    return int(f.read())
