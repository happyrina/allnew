a = "Hello"
b = 1

try:
    c = a + b #문자열과 더했기 때문에 에러
    print(c)
except:
    print('The Error is occurred')

print(a)