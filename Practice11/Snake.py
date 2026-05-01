import pygame
import random
import time

pygame.init()

CELL =30
COLS =20
ROWS= 20
W = COLS *CELL
H = ROWS * CELL

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 22)
font_small = pygame.font.SysFont("Arial", 13, bold=True)
font_big = pygame.font.SysFont("Arial", 46, bold=True)

# (цвет, очки, сколько секунд живет)
FOOD_TYPES = [
    ((255,255,255) ,5,8),
    ((255, 165, 0), 15, 5),
    ((255, 0, 200), 30, 3),
]

def make_food(snake, existing_foods):
    taken = set(snake) | {f["pos"] for f in existing_foods}
    while True:
        pos = (random.randint(1, COLS-2), random.randint(1, ROWS-2))
        if pos not in taken:
            break
    t = random.choice(FOOD_TYPES)
    return {"pos": pos, "color": t[0], "points": t[1], "lifetime": t[2], "born": time.time()}

def game():
    snake = [(10,10),(9,10),(8,10)]
    dir = (1,0)
    next_dir =dir
    score =0
    level =1
    eaten = 0
    speed = 8
    foods = [make_food(snake, [])]
    spawn_timer = time.time()

    while True:
        clock.tick(speed)
        now = time.time()

        for e in pygame.event.get():
            if e.type == pygame.QUIT: return False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP    and dir != (0,1):  next_dir = (0,-1)
                if e.key == pygame.K_DOWN  and dir != (0,-1): next_dir = (0,1)
                if e.key == pygame.K_LEFT  and dir != (1,0):  next_dir = (-1,0)
                if e.key == pygame.K_RIGHT and dir != (-1,0): next_dir = (1,0)

        dir = next_dir
        hx, hy = snake[0]
        new_head = (hx+dir[0], hy+dir[1])
        nx, ny = new_head

        if nx==0 or ny==0 or nx==COLS-1 or ny==ROWS-1 or new_head in snake:
            return True

        snake.insert(0, new_head)

        ate = None
        for f in foods:
            if new_head == f["pos"]:
                ate = f
                break

        if ate:
            score +=ate["points"]
            eaten +=1
            foods.remove(ate)
            if eaten % 3 == 0:
                level +=1
                speed += 2
        else:
            snake.pop()

        foods=[f for f in foods if now - f["born"] < f["lifetime"]]

        if now - spawn_timer > 4 and len(foods) < 4:
            foods.append(make_food(snake, foods))
            spawn_timer = now

        if len(foods) == 0:
            foods.append(make_food(snake, foods))
            spawn_timer = now

        screen.fill((0,0,0))

        #стены
        for x in range(COLS):
            for y in range(ROWS):
                if x==0 or y==0 or x==COLS-1 or y==ROWS-1:
                    pygame.draw.rect(screen, (60,60,60), (x*CELL, y*CELL, CELL, CELL))

        # рисуем едуу
        for f in foods:
            fx, fy =f["pos"]
            left = int(f["lifetime"]-(now - f["born"])) + 1  # сколько секунд осталось

            pygame.draw.rect(screen, f["color"], (fx*CELL+2, fy*CELL+2, CELL-4, CELL-4))

            #цифра таймера внутри бл
            t_surf = font_small.render(str(left), True, (0,0,0))
            t_rect = t_surf.get_rect(center=(fx*CELL + CELL//2, fy*CELL + CELL//2))
            screen.blit(t_surf, t_rect)

        #змейка
        for i,(sx,sy) in enumerate(snake):
            c = (0,140,0) if i==0 else (0,200,0)
            pygame.draw.rect(screen, c, (sx*CELL+1, sy*CELL+1, CELL-2, CELL-2))

        screen.blit(font.render(f"Score: {score}  Level: {level}", True, (255,255,255)), (8,4))
        pygame.display.flip()

    return False

def game_over():
    screen.fill((0,0,0))
    screen.blit(font_big.render("GAME OVER", True, (220,0,0)), (160,230))
    screen.blit(font.render("R - restart    Q - quit", True, (255,255,255)), (170,310))
    pygame.display.flip()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r: return True
                if e.key == pygame.K_q: return False

play=True
while play:
    restart =game()
    if restart:
        play =game_over()
    else:
        play =False

pygame.quit()
