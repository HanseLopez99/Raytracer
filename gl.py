import struct
from collections import namedtuple
import numpy as np

from math import cos, sin, tan, pi

from obj import Obj

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])
V4 = namedtuple('Point4', ['x', 'y', 'z', 'w'])

def char(c):
    #1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    #2 bytes
    return struct.pack('=h', w)

def dword(d):
    #4 bytes
    return struct.pack('=l', d)

def color(r, g, b):
    return bytes([int(b * 255),
                  int(g * 255),
                  int(r * 255)] )

def baryCoords(A, B, C, P):

    areaPBC = (B.y - C.y) * (P.x - C.x) + (C.x - B.x) * (P.y - C.y)
    areaPAC = (C.y - A.y) * (P.x - C.x) + (A.x - C.x) * (P.y - C.y)
    areaABC = (B.y - C.y) * (A.x - C.x) + (C.x - B.x) * (A.y - C.y)

    try:
        # PBC / ABC
        u = areaPBC / areaABC
        # PAC / ABC
        v = areaPAC / areaABC
        # 1 - u - v
        w = 1 - u - v
    except:
        return -1, -1, -1
    else:
        return u, v, w

class Raytracer(object):
    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.fov = 60
        self.nearPlane = 0.1
        self.camPosition = V3(0,0,0)

        self.scene = [ ]
        self.lights = [ ]


        self.clearColor = color(0,0,0)
        self.currColor = color(1,1,1)

        self.glViewport(0,0,self.width, self.height)
        
        self.glClear()

    def glViewport(self, posX, posY, width, height):
        self.vpX = posX
        self.vpY = posY
        self.vpWidth = width
        self.vpHeight = height

    def glClearColor(self, r, g, b):
        self.clearColor = color(r,g,b)

    def glColor(self, r, g, b):
        self.currColor = color(r,g,b)

    def glClear(self):
        self.pixels = [[ self.clearColor for y in range(self.height)]
                         for x in range(self.width)]




    def glClearViewport(self, clr = None):
        for x in range(self.vpX, self.vpX + self.vpWidth):
            for y in range(self.vpY, self.vpY + self.vpHeight):
                self.glPoint(x,y,clr)


    def glPoint(self, x, y, clr = None): # Window Coordinates
        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[x][y] = clr or self.currColor

    def scene_intersect(self, orig, dir, sceneObj):
        depth = float('inf')
        intersect = None

        for obj in self.scene:
            hit = obj.ray_intersect(orig, dir)
            if hit != None:
                if sceneObj != hit.sceneObj:
                    if hit.distance < depth:
                        intersect = hit
                        depth = hit.distance

        return intersect

    def cast_ray(self, orig, dir):
        intersect = self.scene_intersect(orig, dir, None)

        if intersect == None:
            return None

        material = intersect.sceneObj.material

        finalColor = np.array([0,0,0])
        objectColor = np.array([material.diffuse[0],
                                material.diffuse[1],
                                material.diffuse[2]])

        dirLightColor = np.array([0,0,0])
        ambLightColor = np.array([0,0,0])


        for light in self.lights:
            if light.lightType == 0: # directional light
                diffuseColor = np.array([0,0,0])

                light_dir = np.array(light.direction) * -1
                intensity = np.dot(intersect.normal, light_dir)
                intensity = float(max(0, intensity))

                diffuseColor = np.array([intensity * light.color[0] * light.intensity,
                                         intensity * light.color[1] * light.intensity,
                                         intensity * light.color[2] * light.intensity])

                #Shadows
                shadow_intensity = 0
                shadow_intersect = self.scene_intersect(intersect.point, light_dir, intersect.sceneObj)
                if shadow_intersect:
                    shadow_intensity = 1


                dirLightColor = np.add(dirLightColor, diffuseColor * (1 - shadow_intensity))

            elif light.lightType == 2: # ambient light
                ambLightColor = np.array(light.color) * light.intensity

        finalColor = dirLightColor + ambLightColor

        finalColor *= objectColor

        r = min(1, finalColor[0])
        g = min(1, finalColor[1])
        b = min(1, finalColor[2])

        return (r,g,b)




    def glRender(self):
        for y in range(self.vpY, self.vpY + self.vpHeight + 1):
            for x in range(self.vpX, self.vpX + self.vpWidth + 1):
                # Pasar de coordenadas de ventana a
                # coordenadas NDC (-1 a 1)
                Px = ((x + 0.5 - self.vpX) / self.vpWidth) * 2 - 1
                Py = ((y + 0.5 - self.vpY) / self.vpHeight) * 2 - 1

                # Proyeccion
                t = tan((self.fov * np.pi / 180) / 2) * self.nearPlane
                r = t * self.vpWidth / self.vpHeight

                Px *= r
                Py *= t

                direction = V3(Px, Py, -self.nearPlane)
                direction = direction / np.linalg.norm(direction)

                rayColor = self.cast_ray(self.camPosition, direction)

                if rayColor is not None:
                    rayColor = color(rayColor[0],rayColor[1],rayColor[2])
                    self.glPoint(x, y, rayColor)





    def glFinish(self, filename):
        with open(filename, "wb") as file:
            # Header
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))

            #InfoHeader
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            #Color table
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])






