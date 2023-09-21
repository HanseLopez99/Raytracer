import numpy as np
import math_1 as mt

DIR_LIGHT = 0
POINT_LIGHT = 1
AMBIENT_LIGHT = 2


def reflectVector(normal, direction):
    reflect = 2 * mt.dot(normal, direction)
    reflect_vector = reflect
    normal_vector = mt.Vector(*normal)
    reflect = normal_vector.multiply(reflect_vector)

    vector1 = mt.Vector(*reflect)
    vector2 = mt.Vector(*direction)
    reflect = vector1.subtract(vector2)
    reflect = mt.normalize(mt.Vector(*reflect))
    return reflect


class DirectionalLight(object):
    def __init__(self, direction=(0, -1, 0), intensity=1, color=(1, 1, 1)):
        self.direction = mt.normalize(mt.Vector(*direction))
        self.intensity = intensity
        self.color = color
        self.lightType = DIR_LIGHT

    def getDiffuseColor(self, intersect, raytracer):
        light_dir = mt.Vector(*self.direction).multiply(-1)
        intensity = mt.dot(mt.Vector(*intersect.normal), light_dir) * self.intensity
        intensity = max(0, intensity)
        diffuseColor = mt.Vector(
            intensity * self.color[0],
            intensity * self.color[1],
            intensity * self.color[2]
        )
        return diffuseColor.values

    def getSpecColor(self, intersect, raytracer):
        light_dir = mt.Vector(*self.direction).multiply(-1)

        reflect = reflectVector(intersect.normal, light_dir)

        vector1 = mt.Vector(*raytracer.camPosition)
        vector2 = mt.Vector(*intersect.point)
        view_dir = vector1.subtract(vector2)
        view_dir = mt.normalize(mt.Vector(*view_dir))

        # Calculate the specular intensity
        spec_intensity = (
            self.intensity
            * max(0, mt.dot(view_dir, reflect)) ** intersect.sceneObj.material.spec
        )

        # Calculate the specular color
        specColor = mt.Vector(
            spec_intensity * self.color[0],
            spec_intensity * self.color[1],
            spec_intensity * self.color[2]
        )

        return specColor.values  # Return as a list

    def getShadowIntensity(self, intersect, raytracer):
        light_dir = mt.Vector(*self.direction).multiply(-1)


        shadow_intensity = 0
        shadow_intersect = raytracer.scene_intersect(
            intersect.point, light_dir, intersect.sceneObj
        )
        if shadow_intersect:
            shadow_intensity = 1

        return shadow_intensity


class PointLight(object):
    def __init__(self, point, constant=1.0, linear=0.1, quad=0.05, color=(1, 1, 1)):
        self.point = point
        self.constant = constant
        self.linear = linear
        self.quad = quad
        self.color = color
        self.lightType = POINT_LIGHT

    def getDiffuseColor(self, intersect, raytracer):
        
        vector1 = mt.Vector(*self.point)
        vector2 = mt.Vector(*intersect.point)
        light_dir = vector1.subtract(vector2)

        light_dir = mt.normalize(mt.Vector(*light_dir))

        # att = 1 / (Kc + Kl * d + Kq * d * d)
        # attenuation = 1.0 / (self.constant + self.linear * lightDistance + self.quad * lightDistance ** 2)
        attenuation = 1.0
        intensity = mt.dot(mt.Vector(*intersect.normal), light_dir) * attenuation
        intensity = max(0, intensity)
        diffuseColor = mt.Vector(
            intensity * self.color[0],
            intensity * self.color[1],
            intensity * self.color[2]
        )
        return diffuseColor.values

    def getSpecColor(self, intersect, raytracer):
        vector1 = mt.Vector(*self.point)
        vector2 = mt.Vector(*intersect.point)
        light_dir = vector1.subtract(vector2)
        
        light_dir = mt.normalize(mt.Vector(*light_dir))

        reflect = reflectVector(intersect.normal, light_dir)

        vector1 = mt.Vector(*raytracer.camPosition)
        vector2 = mt.Vector(*intersect.point)
        view_dir = vector1.subtract(vector2)

        view_dir = mt.normalize(mt.Vector(*view_dir))

        # att = 1 / (Kc + Kl * d + Kq * d * d)
        # attenuation = 1.0 / (self.constant + self.linear * lightDistance + self.quad * lightDistance ** 2)
        attenuation = 1.0

        spec_intensity = (
            attenuation
            * max(0, mt.dot(view_dir, reflect)) ** intersect.sceneObj.material.spec
        )

        specColor = mt.Vector(
            spec_intensity * self.color[0],
            spec_intensity * self.color[1],
            spec_intensity * self.color[2]
        )
        return specColor.values

    def getShadowIntensity(self, intersect, raytracer):
        vector1 = mt.Vector(*self.point)
        vector2 = mt.Vector(*intersect.point)
        light_dir = vector1.subtract(vector2)
        
        light_dir = mt.normalize(mt.Vector(*light_dir))

        shadow_intensity = 0
        shadow_intersect = raytracer.scene_intersect(
            intersect.point, light_dir, intersect.sceneObj
        )
        if shadow_intersect:
            shadow_intensity = 1

        return shadow_intensity


class AmbientLight(object):
    def __init__(self, intensity=0.1, color=(1, 1, 1)):
        self.intensity = intensity
        self.color = color
        self.lightType = AMBIENT_LIGHT

    def getDiffuseColor(self, intersect, raytracer):
        return mt.Vector(*self.color).multiply(self.intensity).values

    def getSpecColor(self, intersect, raytracer):
        return mt.Vector(0, 0, 0).values

    def getShadowIntensity(self, intersect, raytracer):
        return 0
