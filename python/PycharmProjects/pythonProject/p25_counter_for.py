import p25_timer

timer = p25_timer.counter2()
counter = 0

for i in range(1, 101):
    if i % 7 == 0:
        counter = timer()
print(f"result : {counter}")

