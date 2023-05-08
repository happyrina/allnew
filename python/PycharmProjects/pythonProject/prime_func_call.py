import prime_func

a = int(input("Input first number : "))
print(f"{prime_func.prime(a)}")
# if prime_func.prime(a) == 1:

if prime_func.prime(a) == 1:
    print("소수가 아님")
else:
    print("소수임")

## prime_func_call.py

# import prime_func
#
# while True:
#     n = int(input("Input number(0 : Quit) : "))
#
#     if (n == 0):
#         break
#     if (n < 2) :
#         print("re-enter number~!!")
#         continue
#     print(f"{n} is prime number") if prime_func.prime(n) == 1 else print(f"{n} is not prime number")