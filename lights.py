import math_1 as mt

from math import acos,asin

def reflectVector(normal, direction):
    normal_vec = mt.Vector(*normal)
    direction_vec = mt.Vector(*direction)
    
    reflect = normal_vec.multiply(2 * mt.dot(normal_vec, direction_vec))
    reflect = reflect.subtract(direction_vec)
    
    # Manually normalize the reflect vector
    magnitude = reflect.magnitude()
    if magnitude != 0:
        reflect = reflect.multiply(1.0 / magnitude)
    
    return reflect.values




def refractVector(normal, incident, n1, n2):
    c1 = mt.dot(normal, incident)
    if c1 < 0:
        c1 = -c1
    else:
        normal = normal.multiply(-1)
        n1, n2 = n2, n1

    n = n1 / n2
    T = normal.multiply(c1).add(incident).multiply(n).subtract(normal.multiply((1 - n**2 * (1 - c1**2))**0.5))
    T = mt.Vector(*mt.normalize_vector(T.values))
    return T


def totalInternalReflection(normal, incident, n1, n2):
    c1 = mt.dot(normal, incident)
    if c1 < 0:
        c1 = -c1
    else:
        n1, n2 = n2, n1

    if n1 < n2:
        return False

    return acos(c1) >= asin(n2 / n1)

def fresnel(normal, incident, n1, n2):
    c1 = mt.dot(normal, incident)
    if c1 < 0:
        c1 = -c1
    else:
        n1, n2 = n2, n1
     
    s2 = (n1 * (1 - c1 ** 2) ** 0.5) / n2
    c2 = (1 - s2 ** 2) ** 0.5
    
    F1 = (((n2 * c1) - (n1 * c2)) / ((n2 * c1) + (n1 * c2))) ** 2
    F2 = (((n1 * c2) - (n2 * c1)) / ((n1 * c2) + (n2 * c1))) ** 2
    
    Kr = (F1 + F2) / 2
    Kt = 1 - Kr
    return Kr, Kt


class Light(object):
    def __init__(self, intensity=1, color=(1,1,1), lightType="None"):
        self.intensity = intensity
        self.color = color
        self.lightType = lightType
        
    def getLightColor(self):
        return [self.color[0]*self.intensity,
                self.color[1]*self.intensity,
                self.color[2]*self.intensity]
    
    def getDiffuseColor(self, intercept):
        return None
    
    def getSpecularColor(self, intercept, viewPos):
        return None

    
class AmbientLight(Light):
    def __init__(self, intensity=1, color=(1, 1, 1)):
        super().__init__(intensity, color, "Ambient")

    def getDiffuseColor(self, intercept):
        return mt.Vector(*self.color).multiply(self.intensity).values

        
class DirectionalLight(Light):
    def __init__(self, direction=(0,-1,0), intensity=1, color=(1, 1, 1)):
        self.direction = mt.Vector(*mt.normalize_vector(direction))
        super().__init__(intensity, color, "Directional")
        
    def getDiffuseColor(self, intercept):
        dir = self.direction.multiply(-1)
        
        intensity = mt.dot(intercept.normal, dir) * self.intensity
        intensity = max(0, min(1, intensity))
        intensity *= 1 - intercept.obj.material.Ks
        diffuseColor = [i * intensity for i in self.color]
        
        return diffuseColor
    
    def getSpecularColor(self, intercept, viewPos):
        dir = self.direction.multiply(-1)
        
        reflect = reflectVector(intercept.normal, dir)
        
        viewDir = mt.Vector(*viewPos).subtract(mt.Vector(*intercept.point))
        viewDir = mt.Vector(*mt.normalize_vector(viewDir.values))
        
        specIntensity = max(0, mt.dot(viewDir, reflect)) ** intercept.obj.material.spec
        specIntensity *= intercept.obj.material.Ks
        specIntensity *= self.intensity
        
        specColor = [i * specIntensity for i in self.color]
        
        return specColor

    
class PointLight(Light):
    def __init__(self, point=(0,0,0), intensity=1, color=(1, 1, 1)):
        self.point = mt.Vector(*point)
        super().__init__(intensity, color, "Point")
        
    def getDiffuseColor(self, intercept):
        dir = self.point.subtract(mt.Vector(*intercept.point))
        R = dir.magnitude()
        dir = mt.Vector(*mt.normalize_vector(dir.values))
        
        intensity = mt.dot(intercept.normal, dir) * self.intensity
        intensity *= 1 - intercept.obj.material.Ks
        
        # Ley de cuadrados inversos
        # IF = Intensity/R^2
        # R is the distance from the intercept point to the point light
        if R != 0:
            intensity /= R**2
        
        intensity = max(0, min(1, intensity))
        diffuseColor = [i * intensity for i in self.color]
        
        return diffuseColor
    
    def getSpecularColor(self, intercept, viewPos):
        dir = self.point.subtract(mt.Vector(*intercept.point))
        R = dir.magnitude()
        dir = mt.Vector(*mt.normalize_vector(dir.values))
        
        reflect = reflectVector(intercept.normal, dir)
        
        viewDir = mt.Vector(*viewPos).subtract(mt.Vector(*intercept.point))
        viewDir = mt.Vector(*mt.normalize_vector(viewDir.values))
        
        specIntensity = max(0, mt.dot(viewDir, reflect)) ** intercept.obj.material.spec
        specIntensity *= intercept.obj.material.Ks
        specIntensity *= self.intensity
        
        if R != 0:
            specIntensity /= R**2
        
        specIntensity = max(0, min(1, specIntensity))
        specColor = [i * specIntensity for i in self.color]
        
        return specColor

