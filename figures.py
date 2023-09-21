import numpy as np
import math_1 as mt

WHITE = (1, 1, 1)
BLACK = (0, 0, 0)

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2


class Intersect(object):
    def __init__(self, distance, point, normal, sceneObj):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.sceneObj = sceneObj


class Material(object):
    def __init__(self, diffuse=WHITE, spec=1.0, matType=OPAQUE):
        self.diffuse = diffuse
        self.spec = spec
        self.matType = matType


class Sphere(object):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def ray_intersect(self, orig, dir):
        vector1 = mt.Vector(*self.center)
        vector2 = mt.Vector(*orig)
        L = vector1.subtract(vector2)

        tca = mt.dot(L, dir)
        d = (mt.norm(L) ** 2 - tca**2) ** 0.5

        if d > self.radius:
            return None

        thc = (self.radius**2 - d**2) ** 0.5

        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None

        # P = O + t0 * D
        orig_vector = mt.Vector(*orig)
        dir_vector = mt.Vector(*dir).multiply(t0)  # Assuming you have a multiply method in the Vector class
        P = orig_vector.add(dir_vector)

        center_vector = mt.Vector(*self.center)
        normal = P.subtract(center_vector)

        normal = mt.normalize(normal)


        return Intersect(distance=t0, point=P, normal=normal, sceneObj=self)
