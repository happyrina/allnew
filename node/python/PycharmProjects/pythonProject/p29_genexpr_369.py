# numbers = (i for i in range(1, 101))
# game =(("짝" if('3' in str(i) or '6' in str(i) or '9' in str(i))
#         else str(i) for i in numbers))
#
# print(list(game))

numbers = (i for i in range(1, 101))

for i in list(numbers):
    if i < 10:
        if i in (3, 6, 9):
            print("👏")
        else:
            print(i)
    else:
        st = str(i)
        if st[0] in ("3" , "6", "9") and st[1] in ("3" , "6", "9"):
            print("👏👏")
        elif st[0] in ("3" , "6", "9") or st[1] in ("3" , "6", "9"):
            print("👏")
        else:
            print(i)

#
#
#
# numbers = (i for i in range(1, 101))
#
# data = list(numbers)
#
# item = [3, 6, 9]
#
# for i in data:
#     n10 = int(i/10)
#     n1 = i % 10
#     if i % 10 == 1:
#         print()
#     if i < 10:
#         if i in item:
#             print('짝', end="")
#         else:
#             print("%4d" % i, end="")
#     else:
#         if n10 in item and n1 in item:
#             print('짝짝', end="")
#         elif n10 in item or n1 in item:
#             print('짝', end="")
#         else:
#             print("%4d" % i , end="")