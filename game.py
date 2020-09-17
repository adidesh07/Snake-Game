import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 400,400
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Snake Game')

rows, cols = 40, 40
gap = WIDTH // rows


class Cube:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel

    def move(self):
        x,y = self.pos
        x += self.vel[0]
        y += self.vel[1]
        self.pos = (x,y)


def draw_cube(colour, pos, head=False):
    pygame.draw.rect(WIN, colour, (pos[0]*gap + 1, pos[1]*gap + 1, gap - 1, gap - 1))
    if head:
        pygame.draw.circle(WIN, (0,0,0), (pos[0]*gap + 4, pos[1]*gap + 5), 1)
        pygame.draw.circle(WIN, (0,0,0), (pos[0]*gap + 7, pos[1]*gap + 5), 1)



class Snake:
    body = []
    turn_pos = {}

    def __init__(self, colour):
        self.colour = colour
        self.head = Cube((0,0), (1,0))
        self.body.append(self.head)
        self.vel = (1,0)

    def move(self, vel):
        self.turn_pos[self.head.pos] = vel

        for n in range(len(self.body)):
            pos = self.body[n].pos[:]
            if pos in self.turn_pos:
                self.body[n].vel = self.turn_pos[pos]
                if n == len(self.body)-1:
                    self.turn_pos.pop(pos)

            self.body[n].move()


    def addToBody(self):
        vel = self.body[-1].vel[:]
        self.body.append(Cube((self.body[-1].pos[0] - vel[0], self.body[-1].pos[1] - vel[1]), (vel)))

    def draw(self):
        for n  in range(len(self.body)):
            head = False
            if n == 0:
                head = True
            draw_cube((0,255,255), self.body[n].pos, head)
        time.sleep(0.2)


def drawGrid():
    x = 0
    y = 0
    for i in range(rows):
        x += gap
        y += gap
        pygame.draw.line(WIN, (32,32,32), (0, y), (WIDTH, y))
        pygame.draw.line(WIN, (32,32,32), (x, 0), (x, HEIGHT))

def make_food():
    return (random.randint(0,rows), random.randint(0,cols))

def eat_food(snake, food):
    if snake.body[0].pos == food:
        return True

def self_harm(snake):
    for n in range(1, len(snake.body)):
        if snake.body[0].pos == snake.body[n].pos:
            return True


def main():
    run = True
    snake = Snake((255,255,255))
    default_vel = (1,0)
    food_pos = make_food()

    def redraw_window():
        WIN.fill((0,0,0))
        drawGrid()
        snake.draw()
        draw_cube((0,153,0), food_pos)
        pygame.display.update()

    while run:
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    default_vel = (0,-1)
                if event.key == pygame.K_DOWN:
                    default_vel = (0,1)
                if event.key == pygame.K_LEFT:
                    default_vel = (-1,0)
                if event.key == pygame.K_RIGHT:
                    default_vel = (1,0)

        snake.move(default_vel)

        if self_harm(snake):
            run = False
        if snake.body[0].pos[0]>=rows or snake.body[0].pos[1]>=rows or snake.body[0].pos[0] < 0 or snake.body[0].pos[1] < 0:
            run = False
        if eat_food(snake, food_pos):
            snake.addToBody()
            food_pos = make_food()


if __name__ == '__main__':
    main()