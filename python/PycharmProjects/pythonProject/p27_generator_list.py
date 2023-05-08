#리스트 항목을 꺼내서 제곱값을 구해서 출력하는 제너레이터를 생성하시오!
mynums = [1, 2, 3, 4, 5]

def square_number(nums):
   for i in nums:
       yield i * i

generator = square_number(mynums)

for value in generator:
        print(value)


