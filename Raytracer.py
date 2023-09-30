from gl import Raytracer, V3
from texture import *
from figures import *
from lights import *
import random as rd


width = 1920
height = 1080

# Materiales

brick = Material(diffuse=(0.8, 0.3, 0.3), spec=16)
stone = Material(diffuse=(0.4, 0.4, 0.4), spec=8)
earth = Material(texture=Texture("earthDay.bmp"))
marble = Material(
    diffuse=(0.8, 0.8, 0.8), texture=Texture("marble.bmp"), spec=32, matType=REFLECTIVE
)
canica = Material(
    diffuse=(0.8, 0.8, 1.0),
    texture=Texture("whiteMarble.bmp"),
    spec=32,
    ior=1.5,
    matType=TRANSPARENT,
)
mirror = Material(diffuse=(0.9, 0.9, 0.9), spec=64, matType=REFLECTIVE)
glass = Material(diffuse=(0.9, 0.9, 0.9), spec=64, ior=1.5, matType=TRANSPARENT)
diamond = Material(diffuse=(0.9, 0.9, 0.9), spec=64, ior=2.417, matType=TRANSPARENT)

# Limit random to not allow dark colors
randomValue = rd.random() * 0.5 + 0.5

RandomMaterialTransparent = Material(diffuse=(randomValue, randomValue, randomValue), spec=64, ior=1.5, matType=TRANSPARENT)
RandomMaterialReflective = Material(diffuse=(randomValue, randomValue, randomValue), spec=64, ior=1.5, matType=REFLECTIVE)


rtx = Raytracer(width, height)

rtx.envMap = Texture("Stonewall.bmp")

rtx.lights.append(AmbientLight(intensity=0.1))
rtx.lights.append(DirectionalLight(direction=(-1, -1, -1), intensity=0.8))

# Earth
rtx.scene.append(Sphere(V3(-7, 4, -13), 2, earth))
# Brick
rtx.scene.append(Sphere(V3(-7, -4, -13), 2, brick))

# Marble
rtx.scene.append(Sphere(V3(0, 4, -13), 2, marble))
# Mirror
rtx.scene.append(Sphere(V3(0, -4, -13), 2, RandomMaterialReflective))

# Canica
rtx.scene.append(Sphere(V3(7, 4, -13), 2, canica))
# Glass
rtx.scene.append(Sphere(V3(7, -4, -13), 2, RandomMaterialTransparent))

# Stone
rtx.scene.append(Sphere(V3(7, -4, -18), 1.6, stone))


rtx.glRender()

rtx.glFinish("output.bmp")
