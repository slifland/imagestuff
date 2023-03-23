from numpy import random
from math import sqrt
from queue import PriorityQueue


def rearrange(oldImage, randomImage):
    increment = 0.1
    pixel_map = oldImage.load()  # image trying to recreate
    pixel_map2 = randomImage.load()  # image being shuffled
    newPixels = []
    oldPixels = []
    q = PriorityQueue()
    width, height = randomImage.size
    for i in range(width):
        for j in range(height):
            newPixels.append(newPixel(pixel_map2[i, j][0], pixel_map2[i, j][1], pixel_map2[i, j][2]))
    for i in range(width):
        for j in range(height):
            print(str(i) + " : " + str(j))
            oldPixels.append(oldPixel(i, j, pixel_map[i, j][0], pixel_map[i, j][1], pixel_map[i, j][2], newPixels))
    for i in oldPixels:
        try:
            q.put((i.distanceHighest(), i))
        except TypeError:
            q.put((i.distanceHighest() + (increment / random.random()), i))
            increment = random.random()
    requiredDistance = 5
    while q.qsize() > 0:
        while q.queue[0][0] < requiredDistance:
            if q.queue[0][1].pixelWanted.filled:
                q.queue[0][1].reAllocate(newPixels)
                if q.queue[0][0] != q.queue[0][1].distanceHighest():
                    temp = q.get()
                    q.put((temp[1].distanceHighest(), temp[1]))
                continue
            old = q.get()
            npix = old[1].pixelWanted
            pixel_map[old[1].row, old[1].col] = (npix.r, npix.g, npix.b)
            npix.filled = True
            newPixels.remove(npix)
            print(q.qsize())
            if q.qsize() == 0:
                break
        requiredDistance += 5
    return oldImage


def distance(r, g, b, r2, g2, b2):
    return sqrt((r - r2) ** 2 + (g - g2) ** 2 + (b - b2) ** 2)


class oldPixel:
    currModifier = 0.1

    def __init__(self, row, col, r, g, b, newPixels):
        self.row = row
        self.col = col
        self.r = r
        self.g = g
        self.b = b
        self.pixelWanted = self.reAllocate(newPixels)

    def distanceHighest(self):
        return distance(self.r, self.g, self.b, self.pixelWanted.r, self.pixelWanted.g, self.pixelWanted.b)

    def reAllocate(self, newPixels):
        index = 0
        best = 10000000
        for i in range(len(newPixels)):
            if newPixels[i].filled:
                continue
            if distance(self.r, self.g, self.b, newPixels[i].r, newPixels[i].g, newPixels[i].b) < best:
                index = i
                best = distance(self.r, self.g, self.b, newPixels[i].r, newPixels[i].g, newPixels[i].b)
        self.pixelWanted = newPixels[index]
        return newPixels[index]

    def __lt__(self, other):
        return True


class newPixel:
    def __init__(self, r, g, b):
        self.filled = False
        self.r = r
        self.g = g
        self.b = b