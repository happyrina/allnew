class SmartPhone(object):
    def __init__(self, brand, details):
        self.brand = brand
        self.details = details
    def __str__(self):
        return f'str : {self.brand} - {self.details}'
    def __repr__(self):
        return f'repr : Instant_name = SmartPhone({self.brand} - {self.details})'
    #이걸 하려면 뭘 해라! 이렇게 설명? str써논 이유도 여기에는 이런 멤버들이 존재해~ 라는 것을 알려주는 것임

    def __doc__(self):
        return f'This class is Smart Phone Class. It is have a brand name and detail description.'


SmartPhone1 = SmartPhone('IPhone', {'color' : 'White',
'price' : 10000})
SmartPhone2 = SmartPhone('Galaxy', {'color' : 'Black',
'price' : 8000})
SmartPhone3 = SmartPhone('Blackberry', {'color' : 'Silver',
'price' : 6000})

print(dir(SmartPhone1))
print(SmartPhone1.__dict__)
print(SmartPhone2.__dict__)
print(SmartPhone3.__dict__)

print(id(SmartPhone1))
print(id(SmartPhone2))
print(id(SmartPhone3))

print(SmartPhone1.brand == SmartPhone2.brand)
print(SmartPhone1 is SmartPhone2)

print(SmartPhone.__str__(SmartPhone1))
print(SmartPhone.__repr__(SmartPhone2)) #객체를 어떤 식으로 사용해서 써라!
print(SmartPhone.__doc__) #none 호출을 한 적이 없음
#설명서와 같은 것...?