import math

class Vector:
    def __init__(self, *args):
        self.values = list(args)

    def add(self, other):
        if len(self.values) != len(other.values):
            raise ValueError("Vectors must have the same dimensions for addition")
        return Vector(*(a + b for a, b in zip(self.values, other.values)))

    def subtract(self, other):
        if len(self.values) != len(other.values):
            raise ValueError("Vectors must have the same dimensions for subtraction")
        return Vector(*(a - b for a, b in zip(self.values, other.values)))
    
    def multiply(self, scalar):
        return Vector(*(x * scalar for x in self.values))
    
    def elementwise_multiply(self, other):
        if len(self.values) != len(other.values):
            raise ValueError("Vectors must have the same dimensions for element-wise multiplication")
        return Vector(*(a * b for a, b in zip(self.values, other.values)))
    
    def __iter__(self):
        return iter(self.values)

def dot(v1, v2):
    return sum(a*b for a, b in zip(v1.values, v2.values))

def cross(v1, v2):
    i = v1.values[1] * v2.values[2] - v1.values[2] * v2.values[1]
    j = -(v1.values[0] * v2.values[2] - v1.values[2] * v2.values[0])
    k = v1.values[0] * v2.values[1] - v1.values[1] * v2.values[0]
    return Vector(i, j, k)

def norm(v):
    return math.sqrt(sum(x**2 for x in v.values))

def normalize(v):
    magnitude = norm(v)
    if magnitude == 0:
        raise ValueError("Cannot normalize a zero vector")
    return Vector(*(x/magnitude for x in v.values))

# pi
pi = math.pi