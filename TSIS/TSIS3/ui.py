import pygame
from persistence import load_scores, save_score, save_settings

# цвета
BG= (15, 15, 35)
WHITE= (255, 255, 255)
GRAY =(130, 130, 150)
YELLOW=(230, 200, 50)
RED = (220, 60, 60)
GREEN  = (60, 200, 80)
CYAN = (50, 220, 220)
BTN  = (40, 40, 70)
BTN_H = (70, 70, 115)


def draw_button(screen,text,x, y, w, h, font):
    rect = pygame.Rect(x, y, w, h)
    #тут подсвечиваем если мышь над кнопкой
    hovered = rect.collidepoint(pygame.mouse.get_pos())
    pygame.draw.rect(screen, BTN_H if hovered else BTN, rect, border_radius=8)
    pygame.draw.rect(screen, GRAY, rect, 2, border_radius=8)
    t = font.render(text, True, WHITE)
    screen.blit(t, t.get_rect(center=rect.center))
    return rect   #возвращаем rect чтобы потом проверить клик


def draw_text_center(screen, text, font, color, y):
    t = font.render(text, True, color)
    screen.blit(t, t.get_rect(center=(screen.get_width() // 2, y)))



def screen_name(screen, clock):
    font = pygame.font.SysFont("Arial", 26)
    big  = pygame.font.SysFont("Arial", 42, bold=True)
    name = ""

    while True:
        clock.tick(60)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return ""
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN and name.strip():
                    return name.strip()
                elif ev.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif ev.key == pygame.K_ESCAPE:
                    return ""
                elif len(name) < 14 and ev.unicode.isprintable():
                    name += ev.unicode

        screen.fill(BG)
        draw_text_center(screen, "Enter Your Name", big, YELLOW, 200)

        box = pygame.Rect(80, 280, 340, 52)
        pygame.draw.rect(screen, BTN, box, border_radius=8)
        pygame.draw.rect(screen, WHITE, box, 2, border_radius=8)
        screen.blit(font.render(name + "|", True, WHITE), (box.x + 12, box.y + 14))

        draw_text_center(screen, "Enter = start    Esc = back", font, GRAY, 370)
        pygame.display.flip()



def screen_menu(screen, clock, settings):
    font = pygame.font.SysFont("Arial", 26)
    big  = pygame.font.SysFont("Arial", 56, bold=True)

    while True:
        clock.tick(60)

        # собираем все клики
        clicked = []
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return
            if ev.type == pygame.MOUSEBUTTONDOWN:
                clicked.append(ev.pos)

        screen.fill(BG)
        draw_text_center(screen, "RACER", big, YELLOW, 130)
        draw_text_center(screen, "Arrow keys to switch lanes", font, GRAY, 185)

        btn_play  = draw_button(screen, "Play",        150, 220, 200, 52, font)
        btn_board = draw_button(screen, "Leaderboard", 150, 290, 200, 52, font)
        btn_set   = draw_button(screen, "Settings",    150, 360, 200, 52, font)
        btn_quit  = draw_button(screen, "Quit",        150, 430, 200, 52, font)

        pygame.display.flip()

        # проверяем клики
        for pos in clicked:
            if btn_quit.collidepoint(pos):
                return
            if btn_play.collidepoint(pos):
                name = screen_name(screen, clock)
                if name:
                    _do_play(screen, clock, settings, name)
            if btn_board.collidepoint(pos):
                screen_leaderboard(screen, clock)
            if btn_set.collidepoint(pos):
                settings = screen_settings(screen, clock, settings)


def _do_play(screen, clock, settings, name):
    from racer import run_game
    result = run_game(screen, clock, settings, name)
    if result is None:
        return
    score, dist, coins = result
    save_score(name, score, dist)
    action = screen_gameover(screen, clock, name, score, dist, coins)
    if action == "retry":
        result2 = run_game(screen, clock, settings, name)
        if result2:
            save_score(name, result2[0], result2[1])
            screen_gameover(screen, clock, name, result2[0], result2[1], result2[2])


#  настройки

def screen_settings(screen, clock, settings):
    font = pygame.font.SysFont("Arial", 24)
    big  = pygame.font.SysFont("Arial", 38, bold=True)

    car_options  = ["red", "blue", "green", "yellow"]
    diff_options = ["easy", "normal", "hard"]
    car_rgb = {
        "red":    (210, 50, 50),
        "blue":   (50, 110, 210),
        "green":  (50, 175, 70),
        "yellow": (215, 195, 45),
    }
    diff_col = {"easy": GREEN, "normal": YELLOW, "hard": RED}

    while True:
        clock.tick(60)

        clicked = []
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                save_settings(settings)
                return settings
            if ev.type == pygame.MOUSEBUTTONDOWN:
                clicked.append(ev.pos)

        screen.fill(BG)
        draw_text_center(screen, "Settings", big, YELLOW, 105)

        #звук
        screen.blit(font.render("Sound:", True, WHITE), (90, 190))
        sound_rect = pygame.Rect(240, 185, 100, 36)
        on = settings.get("sound", True)
        pygame.draw.rect(screen, BTN, sound_rect, border_radius=6)
        pygame.draw.rect(screen, GREEN if on else RED, sound_rect, 2, border_radius=6)
        draw_text_center(screen, "ON" if on else "OFF", font, GREEN if on else RED, 203)

        #цвет машины
        screen.blit(font.render("Car Color:", True, WHITE), (90, 248))
        color_rects = []
        for i, c in enumerate(car_options):
            r = pygame.Rect(90 + i * 82, 275, 70, 36)
            pygame.draw.rect(screen, car_rgb[c], r, border_radius=6)
            if settings.get("car_color") == c:
                pygame.draw.rect(screen, WHITE, r, 3, border_radius=6)
            color_rects.append((r, c))

        #сложность
        screen.blit(font.render("Difficulty:", True, WHITE), (90, 348))
        diff_rects = []
        for i, d in enumerate(diff_options):
            r  = pygame.Rect(60 + i * 130, 375, 115, 36)
            dc = diff_col[d]
            bw = 3 if settings.get("difficulty") == d else 1
            pygame.draw.rect(screen, BTN, r, border_radius=6)
            pygame.draw.rect(screen, dc,  r, bw, border_radius=6)
            t = font.render(d.capitalize(), True, dc)
            screen.blit(t, t.get_rect(center=r.center))
            diff_rects.append((r, d))

        btn_back = draw_button(screen, "Back", 150, 460, 200, 48, font)
        pygame.display.flip()

        # обрабатываем клики
        for pos in clicked:
            if sound_rect.collidepoint(pos):
                settings["sound"] = not settings["sound"]
                save_settings(settings)
            for r, c in color_rects:
                if r.collidepoint(pos):
                    settings["car_color"] = c
                    save_settings(settings)
            for r, d in diff_rects:
                if r.collidepoint(pos):
                    settings["difficulty"] = d
                    save_settings(settings)
            if btn_back.collidepoint(pos):
                return settings


# ── game овер

def screen_gameover(screen, clock, name, score, dist, coins):
    font = pygame.font.SysFont("Arial",26)
    big  = pygame.font.SysFont("Arial", 46, bold=True)

    while True:
        clock.tick(60)

        clicked = []
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return "quit"
            if ev.type == pygame.MOUSEBUTTONDOWN:
                clicked.append(ev.pos)

        screen.fill(BG)
        draw_text_center(screen, "GAME OVER",big,  RED,115)
        draw_text_center(screen, f"Driver: {name}", font, YELLOW, 210)
        draw_text_center(screen, f"Score: {score}",font, WHITE,  270)
        draw_text_center(screen, f"Distance: {int(dist)} m", font, CYAN,318)
        draw_text_center(screen, f"Coins: {int(coins)}", font, YELLOW, 366)

        btn_retry = draw_button(screen, "Retry",85, 505, 145, 50, font)
        btn_menu =draw_button(screen, "Main Menu",270, 505, 145, 50, font)
        pygame.display.flip()

        for pos in clicked:
            if btn_retry.collidepoint(pos): return "retry"
            if btn_menu.collidepoint(pos):  return "menu"


# таблица рекордов

def screen_leaderboard(screen, clock):
    font = pygame.font.SysFont("Arial", 22)
    big  = pygame.font.SysFont("Arial", 38, bold=True)

    data = load_scores()
    # топ-3 получают особые цвета
    rank_colors=[(230,195,45), (200,200,200), (180,120,60)]

    while True:
        clock.tick(60)

        clicked= []
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                return
            if ev.type == pygame.MOUSEBUTTONDOWN:
                clicked.append(ev.pos)

        screen.fill(BG)
        draw_text_center(screen, "Leaderboard", big, YELLOW, 50)
        pygame.draw.line(screen, GRAY, (40, 88), (460, 88), 1)

        if not data:
            draw_text_center(screen, "No scores yet!", font, GRAY, 300)
        else:
            for i, e in enumerate(data[:10]):
                col =rank_colors[i] if i < 3 else WHITE
                row = f"{i+1}.  {e['name'][:12]:<13}  {e['score']:<8}  {e['dist']} m"
                screen.blit(font.render(row, True, col), (40, 102 + i * 46))

        btn_back = draw_button(screen, "Back", 150, 600, 200, 48, font)
        pygame.display.flip()

        for pos in clicked:
            if btn_back.collidepoint(pos):
                return
