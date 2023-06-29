import random
class findMax(object):
    def __init__(self, data):
        self.data = data
    def max(self):
        max_value = self.data[0]
        for i in range(1, len(self.data)):
            if self.data[i] > max_value:
                max_value = self.data[i]
            return max_value


data = random.sample(range(1,101),10)
print(data)

data1 = findMax(data)
print(f'Max value is : {data1.max()}')


