import calc_class

a = int(input('Input first number : '))
b = int(input('Input first number : '))

my = calc_class.Calc(a, b)

print(f'{a} + {b} = {my.add()}')
print(f'{a} - {b} = {my.sub()}')