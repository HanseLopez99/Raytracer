from gl import Raytracer, V3
from texture import *
from figures import *
from lights import *


width = 512
height = 512

# Materiales

brick = Material(diffuse=(0.8, 0.3, 0.3), spec=16)
stone = Material(diffuse=(0.4, 0.4, 0.4), spec=8)

earth = Material(texture=Texture("earthDay.bmp"))
marble = Material(
    diffuse=(0.8, 0.8, 0.8), texture=Texture("marble.bmp"), spec=32, matType=REFLECTIVE
)

marble2 = Material(spec=64, texture=Texture("marble.bmp"), matType=REFLECTIVE)

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

rtx = Raytracer(width, height)

rtx.envMap = Texture("parkingLot.bmp")

rtx.lights.append(AmbientLight(intensity=0.1))
rtx.lights.append(DirectionalLight(direction=(-1, -1, -1), intensity=0.8))

# rtx.scene.append(Plane(position=(0, -10, 0), normal=(0, 1, 0), material=brick))
# rtx.scene.append(Plane(position=(-20, 0, 0), normal=(1, 0, 0), material=stone))
# rtx.scene.append(Plane(position=(15, 30, -15), normal=(-1, -1, -1), material=mirror))

rtx.scene.append(
    Disk(position=(0, -3, -10), normal=(0, 1, 0), radius=3, material=glass)
)

# rtx.scene.append(AABB(position=(-2, -3, -10), size=(2, 2, 2), material=mirror))
# rtx.scene.append(AABB(position=(-2, 2, -10), size=(2, 2, 2), material=glass))
# rtx.scene.append(AABB(position=(-2, 2, -10), size=(2, 2, 2), material=diamond))
# rtx.scene.append(AABB(position=(-2, 2, -10), size=(2, 2, 2), material=marble))

rtx.scene.append(AABB(position=(-2, 2, -10), size=(2, 2, 2), material=marble))

rtx.glRender()

rtx.glFinish("output.bmp")
