import pygame
import random

pygame.init()

screen=pygame.display.set_mode((500, 600))
pygame.display.set_caption("Racer")
clock =pygame.time.Clock()

WHITE =(255,255,255)
BLACK=(0,0,0)
RED =(200,0,0)
BLUE = (0,0,200)
GRAY =(100,100,100)
YELLOW =(255,215,0)
ORANGE=(255,140,0)
CYAN = (0,220,220)
DARKGRAY =(50,50,50)

font = pygame.font.SysFont("Arial",22,bold=True)
small =pygame.font.SysFont("Arial",16)

road_offset = 0

# монеты бывают 3 видов: бронза=1,серебро=3,золото=5
COIN_TYPES = [
    {"value": 1, "color":(180,100,30),  "radius": 10,"chance": 60}, # бронза,часто
    {"value": 3, "color": (180,180,180),"radius": 12, "chance": 30},  # серебро
    {"value": 5, "color":YELLOW, "radius": 15,"chance":10},  # золото, редко
]

#ну каждые N очков враги ускоряются
SPEED_UP_EVERY = 10


def draw_road():
    screen.fill((34,139,34))
    pygame.draw.rect(screen,DARKGRAY,(55,0,390,600))
    pygame.draw.rect(screen,WHITE, (55, 0, 5, 600))
    pygame.draw.rect(screen, WHITE, (440, 0, 5, 600))
    y = -40 +(road_offset%80)
    while y < 600:
        pygame.draw.rect(screen, GRAY,(248,y,4,40))
        y += 80


def draw_car(x, y, color):
    pygame.draw.rect(screen,color,(x, y, 50,80), border_radius=6)
    pygame.draw.rect(screen,(200,230,255), (x+8, y+10, 34, 18), border_radius=3)
    for cx in [x-8, x+42]:
        for cy in [y+10, y+50]:
            pygame.draw.rect(screen,BLACK,(cx, cy, 10, 20), border_radius=3)


def pick_coin_type():
    #выбираем тип монеты по шансам (суммарно100)
    roll = random.randint(1, 100)
    total = 0
    for t in COIN_TYPES:
        total += t["chance"]
        if roll <= total:
            return t
    return COIN_TYPES[0]


def draw_coin(x,y,ctype):
    pygame.draw.circle(screen, ctype["color"], (x, y), ctype["radius"])
    pygame.draw.circle(screen, WHITE, (x-3, y-3), 3)  # блик
    #подписываем ценность монеты
    txt = small.render(str(ctype["value"]), True,BLACK)
    screen.blit(txt, (x - txt.get_width()//2, y - txt.get_height()//2))


def game():
    global road_offset
    px =225
    py = 500

    enemies = []
    coins = []    # каждая монета: [x, y, тип]
    score= 0             # счёт в монетах
    enemy_timer =0
    coin_timer = 0
    base_speed =5   # базовая скорость
    enemy_speed = base_speed

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        keys =pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and px > 65:
            px -= 5
        if keys[pygame.K_RIGHT] and px < 385:
            px += 5

        road_offset +=enemy_speed

        draw_road()
        draw_car(px,py, BLUE)

        # ускоряем врагов каждые SPEED_UP_EVERY очков
        enemy_speed=base_speed + score // SPEED_UP_EVERY

        #спавн врагов
        enemy_timer += 1
        if enemy_timer >=90:
            enemies.append([random.randint(65, 385),-80])
            enemy_timer =0

        # спавн монет
        coin_timer += 1
        if coin_timer >=110:
            cx = random.randint(75, 415)
            coins.append([cx, -20, pick_coin_type()])
            coin_timer = random.randint(0, 50)

        # враги
        for e in enemies[:]:
            e[1] +=enemy_speed
            draw_car(e[0], e[1], RED)
            if (px < e[0]+50 and px+50 >e[0] and py < e[1]+80 and py+80 >e[1]):
                return "gameover", score
            if e[1] > 600:
                enemies.remove(e)

        # монеты
        for c in coins[:]:
            c[1] += enemy_speed
            draw_coin(c[0], c[1], c[2])
            if abs(px+25 - c[0]) < 35 and abs(py+40 - c[1]) < 45:
                score += c[2]["value"]   # добавляем вес монеты
                coins.remove(c)
            elif c[1] > 630:
                coins.remove(c)

        # hud
        screen.blit(font.render(f"Coins: {score}", True, YELLOW), (10, 10))
        screen.blit(font.render(f"Speed: {enemy_speed}", True, CYAN), (200, 10))
        #подсказка когда следующий уровень скорости
        next_up = SPEED_UP_EVERY - (score % SPEED_UP_EVERY)
        screen.blit(small.render(f"next speed up in {next_up}", True, GRAY), (10, 38))

        pygame.display.flip()


while True:
    result =game()
    if result == "quit":
        break

    _, sc = result
    screen.fill(BLACK)
    screen.blit(font.render("GAME OVER", True, RED),(170, 200))
    screen.blit(font.render(f"Coins: {sc}", True, YELLOW), (195,255))
    screen.blit(font.render("R - restart   Q - quit", True, GRAY), (90, 320))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting =False
                result = "quit"
            if event.type == pygame.KEYDOWN:
                if event.key== pygame.K_r:
                    waiting = False
                if event.key == pygame.K_q:
                    waiting =False
                    result = "quit"
        if result =="quit":
            break

    if result== "quit":
        break
    road_offset = 0

pygame.quit()
