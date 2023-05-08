while True:
    n = input("input number (q = quit) : ")

    if n == "q":
        print("Exit")
        break

    n = int(n)
    if (n < 2 or n > 9):
        print("input number range 2~9!!")
        continue;
    else:
        for x in range(1, 10):
            print(f'{n} * {x} = {n*x}')

# int는 문자로 받는 숫자들을 숫자로만 받기 위해 사용
# 원래 처음에는 n = int(n)이라는 값을 안 주고 n에 다 int(n)으로 만들어서 여러번 줬음 => n = int(n)이라고 지정해주면 모든 n에 int를 주지 않아도 된다!
# 파이썬은 10까지 쓰면 9까지 나옴! 그래서 9단까지 결과값을 얻으려고 했기 때문에 10까지 숫자를 지정





