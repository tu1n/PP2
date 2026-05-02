import pygame
import random
import json

# размер окна и клетки
WIDTH = 800
HEIGHT = 600
CELL = 20

# цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED  = (220, 0, 0)
GRAY  = (80, 80, 80)
YELLOW = (255, 220, 0)
ORANGE  = (255, 140, 0)
CYAN  = (0, 220, 220)
PURPLE = (160, 0, 200)
DKRED= (120, 0, 0)   # яд
DKGREEN = (0, 130, 0)

# сколько еды надо съесть для перехода на следующий уровень
FOOD_PER_LEVEL = 5


# грузим настройки
def load_settings():
    try:
        with open("settings.json") as f:
            return json.load(f)
    except:
        return {"snake_color": [0, 200, 0], "grid_overlay": True, "sound": False}


# сохраняем настройки
def save_settings(s):
    with open("settings.json", "w") as f:
        json.dump(s, f, indent=4)


# вывод текста на экран
def write(surface, text, size, x, y, color=WHITE, center=False):
    font = pygame.font.SysFont("Arial", size)
    img = font.render(text, True, color)
    r = img.get_rect()
    if center:
        r.center = (x, y)
    else:
        r.topleft = (x, y)
    surface.blit(img, r)


# кнопка, чтобы потом можно было проверить клик
def button(surface, text, x, y, w, h, color=GRAY):
    r = pygame.Rect(x, y, w, h)
    pygame.draw.rect(surface, color, r, border_radius=8)
    pygame.draw.rect(surface, WHITE, r, 2, border_radius=8)
    write(surface, text, 22, x + w // 2, y + h // 2, center=True)
    return r


# ищем свободную клетку
def free_cell(occupied):
    while True:
        x = random.randint(1, WIDTH // CELL - 2)
        y = random.randint(1, HEIGHT // CELL - 2)
        if (x, y) not in occupied:
            return (x, y)


def menu_screen(screen):
    clock = pygame.time.Clock()
    name = ""

    while True:
        screen.fill((30, 30, 30))
        write(screen, "SNAKE GAME", 52, WIDTH // 2, 70, GREEN, center=True)
        write(screen, "Введи имя:", 26, WIDTH // 2, 160, WHITE, center=True)

        # поле для имени
        pygame.draw.rect(screen, GRAY, (WIDTH // 2 - 140, 190, 280, 40), border_radius=6)
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 140, 190, 280, 40), 2, border_radius=6)
        write(screen, name + "|", 24, WIDTH // 2, 208, center=True)

        # кнопки
        btn_play = button(screen, "Play", WIDTH // 2 - 90, 260, 180, 44, DKGREEN)
        btn_lb   = button(screen, "Leaderboard", WIDTH // 2 - 90, 318, 180, 44)
        btn_set  = button(screen, "Settings", WIDTH // 2 - 90, 376, 180, 44)
        btn_quit = button(screen, "Quit", WIDTH // 2 - 90, 434, 180, 44, (130, 0, 0))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit", ""

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif e.key == pygame.K_RETURN and name.strip():
                    return "play", name.strip()
                elif e.unicode.isprintable() and len(name) < 18:
                    name += e.unicode

            if e.type == pygame.MOUSEBUTTONDOWN:
                p = e.pos
                if btn_play.collidepoint(p) and name.strip():
                    return "play", name.strip()
                if btn_lb.collidepoint(p):
                    return "leaderboard", name
                if btn_set.collidepoint(p):
                    return "settings", name
                if btn_quit.collidepoint(p):
                    return "quit", ""

        clock.tick(60)


def gameover_screen(screen, score, level, best):
    clock = pygame.time.Clock()

    while True:
        screen.fill((30, 30, 30))
        write(screen, "GAME OVER", 54, WIDTH // 2, 100, RED, center=True)
        write(screen, f"Счёт: {score}", 28, WIDTH // 2, 200, WHITE, center=True)
        write(screen, f"Уровень: {level}", 24, WIDTH // 2, 245, YELLOW, center=True)
        write(screen, f"Твой рекорд: {best}", 22, WIDTH // 2, 285, GRAY, center=True)

        btn_again = button(screen, "Играть снова", WIDTH // 2 - 100, 350, 200, 46, DKGREEN)
        btn_menu  = button(screen, "Главное меню", WIDTH // 2 - 100, 412, 200, 46)

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit"
            if e.type == pygame.MOUSEBUTTONDOWN:
                if btn_again.collidepoint(e.pos): return "retry"
                if btn_menu.collidepoint(e.pos):  return "menu"
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return "menu"

        clock.tick(60)


def leaderboard_screen(screen, get_top10):
    clock = pygame.time.Clock()
    rows = get_top10()  # берём данные из базы

    while True:
        screen.fill((30, 30, 30))
        write(screen, "TOP 10", 46, WIDTH // 2, 30, YELLOW, center=True)
        write(screen, "#    Имя              Счёт     Уровень   Дата", 18, 50, 90, GRAY)
        pygame.draw.line(screen, GRAY, (40, 115), (WIDTH - 40, 115), 1)

        for i, row in enumerate(rows):
            username, score, level, date = row
            d = date.strftime("%d.%m.%y") if date else "-"
            line = f"{i+1:<5}{username:<18}{score:<10}{level:<10}{d}"
            color = YELLOW if i == 0 else WHITE
            write(screen, line, 19, 50, 125 + i * 30, color)

        btn_back = button(screen, "Назад", WIDTH // 2 - 70, 545, 140, 40)
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT: return
            if e.type == pygame.MOUSEBUTTONDOWN and btn_back.collidepoint(e.pos): return
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE: return

        clock.tick(60)


def settings_screen(screen):
    clock = pygame.time.Clock()
    s = load_settings()

    colors = [
        ("Зелёный", [0, 200, 0]),
        ("Синий", [50, 100, 255]),
        ("Оранжевый", [255, 140, 0]),
        ("Белый", [230, 230, 230]),
    ]

    # ищем текущий цвет змейки
    ci = 0
    for i, (n, c) in enumerate(colors):
        if c == s["snake_color"]:
            ci = i

    while True:
        screen.fill((30, 30, 30))
        write(screen, "Настройки", 44, WIDTH // 2, 40, WHITE, center=True)

        # цвет змейки
        write(screen, "Цвет змейки:", 26, 80, 140)
        cname, cval = colors[ci]
        btn_prev = button(screen, "<", 310, 138, 36, 30)
        pygame.draw.rect(screen, tuple(cval), (355, 138, 50, 30), border_radius=5)
        write(screen, cname, 20, 415, 148, WHITE)
        btn_next = button(screen, ">", 560, 138, 36, 30)

        # сетка
        write(screen, "Сетка:", 26, 80, 210)
        gc = DKGREEN if s["grid_overlay"] else (130, 0, 0)
        btn_grid = button(screen, "ВКЛ" if s["grid_overlay"] else "ВЫКЛ", 310, 208, 80, 30, gc)

        # звук
        write(screen, "Звук:", 26, 80, 270)
        sc = DKGREEN if s["sound"] else (130, 0, 0)
        btn_sound = button(screen, "ВКЛ" if s["sound"] else "ВЫКЛ", 310, 268, 80, 30, sc)

        btn_save = button(screen, "Сохранить", WIDTH // 2 - 90, 370, 180, 46, DKGREEN)
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT: return
            if e.type == pygame.MOUSEBUTTONDOWN:
                p = e.pos
                if btn_prev.collidepoint(p):
                    ci = (ci - 1) % len(colors)
                    s["snake_color"] = colors[ci][1]
                if btn_next.collidepoint(p):
                    ci = (ci + 1) % len(colors)
                    s["snake_color"] = colors[ci][1]
                if btn_grid.collidepoint(p):
                    s["grid_overlay"] = not s["grid_overlay"]
                if btn_sound.collidepoint(p):
                    s["sound"] = not s["sound"]
                if btn_save.collidepoint(p):
                    save_settings(s)
                    return
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                save_settings(s)
                return

        clock.tick(60)


def run_game(screen, best):
    clock = pygame.time.Clock()
    settings = load_settings()

    # змейка хранится списком клеток, голова — первая
    snake = [(20, 15), (19, 15), (18, 15)]
    direction = (1, 0)   # стартуем вправо
    next_dir  = (1, 0)

    score = 0
    level = 1
    eaten = 0   # сколько еды съели на этом уровне

    obstacles = []   # стены с уровня 3
    food = None      # текущая еда
    powerup = None   # текущий бонус

    # время, когда закончится эффект
    speed_until  = 0
    slow_until   = 0
    shield_on    = False

    speed = 8         # ходов в секунду
    timer = 0.0       # накопленное время для шага

    food_born = 0     # когда появилась еда
    pu_born   = 0     # когда появился бонус

    def all_occupied():
        cells = list(snake) + obstacles
        if food:    cells.append(food["pos"])
        if powerup: cells.append(powerup["pos"])
        return cells

    def new_food():
        # случайно выбираем тип еды
        roll = random.random()
        if roll < 0.15:
            kind, color, pts = "poison", DKRED, 0
        elif roll < 0.35:
            kind, color, pts = "bonus", YELLOW, 25
        else:
            kind, color, pts = "normal", RED, 10
        return {"pos": free_cell(all_occupied()), "kind": kind, "color": color, "pts": pts}

    def new_powerup():
        kind  = random.choice(["speed", "slow", "shield"])
        color = {"speed": ORANGE, "slow": CYAN, "shield": PURPLE}[kind]
        return {"pos": free_cell(all_occupied()), "kind": kind, "color": color}

    def place_obstacles():
        # препятствия появляются с третьего уровня
        if level < 3:
            return []
        count = (level - 2) * 3   # чем выше уровень, тем больше блоков
        count = min(count, 20)
        obs = []
        for _ in range(count):
            obs.append(free_cell(list(snake) + obs))
        return obs

    # первая еда
    food = new_food()
    food_born = pygame.time.get_ticks()

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        now = pygame.time.get_ticks()

        #  события 
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return score, level, "quit"

            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_UP, pygame.K_w)    and direction != (0, 1):
                    next_dir = (0, -1)
                if e.key in (pygame.K_DOWN, pygame.K_s)  and direction != (0, -1):
                    next_dir = (0, 1)
                if e.key in (pygame.K_LEFT, pygame.K_a)  and direction != (1, 0):
                    next_dir = (-1, 0)
                if e.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-1, 0):
                    next_dir = (1, 0)
                if e.key == pygame.K_ESCAPE:
                    return score, level, "menu"

        #  таймеры еды и бонусов 
        # если еда лежит слишком долго — меняем её
        if now - food_born > 8000:
            food = new_food()
            food_born = now

        # если бонус висит 8 секунд — убираем
        if powerup and now - pu_born > 8000:
            powerup = None

        # иногда спавним бонус
        if not powerup and random.random() < 0.002:
            powerup = new_powerup()
            pu_born = now

        # скорость с учётом эффектов
        cur_speed = speed
        if now < speed_until: cur_speed = speed + 4
        if now < slow_until:  cur_speed = max(2, speed - 4)

        #  движение змейки 
        timer += dt
        if timer >= 1.0 / cur_speed:
            timer -= 1.0 / cur_speed
            direction = next_dir

            hx, hy = snake[0]
            dx, dy = direction
            new_head = (hx + dx, hy + dy)

            # удар об стену
            if new_head[0] <= 0 or new_head[0] >= WIDTH // CELL - 1 or \
               new_head[1] <= 0 or new_head[1] >= HEIGHT // CELL - 1:
                if shield_on:
                    shield_on = False
                else:
                    return score, level, "dead"

            # удар о себя
            elif new_head in snake[1:]:
                if shield_on:
                    shield_on = False
                else:
                    return score, level, "dead"

            # удар о препятствие
            elif new_head in obstacles:
                if shield_on:
                    shield_on = False
                else:
                    return score, level, "dead"

            else:
                # добавляем голову
                snake.insert(0, new_head)

                # проверяем еду
                if new_head == food["pos"]:
                    if food["kind"] == "poison":
                        # яд — режем змейку
                        snake.pop()
                        snake.pop() if len(snake) > 1 else None
                        if len(snake) <= 1:
                            return score, level, "dead"
                    else:
                        # обычная или бонусная еда
                        score += food["pts"]
                        eaten += 1
                        # переход на следующий уровень
                        if eaten % FOOD_PER_LEVEL == 0:
                            level += 1
                            speed = 8 + (level - 1)   # немного ускоряемся
                            obstacles = place_obstacles()

                    # в любом случае спавним новую еду
                    food = new_food()
                    food_born = now

                # проверяем бонус
                elif powerup and new_head == powerup["pos"]:
                    k = powerup["kind"]
                    if k == "speed":  speed_until = now + 5000
                    if k == "slow":   slow_until  = now + 5000
                    if k == "shield": shield_on   = True
                    powerup = None

                else:
                    # ничего не съели — убираем хвост
                    snake.pop()

        # ── отрисовка 
        screen.fill(BLACK)

        # сетка
        if settings.get("grid_overlay"):
            for x in range(0, WIDTH, CELL):
                pygame.draw.line(screen, (25, 25, 25), (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, CELL):
                pygame.draw.line(screen, (25, 25, 25), (0, y), (WIDTH, y))

        # граница
        pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, HEIGHT), CELL)

        # препятствия
        for ox, oy in obstacles:
            pygame.draw.rect(screen, (160, 160, 160),
                             (ox * CELL, oy * CELL, CELL, CELL))

        # еда
        fx, fy = food["pos"]
        pygame.draw.ellipse(screen, food["color"],
                            (fx * CELL + 3, fy * CELL + 3, CELL - 6, CELL - 6))

        # бонус
        if powerup:
            px, py = powerup["pos"]
            pygame.draw.rect(screen, powerup["color"],
                             (px * CELL + 2, py * CELL + 2, CELL - 4, CELL - 4), border_radius=4)
            label = {"speed": "S", "slow": "W", "shield": "X"}[powerup["kind"]]
            write(screen, label, 13, px * CELL + CELL // 2, py * CELL + CELL // 2, BLACK, center=True)

        # змейка
        sc = tuple(settings.get("snake_color", [0, 200, 0]))
        for i, (sx, sy) in enumerate(snake):
            col = DKGREEN if i == 0 else sc
            pygame.draw.rect(screen, col,
                             (sx * CELL + 1, sy * CELL + 1, CELL - 2, CELL - 2), border_radius=3)

        # если щит активен — подсвечиваем голову
        if shield_on:
            hx, hy = snake[0]
            pygame.draw.rect(screen, PURPLE,
                             (hx * CELL, hy * CELL, CELL, CELL), 2, border_radius=3)

        # счёт сверху
        write(screen, f"Счёт: {score}", 22, 10, 5)
        write(screen, f"Уровень: {level}", 22, 180, 5)
        write(screen, f"Рекорд: {best}", 22, 360, 5)

        # эффекты
        fx_text = []
        if now < speed_until: fx_text.append(f"БЫСТРО {(speed_until - now) // 1000 + 1}с")
        if now < slow_until:  fx_text.append(f"МЕДЛЕННО {(slow_until - now) // 1000 + 1}с")
        if shield_on:         fx_text.append("ЩИТ")
        if fx_text:
            write(screen, "  ".join(fx_text), 18, WIDTH - 10, 5, CYAN, center=False)

        pygame.display.flip()

    return score, level, "dead"