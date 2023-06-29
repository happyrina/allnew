class animal:
    def __init__(self, name):
        self.name = name

    def move(self):
        print("move!")

class Dog(animal):
    def speak(self):
        print("Bark!")

class Duck(animal):
    def speak(self):
        print( "Quack!")


# class Animal:
#     def __init__(self, name):
#         self.name = name
#
#     def move(self):
#         print(f'{self.name} is moving.')
#
#     def speak(self):
#         pass / 뭔가를 정의하지 않은걸 표현하고 싶지 않으면 pass로 표현해 준다
#
# class Dog(Animal):
#     def speak(self):
#         print(f'{self.name} says "Bark!"')
#
#
# class Duck(Animal):
#     def speak(self):
#         print(f'{self.name} says "Quack!"')
