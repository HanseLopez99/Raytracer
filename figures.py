import math
import numpy as np
import math_1 as mt

WHITE = (1, 1, 1)
BLACK = (0, 0, 0)

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2


class Intersect(object):
    def __init__(self, distance, point, normal, texcoords, sceneObj):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.texcoords = texcoords
        self.sceneObj = sceneObj


class Material(object):
    def __init__(self, diffuse=WHITE, spec=1.0, ior=1.0, texture=None, matType=OPAQUE):
        self.diffuse = diffuse
        self.spec = spec
        self.ior = ior
        self.texture = texture
        self.matType = matType


class Sphere(object):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def ray_intersect(self, orig, dir):
        L = mt.Vector(*self.center).subtract(mt.Vector(*orig))
        tca = mt.dot(L, mt.Vector(*dir))
        
        # Replacing L.magnitude() with the square root of the dot product of L with itself
        d = (mt.dot(L, L) - tca**2) ** 0.5

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
        P = mt.Vector(*orig).add(mt.Vector(*dir).multiply(t0))
        normal = P.subtract(mt.Vector(*self.center))
        normal = mt.normalize(normal)

        u = 1 - ((math.atan2(normal.values[2], normal.values[0]) / (2 * math.pi)) + 0.5)
        v = math.acos(-normal.values[1]) / math.pi

        uvs = (u, v)

        return Intersect(
            distance=t0, point=P.values, normal=normal.values, texcoords=uvs, sceneObj=self
        )

