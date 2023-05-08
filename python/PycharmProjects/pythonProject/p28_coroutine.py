def handler():
    print("Initialize Handler")
    while True:
        value = (yield)
        print("%s + %s = %s" % (value[0], value[1], value[0]+value[1]))

listener = handler()
listener.__next__()
listener.send([5, 4])
listener.send([3, 6])

def handler():
     print("Initialize Handler")
     while True:
         v1, v2 = (yield)
         print(f"{v1} + {v2} = {v1 + v2}")

listener = handler()
listener.__next__()
listener.send([5, 4])
listener.send([3, 6])