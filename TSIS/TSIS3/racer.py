import pygame
import random
import time

#размеры экрана
SW = 500
SH = 700

# дорога
ROAD_X = 80
ROAD_W = 340
LANE_W = ROAD_W // 3

#центр каждой полосы
LANE1= ROAD_X+ LANE_W* 0 +LANE_W // 2
LANE2= ROAD_X + LANE_W* 1 +LANE_W // 2
LANE3 = ROAD_X + LANE_W* 2 +LANE_W // 2
LANES = [LANE1, LANE2, LANE3]

# цвета
WHITE= (255, 255, 255)
BLACK= (0, 0, 0)
GRAY= (100, 100, 100)
RED= (220, 50, 50)
GREEN= (34, 130, 34)
YELLOW = (230, 195, 45)
ORANGE= (230, 115, 30)
PURPLE = (160, 50, 200)
CYAN= (50, 215, 215)
ROAD_C = (55, 55, 55)
STRIPE =(210, 190, 40)


def run_game(screen, clock, settings, player_name):
    font= pygame.font.SysFont("Arial", 20)
    font_big = pygame.font.SysFont("Arial", 26, bold=True)

    # выбираем цвет машины из настроек
    colors = {
        "red":  (210, 50, 50),
        "blue":  (50, 110, 210),
        "green":  (50, 175, 70),
        "yellow": (215, 195, 45),
    }
    car_color =colors.get(settings.get("car_color", "red"), (210, 50, 50))

    # скорость зависит от сложности
    if settings.get("difficulty")== "easy":
        base_speed = 4
    elif settings.get("difficulty")=="hard":
        base_speed = 9
    else:
        base_speed = 6

    #пееременные игрока
    lane    = 1          # текущая полоса (0, 1, 2)
    player_x = float(LANES[1])
    player_y = SH - 120
    hp      = 3          # жизни
    coins   = 0
    dist    = 0.0       # пройдено метров
    speed   = float(base_speed)
    scroll  = 0.0     # смещение разметки на дороге

    # бонус
    active_pu  = None    # активный бонус: "nitro" / "shield" / None
    nitro_end  = 0.0
    shield_on  = False
    slow_end   = 0.0   # когда кончается замедление

    # списки объектов
    enemies= []   # вражеские машины: {"x","y","color"}
    coin_lst = []   # монеты: {"x", "y","val","col"}
    hazards= []   # препятствия: {"x", "y","type"}
    powerups=[]   # бонусы: {"x","y","type"}
    events=[]   # события дороги: {"x","y","type"}

    # таймеры спавна
    t_enemy  = time.time() + 1.5
    t_coin   = time.time() + 0.9
    t_hazard = time.time() + 2.0
    t_pu     = time.time() + 7.0
    t_event  = time.time() + 10.0

    running = True

    while running:
        clock.tick(60)
        now = time.time()

        # --- события клавиатуры ---
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return None
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_LEFT and lane > 0:
                    lane -= 1
                if ev.key == pygame.K_RIGHT and lane < 2:
                    lane += 1
                if ev.key == pygame.K_ESCAPE:
                    running = False

        #считаем текущую скорость
        if active_pu == "nitro" and now < nitro_end:
            speed = base_speed * 2.0      # нитро — в два раза быстрее
        elif now < slow_end:
            speed = max(2.0, base_speed * 0.5)   # замедление от масла
        else:
            speed = float(base_speed)

        # нитро истекло
        if active_pu == "nitro" and now > nitro_end:
            active_pu = None

        #плавное движение к нужной полосе
        target_x = float(LANES[lane])
        if abs(player_x - target_x) <= 8:
            player_x = target_x
        elif player_x < target_x:
            player_x += 8
        else:
            player_x -= 8

        #прокрутка разметки
        scroll = (scroll + speed) % 60

        #расстояние
        dist +=speed * 0.05
        if dist>= 3000:
            running = False   # финиш!

        # сложность растёт с расстоянием
        scale = max(0.35, 1.0 - dist / 5000)

        # --- спавним объекты ---
        if now > t_enemy:
            # вражеская машина в случайную полосу
            e_lane = random.randint(0, 2)
            if e_lane == lane:
                e_lane = (e_lane + 1) % 3
            clrs = [(155,155,155),(195,95,45),(95,155,195),(175,85,175)]
            enemies.append({"x": LANES[e_lane], "y": -60, "color": random.choice(clrs)})
            if settings.get("difficulty") == "easy":
                t_enemy = now + max(0.3, 2.0 * scale)
            elif settings.get("difficulty") == "hard":
                t_enemy = now + max(0.3, 0.6 * scale)
            else:
                t_enemy = now + max(0.3, 1.2 * scale)

        if now > t_coin:
            r = random.random()
            if r < 0.60:
                val, col = 1, YELLOW
            elif r < 0.85:
                val, col = 3, ORANGE
            else:
                val, col = 5, PURPLE
            coin_lst.append({"x": LANES[random.randint(0,2)], "y": -20, "val": val, "col": col})
            t_coin = now + 0.9

        if now > t_hazard:
            other_lanes = [i for i in range(3) if i != lane]
            h_lane = random.choice(other_lanes if random.random() < 0.7 else [0,1,2])
            h_type = random.choice(["oil", "oil", "barrier"])
            hazards.append({"x": LANES[h_lane], "y": -40, "type": h_type})
            if settings.get("difficulty") == "easy":
                t_hazard = now + max(0.35, 2.5 * scale)
            elif settings.get("difficulty") == "hard":
                t_hazard = now + max(0.35, 0.8 * scale)
            else:
                t_hazard = now + max(0.35, 1.5 * scale)

        if now > t_pu:
            pu_type = random.choice(["nitro", "nitro", "shield", "repair"])
            powerups.append({"x": LANES[random.randint(0,2)], "y": -30, "type": pu_type})
            t_pu = now + random.randint(5, 9)

        if now > t_event:
            ev_type = random.choice(["nitro", "nitro", "bump"])
            events.append({"x": LANES[random.randint(0,2)], "y": -30, "type": ev_type})
            t_event = now + random.randint(8, 14)

        # прямоугольник игрока для коллизий
        pr = pygame.Rect(int(player_x) - 18, player_y - 31, 36, 62)

        #двигаем врагов и проверяем столкновение
        for e in enemies[:]:
            e["y"] += speed * 0.85
            if e["y"] > SH + 70:
                enemies.remove(e)
                continue
            er = pygame.Rect(e["x"]-18, e["y"]-31, 36, 62)
            if pr.colliderect(er):
                enemies.remove(e)
                if shield_on:
                    shield_on =False
                    active_pu= None
                else:
                    hp -= 1
                    if hp <= 0:
                        running = False

        #двигаем монеты
        for c in coin_lst[:]:
            c["y"] += speed
            if c["y"] > SH + 20:
                coin_lst.remove(c)
                continue
            if pr.colliderect(pygame.Rect(c["x"]-13, c["y"]-13, 26, 26)):
                coin_lst.remove(c)
                coins += c["val"]
                base_speed = float(base_speed) + coins // 8

        #вигаем препятствия
        for h in hazards[:]:
            h["y"] += speed
            if h["y"] > SH + 40:
                hazards.remove(h)
                continue
            if pr.colliderect(pygame.Rect(h["x"]-28, h["y"]-12, 56, 24)):
                hazards.remove(h)
                if h["type"] == "oil":
                    slow_end = now + 2.5    #масло — замедляемся
                else:
                    if shield_on:
                        shield_on = False
                        active_pu = None
                    else:
                        hp -= 1
                        if hp <= 0:
                            running = False

        # --- двигаем бонусы ---
        for p in powerups[:]:
            p["y"] += speed
            if p["y"] > SH + 30:
                powerups.remove(p)
                continue
            if pr.colliderect(pygame.Rect(p["x"]-16, p["y"]-16, 32, 32)):
                powerups.remove(p)
                if p["type"] == "nitro":
                    active_pu = "nitro"
                    nitro_end = now + 4.0
                elif p["type"] == "shield":
                    active_pu = "shield"
                    shield_on = True
                elif p["type"] == "repair":
                    hp = min(3, hp + 1)    # лечимся на 1

        #   двигаем события дороги
        for r in events[:]:
            r["y"] += speed
            if r["y"] > SH + 20:
                events.remove(r)
                continue
            if pr.colliderect(pygame.Rect(r["x"]-LANE_W//2, r["y"]-10, LANE_W, 20)):
                events.remove(r)
                if r["type"] == "nitro":
                    active_pu = "nitro"
                    nitro_end = now + 3.5
                else:
                    slow_end = now + 1.5   # лежачий полицейский

        #рисуем

        # трава
        screen.fill(GREEN)

        # дорога
        pygame.draw.rect(screen, ROAD_C, (ROAD_X, 0, ROAD_W, SH))

        # прокручивающиеся полоски
        for i in range(1, 3):
            x = ROAD_X + LANE_W * i
            y = -60 + scroll
            while y < SH:
                pygame.draw.rect(screen, STRIPE, (x-2, int(y), 4, 32))
                y += 60

        # края дороги
        pygame.draw.rect(screen, WHITE, (ROAD_X,          0, 4, SH))
        pygame.draw.rect(screen, WHITE, (ROAD_X+ROAD_W-4, 0, 4, SH))

        # события на дороге
        for r in events:
            lx = r["x"] - LANE_W // 2
            if r["type"] == "nitro":
                pygame.draw.rect(screen, (200,100,0), (lx, r["y"]-9,LANE_W, 18),border_radius=4)
                t = font.render("NITRO", True, WHITE)
            else:
                pygame.draw.rect(screen, (100,70,30), (lx, r["y"]-7, LANE_W, 14), border_radius=3)
                t = font.render("BUMP", True, WHITE)
            screen.blit(t, t.get_rect(center=(r["x"], r["y"])))

        # препятствия
        for h in hazards:
            if h["type"] == "oil":
                pygame.draw.ellipse(screen, (15,10,65),  (h["x"]-28, h["y"]-12, 56, 24))
                pygame.draw.ellipse(screen, (50,35,150), (h["x"]-22, h["y"]-8,  44, 16))
            else:
                pygame.draw.rect(screen, RED,    (h["x"]-28, h["y"]-13, 56, 26), border_radius=4)
                pygame.draw.line(screen, YELLOW, (h["x"]-26, h["y"]), (h["x"]+26, h["y"]), 3)

        # монеты
        for c in coin_lst:
            pygame.draw.circle(screen, c["col"], (c["x"], c["y"]), 13)
            pygame.draw.circle(screen, WHITE,    (c["x"], c["y"]), 13, 2)
            t = font.render(str(c["val"]), True, BLACK)
            screen.blit(t, t.get_rect(center=(c["x"], c["y"])))

        # бонусы
        pu_colors  = {"nitro": ORANGE, "shield": CYAN, "repair": (60,200,80)}
        pu_letters = {"nitro": "N",    "shield": "S",  "repair": "R"}
        for p in powerups:
            col = pu_colors[p["type"]]
            r   = pygame.Rect(p["x"]-17, p["y"]-17, 34, 34)
            pygame.draw.rect(screen, col,   r, border_radius=7)
            pygame.draw.rect(screen, WHITE, r, 2, border_radius=7)
            t = font_big.render(pu_letters[p["type"]], True, WHITE)
            screen.blit(t, t.get_rect(center=(p["x"], p["y"])))

        # вражеские машины
        for e in enemies:
            draw_car(screen, e["x"], e["y"], e["color"], enemy=True)

        # щит вокруг игрока
        if shield_on:
            pygame.draw.ellipse(screen, CYAN,
                (int(player_x)-26, player_y-39, 52, 78), 3)

        # машина игрока
        draw_car(screen, int(player_x), player_y, car_color, enemy=False)

        # ======== HUD (верхняя панель) ========
        pygame.draw.rect(screen, BLACK, (0, 0, SW, 54))

        # жизни — красные кружки
        for i in range(3):
            c = RED if i < hp else GRAY
            pygame.draw.circle(screen, c, (18 + i*22, 27), 9)

        screen.blit(font.render(f"Score: {int(coins*10 + dist*0.5)}", True, WHITE),  (80, 7))
        screen.blit(font.render(f"Coins: {coins}",                    True, YELLOW), (80, 29))

        left = max(0, 3000 - dist)
        screen.blit(font.render(f"{int(dist)}m  left:{int(left)}m",   True, CYAN),  (215, 7))
        screen.blit(font.render(f"Speed: {int(speed*10)} km/h",        True, WHITE), (215, 29))

        # баннер активного бонуса
        if active_pu == "nitro" and now < nitro_end:
            t = font_big.render(f"NITRO  {nitro_end - now:.1f}s", True, ORANGE)
            screen.blit(t, t.get_rect(center=(SW//2, 67)))
        elif shield_on:
            t = font_big.render("SHIELD ON", True, CYAN)
            screen.blit(t, t.get_rect(center=(SW//2, 67)))
        elif now < slow_end:
            t = font_big.render("SLOWED", True, (170, 120, 255))
            screen.blit(t, t.get_rect(center=(SW//2, 67)))

        pygame.display.flip()

    score = int(coins * 10 + dist * 0.5)
    return score, dist, coins


def draw_car(screen, x, y, color, enemy):
    # кузов машины
    pygame.draw.rect(screen, color, (x-18, y-31, 36, 62), border_radius=6)

    # лобовое стекло: у игрока сверху, у врагов снизу
    ws_y = y + 31 - 20 if enemy else y - 31 + 4
    pygame.draw.rect(screen, (145, 215, 255), (x-13, ws_y, 26, 16), border_radius=3)

    # 4 колеса по углам
    for wx, wy in [(-18, -25), (10, -25), (-18, 13), (10, 13)]:
        pygame.draw.rect(screen, (30, 30, 30), (x+wx, y+wy, 8, 12), border_radius=2)
