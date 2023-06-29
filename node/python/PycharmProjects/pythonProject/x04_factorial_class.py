class Factorial(object):
    def __init__(self, x):
        self.x = x

    def factorial(self):
        if self.x == 0:
            return 1
        else:
            return self.x * Factorial(self.x - 1).factorial()
        ##else를 안 쓰고
        #n = self.x
        #self.x -= 1
        #return n * self.factorial()
        #input = int(input("Input the number : "))
        #fact = Factorial(input)
        #print(f'{input} factorial = {fact.factorial()}')
x = int(input("Input the number : "))
Factorial1 = Factorial(x)
print(f'{x} factorial = {Factorial1.factorial()}')


