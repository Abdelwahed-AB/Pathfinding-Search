from Colors import ColorCode
from pygame.locals import *
from Grid import *
import time
import pygame
import sys
from random import randint

rgb = pygame.Color
clock = pygame.time.Clock()
# Pygame window attributes
WINDOW_SIZE = (610, 410)
FPS = 60

# init Pygame
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
# Learning about pathfinding / search algorithms

g = Grid(screen, dimensions=WINDOW_SIZE)

def BreadthFS(start=(0, 0), end=(g.x_elems - 1, g.y_elems - 1)):
    g.reset(False)
    end = g.grid[end[1]][end[0]]
    # Paths to extend
    agenda = [[g.grid[start[1]][start[0]]]]
    # already visited / checked / extended
    extendedList = []

    while agenda:
        path = agenda.pop(0)
        if path[-1] == end:
            for node in path:  # For Drawing the final path
                node.isPath = True
            g.draw()
            pygame.display.update()
            print(len(path))  # Return the path (might need it in the future)
            return
        elif path[-1] not in extendedList:  # Check if we visited the current node before or not
            extendedList.append(path[-1])
            for node in path[-1].neighbours:
                # Check if the next node is a wall and check if it was already visited (Makes it a bit faster (Which I think is a bit weird), I tested it without the check)
                if node not in extendedList and not node.isWall:
                    path.append(node)
                    agenda.append(path.copy())  # Add to the back of the que
                    path.pop(-1)

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_b:
                    return
        # Draw the current node (green) + checked nodes(red)
        path[-1].isCurrent = True
        g.draw()
        path[-1].isCurrent = False
        path[-1].checked = True
        pygame.display.update()
    return(None)


def DepthFS(start=(0, 0), end=(g.x_elems - 1, g.y_elems - 1)):
    g.reset(False)
    """Not the best for open grids"""
    end = g.grid[end[1]][end[0]]
    # Paths to extend
    agenda = [[g.grid[start[1]][start[0]]]]
    # already visited / checked / extended
    extendedList = []

    while agenda:
        path = agenda.pop(0)
        if path[-1] == end:
            for node in path:  # For Drawing the final path
                node.isPath = True
            g.draw()
            pygame.display.update()
            print(len(path))
            return  # Return the path (might need it in the future)
        elif path[-1] not in extendedList:  # Check if we visited the current node before or not
            extendedList.append(path[-1])
            for node in path[-1].neighbours:
                # Check if the next node is a wall
                if node not in extendedList and not node.isWall:
                    path.append(node)
                    agenda.insert(0, path.copy())  # Add to the front of the queue
                    path.pop(-1)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_d:
                    return
        # Draw the current node (green) + checked nodes(red)
        path[-1].isCurrent = True
        g.draw()
        path[-1].isCurrent = False
        path[-1].checked = True
        pygame.display.update()
    return(None)


def BestFS(start=(0, 0), end=(g.x_elems - 1, g.y_elems - 1)):
    g.reset(False)
    end = g.grid[end[1]][end[0]]
    # Paths to extend
    openSet = [g.grid[start[1]][start[0]]]
    # already visited / checked / extended
    closedSet = []
    while openSet:
        lowest = 0
        for i in range(len(openSet)):
            if openSet[i].f < openSet[lowest].f:
                lowest = i

        current = openSet[lowest]

        if current == end:
            path = []  # If we ever need it
            tmp = current
            tmp.isPath = True
            path.append(tmp)
            while tmp.camefrom != None:
                path.append(tmp.camefrom)
                tmp = tmp.camefrom
                tmp.isPath = True  # Draw the path
            g.draw()
            pygame.display.update()
            print(len(path))
            return

        # Mark the current node as visited / checked
        openSet.remove(current)
        closedSet.append(current)

        # Draw the current node (green) + checked nodes(red)
        current.isCurrent = True
        g.draw()
        current.isCurrent = False
        current.checked = True
        pygame.display.update()

        for node in current.neighbours:
            if not node.isWall and not node in closedSet:
                if not node in openSet:
                    openSet.append(node)

                node.f = node.distance(end)
                node.camefrom = current
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_v:
                    return


def HillClimb(start=(0, 0), end=(g.x_elems - 1, g.y_elems - 1)):
    g.reset(False)
    """Not the best for open grids"""
    end = g.grid[end[1]][end[0]]
    # Paths to extend
    agenda = [[g.grid[start[1]][start[0]]]]
    # already visited / checked / extended
    extendedList = []

    while agenda:
        path = agenda.pop(0)
        if path[-1] == end:
            for node in path:  # For Drawing the final path
                node.isPath = True
            g.draw()
            pygame.display.update()
            print(len(path))
            return  # Return the path (might need it in the future)
        elif path[-1] not in extendedList:  # Check if we visited the current node before or not
            extendedList.append(path[-1])
            a = []  # The paths that will be added to the agenda after being sorted
            for node in path[-1].neighbours:
                # Check if the next node is a wall
                if node not in extendedList and not node.isWall:
                    path.append(node)
                    a.append(path.copy())  # Add to a
                    path.pop(-1)

            # Sort a
            if a:
                min = a[0][-1].distance(end)
                for i in range(len(a)):
                    d = a[i][-1].distance(end)
                    if d < min:
                        t = a[0]
                        a[0] = a[i]
                        a[i] = t
                        min = d
                for p in a[::-1]:
                    agenda.insert(0, p)

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_h:
                    return
        # Draw the current node (green) + checked nodes(red)
        path[-1].isCurrent = True
        g.draw()
        path[-1].isCurrent = False
        path[-1].checked = True
        pygame.display.update()
    return(None)



def Djikstra(start=(0, 0), end=(g.x_elems - 1, g.y_elems - 1)):
    g.reset(False)
    end = g.grid[end[1]][end[0]]
    # Paths to extend
    openSet = [g.grid[start[1]][start[0]]]
    # already visited / checked / extended
    closedSet = []
    while openSet:
        lowest = 0
        for i in range(len(openSet)):
            if openSet[i].f < openSet[lowest].f:
                lowest = i

        current = openSet[lowest]

        if current == end:
            path = []  # If we ever need it
            tmp = current
            tmp.isPath = True
            path.append(tmp)
            while tmp.camefrom != None:
                path.append(tmp.camefrom)
                tmp = tmp.camefrom
                tmp.isPath = True  # Draw the path
            g.draw()
            pygame.display.update()
            print(len(path))
            return

        # Mark the current node as visited / checked
        openSet.remove(current)
        closedSet.append(current)

        # Draw the current node (green) + checked nodes(red)
        current.isCurrent = True
        g.draw()
        current.isCurrent = False
        current.checked = True
        pygame.display.update()

        for node in current.neighbours:
            if not node.isWall and not node in closedSet:
                tempG = current.g + 1
                if node in openSet:
                    if tempG < node.g:
                        node.g = tempG
                else:
                    node.g = tempG
                    openSet.append(node)

                node.f = node.g
                node.camefrom = current
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_n:
                    return
    return(None)


def Astar(start=(0, 0), end=(g.x_elems - 1, g.y_elems - 1)):
    g.reset(False)
    end = g.grid[end[1]][end[0]]
    # Paths to extend
    openSet = [g.grid[start[1]][start[0]]]
    # already visited / checked / extended
    closedSet = []
    while openSet:
        lowest = 0
        for i in range(len(openSet)):
            if openSet[i].f < openSet[lowest].f:
                lowest = i

        current = openSet[lowest]

        if current == end:
            path = []  # If we ever need it
            tmp = current
            tmp.isPath = True
            path.append(tmp)
            while tmp.camefrom != None:
                path.append(tmp.camefrom)
                tmp = tmp.camefrom
                tmp.isPath = True  # Draw the path
            g.draw()
            pygame.display.update()
            print(len(path))
            return

        # Mark the current node as visited / checked
        openSet.remove(current)
        closedSet.append(current)

        # Draw the current node (green) + checked nodes(red)
        current.isCurrent = True
        g.draw()
        current.isCurrent = False
        current.checked = True
        pygame.display.update()

        for node in current.neighbours:
            if not node.isWall and not node in closedSet:
                tempG = current.g + 1
                if node in openSet:
                    if tempG < node.g:
                        node.g = tempG
                else:
                    node.g = tempG
                    openSet.append(node)

                node.h = node.distance(end)
                node.f = node.g + node.h
                node.camefrom = current
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == 113:
                    return
    return(None)


def reset():
    g.reset(True)


def Maze(start=(0, 0)):
    g.reset(True)
    fill_Walls()
    strt = g.grid[start[1]][start[0]]
    visited = [strt]
    stack = [strt]

    while stack != []:
        current = stack.pop(0)
        if len(current.WallNeighbours(visited)) != 0:
            stack.insert(0, current)
            chosen = current.WallNeighbours(visited)[randint(0,
                                                             len(current.WallNeighbours(visited))) - 1]
            y = (current.i + chosen.i) // 2
            x = (current.j + chosen.j) // 2
            g.grid[y][x].isWall = False
            visited.append(chosen)
            stack.insert(0, chosen)


def fill_Walls():
    for i in range(1, g.y_elems, 2):
        for j in range(0, g.x_elems):
            g.grid[i][j].isWall = True
    for i in range(1, g.x_elems, 2):
        for j in range(0, g.y_elems):
            g.grid[j][i].isWall = True


funcs = {pygame.K_b: BreadthFS, pygame.K_d: DepthFS, pygame.K_g: Maze, pygame.K_v: BestFS,
         pygame.K_h: HillClimb, 113: Astar, pygame.K_n: Djikstra, pygame.K_BACKSPACE: reset}

start = (0, 0)
end = (g.x_elems - 1, g.y_elems - 1)
while True:
    # Reset Start and end Nodes
    g.grid[start[1]][start[0]].isStart = True
    g.grid[start[1]][start[0]].isWall = False
    g.grid[end[1]][end[0]].isEnd = True
    g.grid[end[1]][end[0]].isWall = False

    g.draw()
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN:
            mousePos = pygame.mouse.get_pos()
            if event.key in funcs.keys():
                if not event.key in [pygame.K_BACKSPACE, pygame.K_g]:
                    funcs[event.key](start, end)
                else:
                    funcs[event.key]()
            if event.key == pygame.K_s:
                g.grid[start[1]][start[0]].isStart = False
                start = ((mousePos[0] // g.n_width), (mousePos[1] // g.n_width))
            if event.key == pygame.K_e:
                g.grid[end[1]][end[0]].isEnd = False
                end = ((mousePos[0] // g.n_width), (mousePos[1] // g.n_width))

    pygame.display.update()
