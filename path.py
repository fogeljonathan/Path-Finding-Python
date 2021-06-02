import pygame
import math
from queue import PriorityQueue

size=500
window=pygame.display.set_mode((size,size))
pygame.display.set_caption("Path Finding Game")
pygame.display.init()
RED=(255,0,0)
ORA=(255,128,0)
YEL=(255,251,0)
LIM=(169,255,0)
GREEN=(0,255,21)
TUR=(0,255,182)
BLU=(5, 0, 255)
PUR=(141,0,255)
BLA=(0,0,0)
WHI=(255,255,255)
GRE2=(100, 100, 100)
GRE=(200, 200, 200)


open=ORA
closed=YEL
barrier= GRE2
start= GREEN
end=RED
path=PUR

class Spot:
    def __init__(self,row,col,width,total_rows):
        self.row=row
        self.col=col
        self.x=row*width
        self.y=col*width
        self.color=WHI
        self.width=width
        self.total_rows=total_rows

    def get_pos(self):
        return self.row,self.col

    def is_closed(self):
        return self.color==closed

    def is_open(self):
        return self.color==open

    def is_barrier(self):
        return self.color==barrier

    def is_start(self):
        return self.color==start

    def is_end(self):
        return self.color==end

    def reset(self):
        self.color=WHI

    def make_start(self):
        self.color=start

    def make_end(self):
        self.color=end

    def make_closed(self):
        self.color=closed

    def make_open(self):
        self.color=open

    def make_barrier(self):
        self.color=barrier


    def make_path(self):
        self.color=path

    def draw(self, window):
        pygame.draw.rect(window,self.color,(self.x,self.y,self.width,self.width))

    def update_neighbors(self,grid):
        self.neighbors=[]
        if self.row < self.total_rows -1 and not grid[self.row+1][self.col].is_barrier():
            self.neighbors.append(grid[self.row+1][self.col]) #down

        if self.row > 0 and not grid[self.row-1][self.col].is_barrier():
            self.neighbors.append(grid[self.row-1][self.col]) #up

        if self.col < self.total_rows-1 and not grid[self.row][self.col+1].is_barrier():
            self.neighbors.append(grid[self.row][self.col+1]) #right

        if self.col > 0 and not grid[self.row][self.col-1].is_barrier():
            self.neighbors.append(grid[self.row][self.col-1]) #left

    def __lt__(self, other):
        return False

def h(p1,p2):
    x1,y1=p1
    x2,y2=p2
    return int(math.sqrt( (abs(x1-x2))**2+(abs(y1-y2))**2 ))

def reconstruct_path(came_from,current,draw):
    while current in came_from:
        current=came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    draw()
    count=0
    open_set=PriorityQueue()
    open_set.put((0,count,start))
    came_from={}
    g_score={spot: float("inf") for row in grid for spot in row}
    g_score[start]=0
    f_score={spot: float("inf") for row in grid for spot in row}
    f_score[start]=h(start.get_pos(),end.get_pos())

    open_set_hash={start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()

        current=open_set.get()[2]
        open_set_hash.remove(current)

        if current==end:
            reconstruct_path(came_from,end,draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score=g_score[current]+1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor]=current
                g_score[neighbor]=temp_g_score
                f_score[neighbor]=temp_g_score+h(neighbor.get_pos(),end.get_pos())
                if neighbor not in open_set_hash:
                    count+=1
                    open_set.put((f_score[neighbor],count,neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()
        if current!=start:
            current.make_closed()
    return False

def make_grid(rows,width):
    grid=[]
    gap=width//rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot=Spot(i,j,gap,rows)
            grid[i].append(spot)
    return grid

def draw_grid(window,rows,width):
    gap= width//rows
    for i in range(rows):
        pygame.draw.line(window,GRE,(0,i*gap),(width,i*gap))
        for j in range(rows):
            pygame.draw.line(window,GRE,(i*gap,0),(i*gap,width))

def draw(window,grid,rows,width):
    window.fill(WHI)
    for row in grid:
        for spot in row:
            spot.draw(window)
    draw_grid(window,rows,width)
    pygame.display.update()

def get_clicked_pos(pos,rows,width):
    gap=width//rows
    y,x=pos
    row=y//gap
    col=x//gap
    return row,col

def main(window,size):
    rows=50
    grid=make_grid(rows,size)

    start=None
    end=None

    run=True
    started=False

    while run:
        draw(window,grid,rows,size)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                pos=pygame.mouse.get_pos()
                row,col=get_clicked_pos(pos,rows,size)
                spot=grid[row][col]

                if not start and spot!=end:
                    start=spot
                    start.make_start()

                elif not end and spot!=start:
                    end=spot
                    end.make_end()

                elif spot!=end and spot!=start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos=pygame.mouse.get_pos()
                row,col=get_clicked_pos(pos,rows,size)
                spot=grid[row][col]
                spot.reset()
                if spot==start:
                    start=None
                elif spot==end:
                    end=None

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    algorithm(lambda: draw(window, grid, rows, size), grid, start, end)

                if event.key==pygame.K_a:
                    start=None
                    end=None
                    grid=make_grid(rows,size)

    pygame.quit()

main(window,size)
