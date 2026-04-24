import pygame
import random

pygame.init()

CELL = 30
COLS = 20
ROWS = 20
W = COLS * CELL
H = ROWS * CELL

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 22)
font_big = pygame.font.SysFont("Arial", 46, bold=True)

def spawn_food(snake):
    # генерим еду пока не найдем свободную клетку
    while True:
        pos = (random.randint(1, COLS-2), random.randint(1, ROWS-2))
        if pos not in snake:
            return pos

def game():
    snake = [(10,10),(9,10),(8,10)]
    dir = (1,0)
    next_dir = dir
    food = spawn_food(snake)
    score = 0
    level = 1
    eaten = 0
    speed = 8

    while True:
        clock.tick(speed)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP and dir != (0,1):
                    next_dir = (0,-1)
                if e.key == pygame.K_DOWN and dir != (0,-1):
                    next_dir = (0,1)
                if e.key == pygame.K_LEFT and dir != (1,0):
                    next_dir = (-1,0)
                if e.key == pygame.K_RIGHT and dir != (-1,0):
                    next_dir = (1,0)

        dir = next_dir
        hx, hy = snake[0]
        new_head = (hx + dir[0], hy + dir[1])
        nx, ny = new_head

        # врезались в стену или в себя - конец
        if nx == 0 or ny == 0 or nx == COLS-1 or ny == ROWS-1 or new_head in snake:
            return True

        snake.insert(0, new_head)

        if new_head == food:
            score += 10
            eaten += 1
            food = spawn_food(snake)
            # каждые 3 еды - новый уровень, скорость растет
            if eaten % 3 == 0:
                level += 1
                speed += 2
        else:
            snake.pop()

        screen.fill((0,0,0))

        # рисуем стены
        for x in range(COLS):
            for y in range(ROWS):
                if x==0 or y==0 or x==COLS-1 or y==ROWS-1:
                    pygame.draw.rect(screen, (60,60,60), (x*CELL, y*CELL, CELL, CELL))

        # еда
        pygame.draw.rect(screen, (220,0,0), (food[0]*CELL+4, food[1]*CELL+4, CELL-8, CELL-8))

        # змейка
        for i,(sx,sy) in enumerate(snake):
            c = (0,140,0) if i==0 else (0,200,0)
            pygame.draw.rect(screen, c, (sx*CELL+1, sy*CELL+1, CELL-2, CELL-2))

        screen.blit(font.render(f"Score: {score}  Level: {level}", True, (255,255,255)), (8, 4))

        pygame.display.flip()

    return False

def game_over():
    screen.fill((0,0,0))
    screen.blit(font_big.render("GAME OVER", True, (220,0,0)), (160, 230))
    screen.blit(font.render("R - restart    Q - quit", True, (255,255,255)), (170, 310))
    pygame.display.flip()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r: return True
                if e.key == pygame.K_q: return False

play = True
while play:
    restart = game()
    if restart:
        play = game_over()
    else:
        play = False

pygame.quit()
