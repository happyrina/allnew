#60과 28의 최대공약수
def gcd(a, b):
    print("gcd", (a,b))
    while b != 0:
        r = a % b
        a = b
        b = r
        print("gcd", (a,b))
    return a
a = int(input("Input First number : "))
b = int(input("Input Second number : "))

print(f'gcd({a}, {b}) of {a}, {b} : {gcd(a, b)}')


