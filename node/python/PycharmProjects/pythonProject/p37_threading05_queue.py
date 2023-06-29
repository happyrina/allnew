import threading, queue, time

work = queue.Queue()

def generator(start, end):
    for _ in range(start, end):
        work.put(_)
def display():
    while work.empty() is False:
        data = work.get()
        print('data is ' + str(data))
        time.sleep(1)
        work.task_done()2

threading.Thread(target=generator, args=(1,10)).start()
threading.Thread(target=display).start()
work.join() #work = queue.Queue() 위에 이거 의미하고 join은 이걸 연결한다느 뜻

