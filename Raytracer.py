from gl import Raytracer, V3
from figures import *
from lights import *

# Create Snowman

width = 1920
height = 1080

# Materiales
snow = Material(diffuse=(1, 1, 1), spec=32)
carrot = Material(diffuse=(1, 0.5, 0), spec=16)
black = Material(diffuse=(0, 0, 0), spec=32)
lightGray = Material(diffuse=(0.5, 0.5, 0.5), spec=32)


rtx = Raytracer(width, height)

rtx.lights.append(AmbientLight())
rtx.lights.append(DirectionalLight(direction=(-1, -1, -1)))

# Eyes
rtx.scene.append(Sphere(V3(0.2, 1.5, -4), 0.1, lightGray))
rtx.scene.append(Sphere(V3(0.2, 1.49, -3.94), 0.05, black))
rtx.scene.append(Sphere(V3(-0.2, 1.5, -4), 0.1, lightGray))
rtx.scene.append(Sphere(V3(-0.2, 1.49, -3.94), 0.05, black))
# Nose
rtx.scene.append(Sphere(V3(0, 1.3, -4), 0.12, carrot))
# Mouth
rtx.scene.append(Sphere(V3(0.16, 1.15, -4), 0.04, black))
rtx.scene.append(Sphere(V3(0.06, 1.1, -4), 0.04, black))
rtx.scene.append(Sphere(V3(-0.06, 1.1, -4), 0.04, black))
rtx.scene.append(Sphere(V3(-0.16, 1.15, -4), 0.04, black))
# Body
rtx.scene.append(Sphere(V3(0, 3, -10), 1.2, snow))
rtx.scene.append(Sphere(V3(0, 1, -10), 1.5, snow))
rtx.scene.append(Sphere(V3(0, -2, -10), 2, snow))
# Buttons
rtx.scene.append(Sphere(V3(0, 0.5, -4), 0.1, black))
rtx.scene.append(Sphere(V3(0, -0.28, -4), 0.1, black))
rtx.scene.append(Sphere(V3(0, -0.9, -4), 0.1, black))

rtx.glRender()

rtx.glFinish("output.bmp")
