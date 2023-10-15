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
    
    def magnitude(self):
        return sum(x**2 for x in self.values)**0.5
    
    def __iter__(self):
        return iter(self.values)

def dot(v1, v2):
    if not isinstance(v1, Vector):
        v1 = Vector(*v1)
    if not isinstance(v2, Vector):
        v2 = Vector(*v2)

    return sum(a*b for a, b in zip(v1.values, v2.values))

def cross(v1, v2):
    i = v1.values[1] * v2.values[2] - v1.values[2] * v2.values[1]
    j = -(v1.values[0] * v2.values[2] - v1.values[2] * v2.values[0])
    k = v1.values[0] * v2.values[1] - v1.values[1] * v2.values[0]
    return Vector(i, j, k)

def norm(v):
    return math.sqrt(sum(x**2 for x in v))

def normalize_vector(vector):
    magnitude = math.sqrt(sum(x**2 for x in vector))
    if magnitude != 0:
        return [x / magnitude for x in vector]
    return vector

def solve_quadratic(a, b, c):
    # If a is zero, handle as linear equation
    if a == 0:
        if b == 0:
            return []  # No solution if both a and b are zero
        return [-c/b]

    # Calculate the discriminant
    discriminant = b**2 - 4*a*c

    # If the discriminant is negative, there are no real roots
    if discriminant < 0:
        return []

    # Calculate the two roots
    root1 = (-b + math.sqrt(discriminant)) / (2*a)
    root2 = (-b - math.sqrt(discriminant)) / (2*a)

    return [root1, root2]

def solve_cubic(a, b, c, d):
    # Normalize the equation
    a, b, c, d = b/a, c/a, d/a, 1  # Make sure a is 1

    # Calculate the discriminant and other necessary values
    delta_0 = c**2 - 3*b*d + 12*a*e
    delta_1 = 2*c**3 - 9*b*c*d + 27*b**2*e + 27*a*d**2 - 72*a*c*e
    C = ((delta_1 + math.sqrt(delta_1**2 - 4*delta_0**3)) / 2)**(1/3)

    # If C is zero, use an alternate formula
    if C == 0:
        C = ((delta_1 - math.sqrt(delta_1**2 - 4*delta_0**3)) / 2)**(1/3)

    # Calculate the three roots
    root1 = -1/(3*a) * (b + C + delta_0/C)
    root2 = -1/(3*a) * (b + complex(-1, math.sqrt(3))*C/2 + complex(-1, -math.sqrt(3))*delta_0/(2*C))
    root3 = -1/(3*a) * (b + complex(-1, -math.sqrt(3))*C/2 + complex(-1, math.sqrt(3))*delta_0/(2*C))

    # Return the real parts of the roots
    return [root1.real, root2.real, root3.real]



def solve_quartic(A, B, C, D, E):
    # Check if A is zero
    if A == 0:
        if B == 0:
            # Handle as quadratic
            return solve_quadratic(C, D, E)
        else:
            # Handle as cubic
            return solve_cubic(C, D, E)

    # If A is not zero, proceed with the quartic solution:
    
    # Step 1: Depress the quartic
    p = C/A - 3*B**2/(8*A**2)
    q = D/A + B**3/(8*A**3) - B*C/(2*A**2)
    r = E/A - 3*B**4/(256*A**4) + B**2*D/(16*A**3) - B*C**2/(4*A**2)

    # Step 2 & 3: Introduce a square and choose constants
    # This results in a cubic equation for alpha:
    cubic_coeffs = [1, 2*p, p**2 - 4*r, -q**2]
    alpha = solve_cubic(*cubic_coeffs)  # You'll need to implement solve_cubic

    # Calculate beta and gamma
    beta = math.sqrt(alpha)
    gamma = -q / (2*beta)

    # Step 4: Solve the resulting quadratics
    quadratic1_coeffs = [1, beta, p + alpha + gamma]
    quadratic2_coeffs = [1, -beta, p + alpha - gamma]
    roots1 = solve_quadratic(*quadratic1_coeffs)  # You'll need to implement solve_quadratic
    roots2 = solve_quadratic(*quadratic2_coeffs)  # You'll need to implement solve_quadratic

    return roots1 + roots2




# pi
pi = math.pi