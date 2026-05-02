import pygame
from persistence import load_settings
from ui import screen_menu


def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 700))
    pygame.display.set_caption("Racer — TSIS 3")
    clock = pygame.time.Clock()

    settings= load_settings()
    screen_menu(screen, clock, settings)

    pygame.quit()


if __name__ == "__main__":
    main()
