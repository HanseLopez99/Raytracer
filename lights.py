import math_1 as mt

DIR_LIGHT = 0
POINT_LIGHT = 1
AMBIENT_LIGHT = 2


def reflectVector(normal, direction):
    # Calculate the reflection vector
    reflect_coefficient = 2 * mt.dot(mt.Vector(*normal), mt.Vector(*direction))
    reflect = mt.Vector(*normal).multiply(reflect_coefficient)
    reflect = reflect.subtract(mt.Vector(*direction))
    reflect = mt.normalize(reflect)
    
    return reflect.values  # Return as a list



def refractVector(normal, direction, ior):
    # Snell's Law
    cosi = max(-1, min(1, mt.dot(mt.Vector(*direction), mt.Vector(*normal))))
    etai = 1
    etat = ior

    if cosi < 0:
        cosi = -cosi
    else:
        etai, etat = etat, etai
        normal = mt.Vector(*normal).multiply(-1)

    eta = etai / etat
    k = 1 - (eta**2) * (1 - (cosi**2))

    if k < 0:  # Total Internal Reflection
        return None

    R = mt.Vector(*direction).multiply(eta).add(mt.Vector(*normal).multiply(eta * cosi - k**0.5))
    return R.values  # Return as a list



def fresnel(normal, direction, ior):
    # Fresnel Equation
    cosi = max(-1, min(1, mt.dot(direction, normal)))
    etai = 1
    etat = ior

    if cosi > 0:
        etai, etat = etat, etai

    sint = etai / etat * (max(0, 1 - cosi**2) ** 0.5)

    if sint >= 1:  # Total Internal Reflection
        return 1

    cost = max(0, 1 - sint**2) ** 0.5
    cosi = abs(cosi)

    Rs = ((etat * cosi) - (etai * cost)) / ((etat * cosi) + (etai * cost))
    Rp = ((etai * cosi) - (etat * cost)) / ((etai * cosi) + (etat * cost))

    return (Rs**2 + Rp**2) / 2



class DirectionalLight(object):
    def __init__(self, direction=(0, -1, 0), intensity=1, color=(1, 1, 1)):
        self.direction = mt.normalize(mt.Vector(*direction)).values
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

        return diffuseColor.values  # Return as a list

    def getSpecColor(self, intersect, raytracer):
        light_dir = mt.Vector(*self.direction).multiply(-1).values
        reflect = reflectVector(intersect.normal, light_dir)

        view_dir_vector = mt.Vector(*raytracer.camPosition).subtract(mt.Vector(*intersect.point))
        view_dir = mt.normalize(view_dir_vector).values

        spec_intensity = (
            self.intensity
            * max(0, mt.dot(mt.Vector(*view_dir), mt.Vector(*reflect))) ** intersect.sceneObj.material.spec
        )
        specColor = mt.Vector(
            spec_intensity * self.color[0],
            spec_intensity * self.color[1],
            spec_intensity * self.color[2]
        )

        return specColor.values

    def getShadowIntensity(self, intersect, raytracer):
        light_dir = mt.Vector(*self.direction).multiply(-1).values

        shadow_intensity = 0
        shadow_intersect = raytracer.scene_intersect(
            intersect.point, light_dir, intersect.sceneObj
        )
        if shadow_intersect:
            shadow_intensity = 1

        return shadow_intensity



class PointLight(object):
    def __init__(self, point, constant=1.0, linear=0.1, quad=0.05, color=(1, 1, 1)):
        self.point = mt.Vector(*point)
        self.constant = constant
        self.linear = linear
        self.quad = quad
        self.color = color
        self.lightType = POINT_LIGHT

    def getDiffuseColor(self, intersect, raytracer):
        light_dir = self.point.subtract(mt.Vector(*intersect.point))
        light_dir = mt.normalize(light_dir)

        # You can uncomment and adjust the attenuation calculation if needed
        # lightDistance = self.point.distance_to(mt.Vector(*intersect.point))
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
        light_dir = self.point.subtract(mt.Vector(*intersect.point))
        light_dir = mt.normalize(light_dir)

        reflect = reflectVector(intersect.normal, light_dir)

        view_dir = mt.Vector(*raytracer.camPosition).subtract(mt.Vector(*intersect.point))
        view_dir = mt.normalize(view_dir)

        # You can uncomment and adjust the attenuation calculation if needed
        # lightDistance = self.point.distance_to(mt.Vector(*intersect.point))
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
        light_dir = self.point.subtract(mt.Vector(*intersect.point))
        light_dir = mt.normalize(light_dir)

        shadow_intensity = 0
        shadow_intersect = raytracer.scene_intersect(
            intersect.point, light_dir.values, intersect.sceneObj
        )
        if shadow_intersect:
            shadow_intensity = 1

        return shadow_intensity



class AmbientLight(object):
    def __init__(self, intensity=0.1, color=(1, 1, 1)):
        self.intensity = intensity
        self.color = color
        self.lightType = AMBIENT_LIGHT

    def getDiffuseColor(self):
        diffuseColor = mt.Vector(*self.color).multiply(self.intensity)
        return diffuseColor.values  # Return as a lidst

    def getSpecColor(self):
        return mt.Vector(0, 0, 0).values  # Return as a list

    def getShadowIntensity(self):
        return 0

