class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other_vector):
        self.x += other_vector.x
        self.y += other_vector.y

    def __sub__(self, other_vector):
        self.x -= other_vector.x
        self.y -= other_vector.y

    def __mul__(self, number):
        self.x *= number
        self.y *= number

    def __truediv__(self, number):
        self.x /= number
        self.y /= number
