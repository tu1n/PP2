import pygame
import sys

from game import (
    menu_screen,
    gameover_screen,
    leaderboard_screen,
    settings_screen,
    run_game,
)

#подключить БД
try:
    from db import (
        create_tables,
        get_or_create_player,
        save_game_result,
        get_personal_best,
        get_top10
    )

    create_tables()
    DB_OK = True

except Exception as e:
    print("БД не подключилась:", e)
    DB_OK = False

    # заглушки, чтобы игра не падала
    def get_or_create_player(n): return 0
    def save_game_result(p, s, l): pass
    def get_personal_best(p): return 0
    def get_top10(): return []


pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Snake")

player_id = None
best = 0

state = "menu"

username = ""
last_score = 0
last_level = 1


while True:

    if state == "menu":
        action, username = menu_screen(screen)

        if action == "quit":
            break

        elif action == "play":
            player_id = get_or_create_player(username)
            best = get_personal_best(player_id)
            state = "game"

        elif action == "leaderboard":
            state = "leaderboard"

        elif action == "settings":
            state = "settings"

    elif state == "game":
        last_score, last_level, reason = run_game(screen, best)

        save_game_result(player_id, last_score, last_level)

        if last_score > best:
            best = last_score

        if reason == "quit":
            break
        elif reason == "menu":
            state = "menu"
        else:
            state = "gameover"

    elif state == "gameover":
        action = gameover_screen(screen, last_score, last_level, best)

        if action == "retry":
            state = "game"
        elif action == "menu":
            state = "menu"
        elif action == "quit":
            break

    elif state == "leaderboard":
        leaderboard_screen(screen, get_top10)
        state = "menu"

    elif state == "settings":
        settings_screen(screen)
        state = "menu"


pygame.quit()
sys.exit()