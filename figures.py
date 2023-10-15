import math_1 as mt
from math import tan, pi, atan2, acos

class Intercept(object):
    def __init__(self, distance, point, normal, texcoords, obj):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.texcoords = texcoords
        self.obj = obj

class Shape(object):
    def __init__(self, position, material):
        self.position = position
        self.material = material

    def ray_intersect(self, orig, dir):
        return None

class Sphere(Shape):
    def __init__(self, position, radius, material):
        self.radius = radius
        super().__init__(position, material)

    def ray_intersect(self, orig, dir):
        L = mt.Vector(*self.position).subtract(mt.Vector(*orig))
        tca = mt.dot(L, mt.Vector(*dir))
        d = (L.magnitude() ** 2 - tca ** 2) ** 0.5

        if d > self.radius:
            return None

        thc = (self.radius ** 2 - d ** 2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None

        P = mt.Vector(*orig).add(mt.Vector(*dir).multiply(t0))
        normal = P.subtract(mt.Vector(*self.position))
        normal = mt.Vector(*mt.normalize_vector(normal.values))


        u = (atan2(normal.values[2], normal.values[0]) / (2 * pi)) + 0.5
        v = acos(normal.values[1]) / pi

        return Intercept(distance=t0, point=P.values, normal=normal.values, texcoords=(u, v), obj=self)
    
class Plane(Shape):
    def __init__(self, position, normal, material):
        self.normal = mt.Vector(*mt.normalize_vector(normal))

        super().__init__(position, material)
        
    def ray_intersect(self, orig, dir):
        denom = mt.dot(mt.Vector(*dir), self.normal)
        
        if abs(denom) <= 0.0001:
            return None
        
        num = mt.dot(mt.Vector(*self.position).subtract(mt.Vector(*orig)), self.normal)
        t = num / denom
        
        if t < 0:
            return None
        
        P = mt.Vector(*orig).add(mt.Vector(*dir).multiply(t))
        
        return Intercept(distance=t, point=P.values, normal=self.normal.values, texcoords=None, obj=self)


class Disk(Plane):
    def __init__(self, position, normal, radius, material):
        self.radius = radius
        super().__init__(position, normal, material)
        
    def ray_intersect(self, orig, dir):
        planeIntersect = super().ray_intersect(orig, dir)
        
        if planeIntersect is None:
            return None
        
        contactDistanceVector = mt.Vector(*planeIntersect.point).subtract(mt.Vector(*self.position))
        contactDistance = contactDistanceVector.magnitude()
        
        if contactDistance > self.radius:
            return None
        
        return Intercept(distance=planeIntersect.distance,
                         point=planeIntersect.point,
                         normal=self.normal,
                         texcoords=None,
                         obj=self)

    
class AABB(Shape):
    # Axis Aligned Bounding Box
    
    def __init__(self, position, size, material):
        self.size = size
        super().__init__(position, material)
        
        self.planes = []
        self.size = size
        
        # Sides
        leftPlane = Plane(mt.Vector(*self.position).add(mt.Vector(-size[0]/2, 0, 0)), mt.Vector(-1, 0, 0), material)
        rightPlane = Plane(mt.Vector(*self.position).add(mt.Vector(size[0]/2, 0, 0)), mt.Vector(1, 0, 0), material)
        
        bottomPlane = Plane(mt.Vector(*self.position).add(mt.Vector(0, -size[1]/2, 0)), mt.Vector(0, -1, 0), material)
        topPlane = Plane(mt.Vector(*self.position).add(mt.Vector(0, size[1]/2, 0)), mt.Vector(0, 1, 0), material)
    
        backPlane = Plane(mt.Vector(*self.position).add(mt.Vector(0, 0, -size[2]/2)), mt.Vector(0, 0, -1), material)
        frontPlane = Plane(mt.Vector(*self.position).add(mt.Vector(0, 0, size[2]/2)), mt.Vector(0, 0, 1), material)
        
        self.planes.extend([leftPlane, rightPlane, bottomPlane, topPlane, backPlane, frontPlane])
        
        # Bounds
        self.boundsMin = [0, 0, 0]
        self.boundsMax = [0, 0, 0]
        
        bias = 0.001
        
        for i in range(3):
            self.boundsMin[i] = self.position[i] - (bias + size[i] / 2)
            self.boundsMax[i] = self.position[i] + (bias + size[i] / 2)
            
    def ray_intersect(self, orig, dir):
        intersect = None
        t = float('inf')
        
        u = 0
        v = 0
        
        for plane in self.planes:
            planeIntersect = plane.ray_intersect(orig, dir)
            
            if planeIntersect:
                planePoint = planeIntersect.point
                if self.boundsMin[0] < planePoint[0] < self.boundsMax[0]:
                    if self.boundsMin[1] < planePoint[1] < self.boundsMax[1]:
                        if self.boundsMin[2] < planePoint[2] < self.boundsMax[2]:
                            if planeIntersect.distance < t:
                                t = planeIntersect.distance
                                intersect = planeIntersect
                                
                                # Generate the UVs
                                if abs(plane.normal.values[0]) > 0:
                                    # On X, use Y and Z for UVs
                                    u = (planePoint[1] - self.boundsMin[1]) / (self.size[1] + 0.002)
                                    v = (planePoint[2] - self.boundsMin[2]) / (self.size[2] + 0.002)
                                elif abs(plane.normal.values[1]) > 0:
                                    # On Y, use X and Z for UVs
                                    u = (planePoint[0] - self.boundsMin[0]) / (self.size[0] + 0.002)
                                    v = (planePoint[2] - self.boundsMin[2]) / (self.size[2] + 0.002)
                                elif abs(plane.normal.values[2]) > 0:
                                    # On Z, use X and Y for UVs
                                    u = (planePoint[0] - self.boundsMin[0]) / (self.size[0] + 0.002)
                                    v = (planePoint[1] - self.boundsMin[1]) / (self.size[1] + 0.002)
                                
        if not intersect:
            return None
        
        return Intercept(distance=t, point=intersect.point, normal=intersect.normal, texcoords=(u, v), obj=self)

class Torus(object):
    def __init__(self, center, major_radius, minor_radius, material):
        self.center = mt.Vector(*center)
        self.major_radius = major_radius
        self.minor_radius = minor_radius
        self.material = material


    def ray_intersect(self, orig, dir):
        # Initialize coefficients for the quartic equation
        A = B = C = D = E = 0
        # ... (This is where you'll substitute the ray's equation into the torus equation and collect terms)

        # Solve the quartic equation to get potential t values
        # You might need an external method or library to solve the quartic equation
        t_values = mt.solve_quartic(A, B, C, D, E)

        # Filter out negative t values and find the smallest positive t
        t_values = [t for t in t_values if t > 0]
        if not t_values:
            return None
        t = min(t_values)

        # Calculate the intersection point
        P = orig.add(dir.multiply(t))
        # Calculate the normal at the intersection point
        normal = ...  # This will require some additional logic using your Vector class

        return Intersect(
            distance=t,
            point=list(P),
            normal=list(normal),
            texcoords=None,  # You can add texture coordinates logic if needed
            sceneObj=self
        )
