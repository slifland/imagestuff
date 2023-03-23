import pygame
from PIL import Image
from numpy import random as nprandom
import random
from math import sqrt
from multiprocessing import Process, Manager
import multiprocessing
import time

import reArrange

CHILDREN = 160
# activate the pygame library .

targetImage = Image.open('cool-abstract-graffiti-watercolor-panda-portrait-in-black-and-white-philipp-rietz (1).png').convert('RGB')


# copying from parent, returning with some mutations
def mutateImage(world):
    pixel_map = world.load()
    width, height = world.size
    for i in range(width):
        for j in range(height):
            if random.randint(1, 10) <= 4:
                r, g, b = world.getpixel((i, j))
                new = random.randint(-10, 10)
                if r + new > 255:
                        r = 255 - new
                if g + new > 255:
                        g = 255 - new
                if b + new > 255:
                        b = 255 - new
                if r + new < 0:
                    r = new
                if g + new < 0:
                    g = new
                if b + new < 0:
                    b = new
                pixel_map[i, j] = (r + new, g + new, b + new)

    return world

def synthesize(world, world2):
    pixel_map = world.load()
    width, height = world.size
    for i in range(width):
        for j in range(height):
            pixel_map[i, j] = random.choice([world.load()[i,j], world2.load()[i,j]])
    return world



def findPercentage(world2):
    width, height = targetImage.size
    Value = 0.0
    for i in range(width):
        for j in range(height):
            r, g, b = targetImage.getpixel((i, j))
            r2, g2, b2 = world2.getpixel((i, j))
            Value += (1 - sqrt((r - r2) ** 2 + (g - g2) ** 2 + (b - b2) ** 2) / 441.6722956) / (width * height)
    return Value


def findValue(world2):
    width, height = targetImage.size
    Value = 0.0
    for i in range(width):
        for j in range(height):
            r, g, b = targetImage.getpixel((i, j))
            r2, g2, b2 = world2.getpixel((i, j))
            Value += -1 * sqrt((r - r2) ** 2 + (g - g2) ** 2 + (b - b2) ** 2)
    return Value


def randomImage(world):
    pixel_map = world.load()
    width, height = world.size
    for i in range(width):
        for j in range(height):
            ran = random.randint(0,255)
            pixel_map[i, j] = (ran, ran, ran)
            #pixel_map[i, j] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return world

def shiftPixels(image):
    pixel_map = image.load()
    width, height = image.size
    for i in range(width):
        for j in range(height):
            if i < width - 1:
                pixel_map[i, j] = (pixel_map[i+ 1, j][0], pixel_map[i+ 1, j][1], pixel_map[i+ 1, j][2])
            else:
                pixel_map[i, j] = (pixel_map[0, j][0], pixel_map[0, j][1], pixel_map[0, j][2])
    return image


if __name__ == '__main__':
    with Manager() as manager:
        children = manager.list()
        multiprocessing.freeze_support()
        pygame.init()
        #world2 = targetImage
        world2 = randomImage(targetImage.copy())
        world2 = reArrange.rearrange(targetImage, world2)
        X = 600
        Y = 600
        scrn = pygame.display.set_mode((X, Y))
        world2.save('world2.png', type='PNG')
        imp = pygame.image.load("world2.png").convert()
        scrn.blit(imp, (0, 0))
        pygame.display.flip()
        status = True
        iteration = 0
        pool = multiprocessing.Pool()
        while status:
        #     for i in range(0, CHILDREN):
        #         result = pool.apply(mutateImage, args=[world2])
        #         children.append(result)
        #     maxPerc = findValue(children[0])
        #     maxIndex2 = 1
        #     secHighPerc = findValue(children[1])
        #     maxIndex = 0
        #     k = 0
        #     for i in pool.map(findValue, children, chunksize=10):
        #         if i > maxPerc and i > secHighPerc:
        #             secHighPerc = maxPerc
        #             maxIndex2 = maxIndex
        #             maxPerc = i
        #             maxIndex = k
        #         elif i > secHighPerc:
        #             secHighPerc = i
        #             maxIndex2 = k
        #         k += 1
            pygame.display.set_caption('iteration: ' + str(iteration))
            iteration += 1
            #oldVal = findValue(world2)
            #world3 = synthesize(children[maxIndex], children[maxIndex2])
            # if findValue(world3) > oldVal:
            #     world2 = world3
            # if maxPerc > 0.98:
            #     pause = True
            pause = False
            #print(maxPerc)
            #world2 = shiftPixels(world2)
            world2.save('world2.png', type='PNG')
            scrn.blit(pygame.transform.scale(pygame.image.load('world2.png'), (375, 500)), (0, 0))
            #pause = True
            pygame.display.update()
            while pause:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
            # scrn.blit(pygame.image.load('world2.png'), (0, 0))
            pygame.display.update()
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    status = False
            children[:] = []
    pygame.quit()
