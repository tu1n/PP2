import pygame
import sys
import os
from player import Player

pygame.init()
screen = pygame.display.set_mode((600, 300))
pygame.display.set_caption("Music Player")
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

player = Player()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            if event.key == pygame.K_s:
                player.stop()
            if event.key == pygame.K_n:
                player.next_track()
            if event.key == pygame.K_b:
                player.prev_track()
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    screen.fill((0, 0, 0))

    name = os.path.basename(player.songs[player.track_index]).replace(".mp3", "")
    screen.blit(font.render("Track: " + name, True, (255, 255, 255)), (50, 60))

    if player.playing:
        screen.blit(font.render("Status: Playing", True, (0, 200, 0)), (50, 110))
    else:
        screen.blit(font.render("Status: Stopped", True, (200, 0, 0)), (50, 110))

    pos = str(player.get_pos()) + "s"
    screen.blit(font.render("Position: " + pos, True, (255, 255, 0)), (50, 160))

    info = "Track " + str(player.track_index + 1) + " of " + str(len(player.songs))
    screen.blit(font.render(info, True, (150, 150, 150)), (50, 210))

    screen.blit(font.render("P=Play  S=Stop  N=Next  B=Back  Q=Quit", True, (100, 100, 100)), (50, 260))

    pygame.display.flip()
    clock.tick(60)