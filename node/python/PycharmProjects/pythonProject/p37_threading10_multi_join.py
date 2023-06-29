import threading, time

data = 0
lock = threading.Lock()

def generator(start, end):
    global data
    for _ in range(start, end):
        lock.acquire()
        buf = data
        time.sleep(0.01)
        data = buf + 1
        lock.release() #락을 안 걸면 자기 마음대로 나온다!

t1 = threading.Thread(target=generator, args=(1, 10))
t2 = threading.Thread(target=generator, args=(1, 10))

t1.start()
t2.start()

t1.join()
t2.join()

print(data)

