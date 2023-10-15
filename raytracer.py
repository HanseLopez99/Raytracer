import pygame
from pygame.locals import *

from rt import RayTracer
from figures import *
from lights import *
from materials import *


width = 900
height = 900

pygame.init()

screen = pygame.display.set_mode((width,height),pygame.DOUBLEBUF|pygame.HWACCEL|pygame.HWSURFACE)
screen.set_alpha(None)

raytracer = RayTracer(screen)
raytracer.envMap = pygame.image.load("textures/parkingLot.bmp")
raytracer.rtClearColor(0.25,0.25,0.25)

#Texturas
earthTexture = pygame.image.load("textures/earthDay.bmp")
wallTexture = pygame.image.load("textures/wall.bmp")
marbleTexture = pygame.image.load("textures/marble.bmp")
whiteMarbleTexture = pygame.image.load("textures/whiteMarble.bmp")

#Materiales
brick = Material(diffuse=(1,0.4,0.4),spec=8,Ks=0.01)
grass = Material(diffuse=(0.4,1,0.4),spec=32,Ks=0.1)
water = Material(diffuse=(0.4,0.4,1),spec=256,Ks=0.2)
concrete = Material(diffuse=(0.5,0.5,0.5),spec=256,Ks=0.2)
wall = Material(texture = wallTexture,spec=64,Ks=0.1)
marble = Material(texture=marbleTexture, spec=64, Ks=0.1)
whiteMarble = Material(texture=whiteMarbleTexture, spec=64, Ks=0.1)
blue_metal = Material(diffuse=(0.4,0.4,1),spec=64,Ks=0.2,matType=REFLECTIVE)

mirror = Material(diffuse=(0.9,0.9,0.9),spec=64,Ks=0.2,matType=REFLECTIVE)
earth = Material(texture = earthTexture,spec=64,Ks=0.1,matType=OPAQUE)
glass = Material(diffuse=(0.9,0.9,0.9),spec=64,Ks=0.15,ior=1.5,matType=TRANSPARENT)
diamond = Material(diffuse=(0.9,0.9,0.9),spec=128,Ks=0.2,ior=2.417,matType=TRANSPARENT)
realWater = Material(diffuse=(0.4,0.4,0.9),spec=128,Ks=0.2,ior=1.33,matType=TRANSPARENT)
torus_material = Material(diffuse=(0.9, 0.5, 0.3), spec=64, Ks=0.2, matType=OPAQUE)



width = 100
height = 100
depth = 600

# Left wall
raytracer.scene.append(Plane(position=(-width,height/2,0),normal=(1,0,0),material=blue_metal))
# Right wall
raytracer.scene.append(Plane(position=(width,height/2,0),normal=(-1,0,0),material=blue_metal))
# Ceiling
raytracer.scene.append(Plane(position=(0,height,0),normal=(0,-1,0),material=marble))
# Floor
raytracer.scene.append(Plane(position=(0,-height/2,0),normal=(0,1,0),material=concrete))
# Back wall
raytracer.scene.append(Plane(position=(0,height/2,-depth/2),normal=(0,0,1),material=brick))
# Front wall behind camera
raytracer.scene.append(Plane(position=(0,height/2,depth/2),normal=(0,0,-1),material=brick))

# Torus
torus_center = (0, 0, -5)  # Example position
major_radius = 2
minor_radius = 1
torus = Torus(center=torus_center, major_radius=major_radius, minor_radius=minor_radius, material=torus_material)
raytracer.scene.append(torus)


# Disks
raytracer.scene.append(Disk(position=(2.1,0.6,-5),normal=(-1,0,0),radius=1,material=mirror))
raytracer.scene.append(Disk(position=(0,0.5,-10),normal=(0,0,-1),radius=1.5,material=mirror))
raytracer.scene.append(Disk(position=(-2.1,0.6,-5),normal=(-1,0,0),radius=1,material=mirror))
raytracer.scene.append(Disk(position=(0, -3, -6), normal=(0, 1, 0), radius=3, material=mirror))

# Lights
raytracer.lights.append(AmbientLight(intensity=1))
raytracer.lights.append(DirectionalLight(direction=(0,0,-1),intensity=0.9))
raytracer.lights.append(PointLight(point=(1.5,0,-5),intensity=1,color=(1,1, 0)))

raytracer.rtClear()
raytracer.rtRender()

print("\nRender Time:",pygame.time.get_ticks()/1000,"secs")

isRunning = True
while isRunning:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			isRunning = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				isRunning = False

# Ensure the display module is initialized
pygame.display.init()

# Update the display to ensure all previous draw calls are reflected
pygame.display.flip()

# Capture the entire screen surface
screenshot = pygame.Surface((width, height))
screenshot.blit(screen, (0, 0))

# Save the screenshot
pygame.image.save(screenshot, "screenshot.jpg")


pygame.quit()