def prime(n):   # n = 4
    for i in range(2, n):
        if n % i == 0:
            return 1
        else:
            return 0
## prime_func.py
# def prime(n):
#     for k in (2, n):
#         if n % k == 0:
#             break
#     if k == n:
#         return 1
#     else:
#         return 0







