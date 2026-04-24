import pygame
import random

pygame.init()

screen = pygame.display.set_mode((500, 600))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()

# цвета
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (200,0,0)
BLUE = (0,0,200)
GRAY = (100,100,100)
YELLOW = (255,215,0)
DARKGRAY = (50,50,50)

font = pygame.font.SysFont("Arial", 26, bold=True)

road_offset = 0


def draw_road():
    screen.fill((34,139,34))
    pygame.draw.rect(screen, DARKGRAY, (55, 0, 390, 600))  # сама дорога
    pygame.draw.rect(screen, WHITE, (55, 0, 5, 600))        # левая линия
    pygame.draw.rect(screen, WHITE, (440, 0, 5, 600))       # правая линия

    # пунктир посередине, двигается вниз
    y = -40 + (road_offset % 80)
    while y < 600:
        pygame.draw.rect(screen, GRAY, (248, y, 4, 40))
        y += 80


def draw_car(x, y, color):
    pygame.draw.rect(screen, color, (x, y, 50, 80), border_radius=6)
    pygame.draw.rect(screen, (200,230,255), (x+8, y+10, 34, 18), border_radius=3)
    # колеса
    for cx in [x-8, x+42]:
        for cy in [y+10, y+50]:
            pygame.draw.rect(screen, BLACK, (cx, cy, 10, 20), border_radius=3)


def draw_coin(x, y):
    pygame.draw.circle(screen, YELLOW, (x, y), 13)
    pygame.draw.circle(screen, WHITE, (x-4, y-4), 4)  # блик


# --- главный цикл ---
def game():
    global road_offset

    px = 225  # позиция игрока x
    py = 500

    enemies = []   # список врагов [x, y]
    coins = []     # список монет [x, y]
    score = 0
    coin_count = 0
    enemy_timer = 0
    coin_timer = 0
    speed = 4

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and px > 65:
            px -= 5
        if keys[pygame.K_RIGHT] and px < 385:
            px += 5

        # скорость растет со временем
        score += 1
        speed = 4 + score // 500
        road_offset += speed

        draw_road()
        draw_car(px, py, BLUE)

        # спавн врага
        enemy_timer += 1
        if enemy_timer >= 90:
            ex = random.randint(65, 385)
            enemies.append([ex, -80])
            enemy_timer = 0

        # спавн монеты
        coin_timer += 1
        if coin_timer >= 130:
            cx = random.randint(75, 420)
            coins.append([cx, -20])
            coin_timer = random.randint(0, 40)

        # двигаем и рисуем врагов
        for e in enemies[:]:
            e[1] += speed
            draw_car(e[0], e[1], RED)
            # столкновение
            if (px < e[0]+50 and px+50 > e[0] and
                    py < e[1]+80 and py+80 > e[1]):
                return "gameover", score//10, coin_count
            if e[1] > 600:
                enemies.remove(e)

        # двигаем и рисуем монеты
        for c in coins[:]:
            c[1] += speed
            draw_coin(c[0], c[1])
            # подбор монеты
            if (abs(px+25 - c[0]) < 35 and abs(py+40 - c[1]) < 45):
                coin_count += 1
                coins.remove(c)
            elif c[1] > 620:
                coins.remove(c)

        # счёт
        screen.blit(font.render(f"Score: {score//10}", True, WHITE), (10,10))
        # монеты в правом углу
        screen.blit(font.render(f"Coins: {coin_count}", True, YELLOW), (360,10))

        pygame.display.flip()


while True:
    result = game()
    if result == "quit":
        break

    # game over экран
    _, sc, cn = result
    screen.fill(BLACK)
    screen.blit(font.render("GAME OVER", True, RED), (160, 200))
    screen.blit(font.render(f"Score: {sc}", True, WHITE), (185, 260))
    screen.blit(font.render(f"Coins: {cn}", True, YELLOW), (185, 300))
    screen.blit(font.render("R - restart   Q - quit", True, GRAY), (80, 370))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                result = "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                if event.key == pygame.K_q:
                    waiting = False
                    result = "quit"
        if result == "quit":
            break

    if result == "quit":
        break
    road_offset = 0

pygame.quit()
