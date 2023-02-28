"""
conway.py 
A simple Python/matplotlib implementation of Conway's Game of Life.
"""

import sys, argparse
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import rotate_matrix
import datetime

ON = 255
OFF = 0
vals = [ON, OFF]

def randomGrid(N):
    """returns a grid of NxN random values"""
    return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N)

def generateGrid(N,M):
    return np.random.choice(vals, N*M, p=[0.2, 0.8]).reshape(N, M)

def addGlider(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[0,    0, 255], 
                       [255,  0, 255], 
                       [0,  255, 255]])
    grid[i:i+3, j:j+3] = glider

block = np.array([[0,0,0,0],
                 [0,255,255,0],
                 [0,255,255,0],
                 [0,0,0,0]])

beehive = np.array([[0,0,0,0,0,0],
                    [0,0,255,255,0,0],
                    [0,255,0,0,255,0],
                    [0,0,255,255,0,0],
                    [0,0,0,0,0,0]])

loaf = np.array([[0,0,0,0,0,0],
                [0,0,255,255,0,0],
                [0,255,0,0,255,0],
                [0,0,255,0,255,0],
                [0,0,0,255,0,0],
                [0,0,0,0,0,0]])

boat = np.array([[0,0,0,0,0],
                [0,255,255,0,0],
                [0,255,0,255,0],
                [0,0,255,0,0],
                [0,0,0,0,0]])

tub = np.array([[0,0,0,0,0],
                [0,0,255,0,0],
                [0,255,0,255,0],
                [0,0,255,0,0],
                [0,0,0,0,0]])

blinker = np.array([[0,0,0,0,0],
                [0,0,255,0,0],
                [0,0,255,0,0],
                [0,0,255,0,0],
                [0,0,0,0,0]])

toad1 = np.array([[0,0,0,0,0,0],
                [0,0,0,255,0,0],
                [0,255,0,0,255,0],
                [0,255,0,0,255,0],
                [0,0,255,0,0,0],
                [0,0,0,0,0,0]])

toad2 = np.array([[0,0,0,0,0,0],
                [0,0,0,0,0,0],
                [0,0,255,255,255,0],
                [0,255,255,255,0,0],
                [0,0,0,0,0,0],
                [0,0,0,0,0,0]])

beacon1 = np.array([[0,0,0,0,0,0],
                [0,255,255,0,0,0],
                [0,255,255,0,0,0],
                [0,0,0,255,255,0],
                [0,0,0,255,255,0],
                [0,0,0,0,0,0]])

beacon2 = np.array([[0,0,0,0,0,0],
                [0,255,255,0,0,0],
                [0,255,0,0,0,0],
                [0,0,0,0,255,0],
                [0,0,0,255,255,0],
                [0,0,0,0,0,0]])

glider1 = np.array([[0,0,0,0,0],
                [0,0,255,0,0],
                [0,0,0,255,0],
                [0,255,255,255,0],
                [0,0,0,0,0]])

glider2 = np.array([[0,0,0,0,0],
                [0,255,0,255,0],
                [0,0,255,255,0],
                [0,0,255,0,0],
                [0,0,0,0,0]])

spaceship1 = np.array([[0,0,0,0,0,0,0],
                [0,255,0,0,255,0,0],
                [0,0,0,0,0,255,0],
                [0,255,0,0,0,255,0],
                [0,0,255,255,255,255,0],
                [0,0,0,0,0,0,0]])

spaceship2 = np.array([[0,0,0,0,0,0,0],
                [0,0,0,255,255,0,0],
                [0,255,255,0,255,255,0],
                [0,255,255,255,255,0,0],
                [0,0,255,255,0,0,0],
                [0,0,0,0,0,0,0]])

o = open("Output.txt","w")
generations = 200
first = True
firstFrame = 0

def update(frameNum, img, grid, N, M):
    # copy grid since we require 8 neighbors for calculation
    # and we go line by line 
    newGrid = grid.copy()
    for y in range(N):
        for x in range(M):
            neighbours = 0
            for i in range(-1,2):
                for j in range(-1,2):
                    if (x+i >= 0 and x+i < M and y+j >= 0 and y+j < N):
                        if (grid[y+j,x+i] == 255):
                            neighbours += 1

            if(grid[y,x] == 255):
                neighbours -= 1
                if(neighbours < 2 or neighbours > 3):
                    newGrid[y,x] = 0
            else:
                if(neighbours == 3):
                    newGrid[y,x] = 255

    global block
    global beehive
    global loaf
    global boat
    global tub
    global blinker
    global toad1
    global toad2
    global beacon1
    global beacon2
    global glider1
    global glider2
    global spaceship1
    global spaceship2

    blockC = 0
    beehiveC = 0
    loafC = 0
    boatC = 0
    tubC = 0
    blinkerC = 0
    toadC = 0
    beaconC = 0
    gliderC = 0
    spaceshipC = 0 
    
    for y in range(N):
        for x in range(M):
            if(x <= M - 4 and y <= N - 4 and (newGrid[y:y+4,x:x+4] == block).all()):
                blockC += 1

            if(x <= M - 6 and y <= N - 5 and (newGrid[y:y+5,x:x+6] == beehive).all()):
                beehiveC += 1

            if(x <= M - 5 and y <= N - 6 and (newGrid[y:y+6,x:x+5] == rotate_matrix.clockwise(beehive)).all()):
                beehiveC += 1

            if(x <= M - 6 and y <= N - 6):
                for i in range(4):
                    if((newGrid[y:y+6,x:x+6] == loaf).all()):
                        loafC += 1
                    loaf = rotate_matrix.clockwise(loaf)

            if(x <= M - 5 and y <= N - 5):
                for i in range(4):
                    if((newGrid[y:y+5,x:x+5] == boat).all()):
                        boatC += 1
                    boat = rotate_matrix.clockwise(boat)

            if(x <= M - 5 and y <= N - 5 and (newGrid[y:y+5,x:x+5] == tub).all()):
                tubC += 1

            if(x <= M - 5 and y <= N - 5):
                for i in range(2):
                    if((newGrid[y:y+5,x:x+5] == blinker).all()):
                        blinkerC += 1
                    blinker = rotate_matrix.clockwise(blinker)

            if(x <= M - 6 and y <= N - 6):
                for i in range(2):
                    for i in range(2):
                        if((newGrid[y:y+6,x:x+6] == toad1).all() or (newGrid[y:y+6,x:x+6] == toad2).all()):
                            toadC += 1
                        toad1 = rotate_matrix.clockwise(toad1)
                        toad2 = rotate_matrix.clockwise(toad2)
                    toad1 = np.array(toad1)
                    toad2 = np.array(toad2)
                    toad1.transpose()
                    toad2.transpose()

            if(x <= M - 6 and y <= N - 6):
                for i in range(2):
                    if((newGrid[y:y+6,x:x+6] == beacon1).all() or (newGrid[y:y+6,x:x+6] == beacon2).all()):
                        beaconC += 1
                    beacon1 = rotate_matrix.clockwise(beacon1)
                    beacon2 = rotate_matrix.clockwise(beacon2)

            if(x <= M - 5 and y <= N - 5):
                for i in range(2):
                    for i in range(4):
                        if((newGrid[y:y+5,x:x+5] == glider1).all() or (newGrid[y:y+5,x:x+5] == glider2).all()):
                            gliderC += 1
                        glider1 = rotate_matrix.clockwise(glider1)
                        glider2 = rotate_matrix.clockwise(glider2)
                    glider1 = np.array(glider1)
                    glider2 = np.array(glider2)
                    glider1.transpose()
                    glider2.transpose()

            for i in range(2):
                for i in range(2):
                    if(x <= M - 7 and y <= N - 6):
                        if((newGrid[y:y+6,x:x+7] == spaceship1).all() or (newGrid[y:y+6,x:x+7] == spaceship2).all()):
                            spaceshipC += 1
                    spaceship1 = rotate_matrix.clockwise(spaceship1)
                    spaceship2 = rotate_matrix.clockwise(spaceship2)
                    if(x <= M - 6 and y <= N - 7):
                        if((newGrid[y:y+7,x:x+6] == spaceship1).all() or (newGrid[y:y+7,x:x+6] == spaceship2).all()):
                            spaceshipC += 1
                    spaceship1 = rotate_matrix.clockwise(spaceship1)
                    spaceship2 = rotate_matrix.clockwise(spaceship2)

                spaceship1 = np.array(spaceship1)
                spaceship2 = np.array(spaceship2)
                spaceship1.transpose()
                spaceship2.transpose()

    global generations
    global o
    global first
    global firstFrame
    total = blockC + beehiveC + loafC + boatC + tubC + blinkerC + toadC + beaconC + gliderC + spaceshipC
    if(total == 0):
        total = 1

    if(frameNum < generations):
        o.write("Iteration: " + str(frameNum + 1 + firstFrame) + "\n")
        o.write("Block: \t\t" + str(blockC) + "\tPercent: " + str(int(blockC/total*100)) + "\n")
        o.write("Beehive: \t" + str(beehiveC) + "\tPercent: " + str(int(beehiveC/total*100)) + "\n")
        o.write("Loaf: \t\t" + str(loafC) + "\tPercent: " + str(int(loafC/total*100)) + "\n")
        o.write("Boat: \t\t" + str(boatC) + "\tPercent: " + str(int(boatC/total*100)) + "\n")
        o.write("Tub: \t\t" + str(tubC) + "\tPercent: " + str(int(tubC/total*100)) + "\n")
        o.write("Blinker: \t" + str(blinkerC) + "\tPercent: " + str(int(blinkerC/total*100)) + "\n")
        o.write("Toad: \t\t" + str(toadC) + "\tPercent: " + str(int(toadC/total*100)) + "\n")
        o.write("Beacon: \t" + str(beaconC) + "\tPercent: " + str(int(beaconC/total*100)) + "\n")
        o.write("Glider: \t" + str(gliderC) + "\tPercent: " + str(int(gliderC/total*100)) + "\n")
        o.write("Spaceship: \t" + str(spaceshipC) + "\tPercent: " + str(int(spaceshipC/total*100)) + "\n\n")

    if(first):
        firstFrame = 1
        first = False

    # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

# main() function
def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life system.py.")
    # TODO: add arguments
    f = open("Test04.txt","r")

    # set grid size
    N = 200 #Height
    M = 300 #Width
    M, N = f.readline().split(" ")
    M = int(M)
    N = int(N)

    o.write("Simulation at " + datetime.datetime.now().strftime("%x") + "\n")
    o.write("Universe size " + str(M) + " x " + str(N) + "\n\n")

    # set animation update interval
    updateInterval = 50

    # declare grid
    grid = np.array([])
    #grid = generateGrid(N, M) #Random grid

    grid = np.zeros((N,M), dtype = int)

    global generations
    generations = int(f.readline())
    for line in f:
        y, x = line.split(" ")
        x = int(x)
        y = int(y)
        grid[x,y] = 255
    
    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, M), 
                                                    frames = 200, 
                                                    interval=updateInterval, 
                                                    save_count=200)
    '''ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, M,), 
                                                    frames = 200, 
                                                    interval=updateInterval)'''

    plt.show()

# call main
if __name__ == '__main__':
    main()