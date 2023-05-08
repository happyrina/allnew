class Rectangle(object):
    count = 0

    def __init__(self, width, height):
        Rectangle.count += 1
        self.width = width
        self.height = height

    def calcArea(self):
        return self.width * self.height

    def isSquare(recWidth, recHeight):
        return recWidth == recHeight

    def__add__(self, other):
    obj = Rectangle(self)

    def printCount(cls):
        print(cls.count)



