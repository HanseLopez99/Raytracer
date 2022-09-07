from gl import Raytracer, V3
from figures import *
from lights import *


width = 1024
height = 1024

# Materiales

brick = Material(diffuse = (0.8, 0.3, 0.3))
stone = Material(diffuse = (0.4, 0.4, 0.4))
grass = Material(diffuse = (0.3, 1, 0.3))



rtx = Raytracer(width, height)

rtx.lights.append( AmbientLight( ))
rtx.lights.append( DirectionalLight(direction = (-1,-1,-1) ))


rtx.scene.append( Sphere(V3(0,0,-10), 2, brick)  )
rtx.scene.append( Sphere(V3(-4,-2,-15), 1.5, stone)  )
rtx.scene.append( Sphere(V3(2,2,-8), 0.2, grass)  )


rtx.glRender()

rtx.glFinish("output.bmp")