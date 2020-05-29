from Colors import ColorCode
from pygame import mouse, Rect, draw, Surface

class Node(object):
    def __init__(self, surfac, x, y, width, i, j, offsetx=0, offsety=0):

        self.x = x
        self.y = y
        self.width = width
        self.surface = surfac

        self.i = i
        self.j = j

        # For A-Star
        self.f = 0
        self.g = 0
        self.h = 0
        self.camefrom = None

        self.color = ColorCode.BLACK  # SET as BG color

        self.offsetx = offsetx
        self.offsety = offsety

        self.neighbours = []

        self.wall_neighbours = []  # For maze generation (I need to remake it)

        # Node states
        self.isStart = False
        self.isEnd = False
        self.isWall = False
        self.isPath = False
        self.isCurrent = False
        self.checked = False

    def draw(self):
        # What is needed? : Highlight if mouseOver, Change color to white if it's a wall

        # Set the state of the node
        if isMouseOver(self):
            # Left Mouse Button
            if mouse.get_pressed()[0] == 1:
                self.isWall = True
            # Right Mouse Button
            if mouse.get_pressed()[2] == 1:
                self.isWall = False

            self.color = ColorCode.DARK_GRAY
        elif self.isStart:
            self.color = ColorCode.YELLOW
        elif self.isEnd:
            self.color = ColorCode.ORANGE
        elif self.isWall:
            self.color = ColorCode.WHITE
        elif self.isPath:
            self.color = ColorCode.BLUE
        elif self.checked:
            self.color = ColorCode.RED
        elif self.isCurrent:
            self.color = ColorCode.GREEN
        else:
            self.color = ColorCode.BLACK

        # Render the node on the screen
        rect = Rect(self.x, self.y, self.width, self.width)
        draw.rect(self.surface, self.color, rect)

    def WallNeighbours(self, arr=[]):  # WIP (Need to remake the whole classes so this is easier)
        a = []
        for node in self.wall_neighbours:
            if not node.isWall and node not in arr:
                a.append(node)
        return(a)

    def hasNeighbours(self):  # WIP (Need to remake the whole classes so this is easier)
        a = []
        for node in self.neighbours:
            if not node.isWall:
                a.append(node)
        return(a)

    def distance(self, node):
        """Returns distance between current node and passed node"""
        x = abs(self.j - node.j)
        y = abs(self.i - node.i)
        return(x + y)


class Grid(object):
    def __init__(self, surfac, x=0, y=0, dimensions=(100, 100), node_width=10):
        # What is needed? : Create the nodes, Store the nodes, give each node its neighbours.

        self.surface = surfac
        self.x = x
        self.y = y
        self.dimensions = dimensions
        self.n_width = node_width

        self.x_elems = self.dimensions[0] // self.n_width  # Number of nodes in a row
        self.y_elems = self.dimensions[1] // self.n_width  # Number of nodes in a column

        self.grid = []
        self.grid_surf = Surface(self.dimensions)

        # Create the nodes
        for i in range(self.y_elems):
            a = []
            for j in range(self.x_elems):
                a.append(Node(self.grid_surf, j * self.n_width, i *
                              self.n_width, self.n_width, i, j, self.x, self.y))
            self.grid.append(a)
        # Give each node its neighbours
        for i in range(self.y_elems):
            for j in range(self.x_elems):
                if j > 0:  # Left neighbour
                    self.grid[i][j].neighbours.append(self.grid[i][j - 1])
                if j < self.x_elems - 1:  # Right neighbour
                    self.grid[i][j].neighbours.append(self.grid[i][j + 1])
                if i > 0:  # Top neighbour
                    self.grid[i][j].neighbours.append(self.grid[i-1][j])
                if i < self.y_elems - 1:  # Bottom neighbour
                    self.grid[i][j].neighbours.append(self.grid[i+1][j])

        # For maze generation (Kind of stupid of me, Need to remake)
        for i in range(0, self.y_elems):
            for j in range(0, self.x_elems):
                if j > 1:  # Left neighbour
                    self.grid[i][j].wall_neighbours.append(self.grid[i][j - 2])
                if j < self.x_elems - 2:  # Right neighbour
                    self.grid[i][j].wall_neighbours.append(self.grid[i][j + 2])
                if i > 0:  # Top neighbour
                    self.grid[i][j].wall_neighbours.append(self.grid[i-2][j])
                if i < self.y_elems - 2:  # Bottom neighbour
                    self.grid[i][j].wall_neighbours.append(self.grid[i+2][j])

    def draw(self):
        # Draw the grid
        self.grid_surf.fill(ColorCode.BLACK)  # Replace with background color

        # Draw the nodes
        for row in self.grid:
            for node in row:
                node.draw()

        # Render to screen
        self.surface.blit(self.grid_surf, (self.x, self.y))

    def reset(self, walls):
        for row in self.grid:
            for node in row:
                if walls:
                    node.isWall = False
                node.checked = False
                node.isCurrent = False
                node.isPath = False


def isMouseOver(node):
    if (node.x + node.offsetx < mouse.get_pos()[0] < node.x + node.offsetx + node.width) and (node.y + node.offsety < mouse.get_pos()[1] < node.y + node.width + node.offsety):
        return(True)
    else:
        return(False)
