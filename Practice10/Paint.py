import pygame
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# холст отдельно чтобы не стиралось
canvas = pygame.Surface((800, 540))
canvas.fill(WHITE)

color = BLACK
brush = 5
mode = "brush"  # brush, rect, circle, eraser

start = None
holding = False

font = pygame.font.SysFont(None, 22)

colors = [
    (0,0,0), (255,0,0), (0,200,0), (0,0,255),
    (255,165,0), (128,0,128), (0,200,200),
    (255,20,147), (139,69,19), (255,255,0)
]

def draw_panel():
    pygame.draw.rect(screen, (210,210,210), (0, 540, 800, 60))

    for i, c in enumerate(colors):
        x = 10 + i * 45
        pygame.draw.rect(screen, c, (x, 550, 38, 38))
        if c == color and mode != "eraser":
            pygame.draw.rect(screen, WHITE, (x, 550, 38, 38), 3)

    tools = [("Brush","brush"), ("Rect","rect"), ("Circle","circle"), ("Eraser","eraser")]
    for i, (name, m) in enumerate(tools):
        x = 480 + i * 75
        col = (100,200,100) if mode == m else (180,180,180)
        pygame.draw.rect(screen, col, (x, 550, 65, 38))
        t = font.render(name, True, BLACK)
        screen.blit(t, (x+8, 562))

    txt = font.render(f"size:{brush}", True, (50,50,50))
    screen.blit(txt, (10, 527))


running = True
while running:
    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEWHEEL:
            brush = max(1, min(50, brush + event.y))

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if my >= 540:
                for i, c in enumerate(colors):
                    x = 10 + i * 45
                    if x <= mx <= x+38:
                        color = c
                        mode = "brush"
                tools = ["brush","rect","circle","eraser"]
                for i, m in enumerate(tools):
                    x = 480 + i * 75
                    if x <= mx <= x+65:
                        mode = m
            else:
                holding = True
                start = (mx, my)
                if mode in ("brush","eraser"):
                    c = WHITE if mode=="eraser" else color
                    pygame.draw.circle(canvas, c, (mx,my), brush)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if holding and start and my < 540:
                if mode == "rect":
                    w = mx - start[0]
                    h = my - start[1]
                    pygame.draw.rect(canvas, color, (*start, w, h), brush)
                elif mode == "circle":
                    r = int(math.hypot(mx-start[0], my-start[1]))
                    pygame.draw.circle(canvas, color, start, r, brush)
            holding = False
            start = None

        if event.type == pygame.MOUSEMOTION and holding and my < 540:
            if mode in ("brush","eraser"):
                c = WHITE if mode=="eraser" else color
                prev = (mx - event.rel[0], my - event.rel[1])
                pygame.draw.line(canvas, c, prev, (mx,my), brush*2)
                pygame.draw.circle(canvas, c, (mx,my), brush)

    screen.blit(canvas, (0,0))

    # превью пока тащим прямоугольник/круг
    if holding and start and mode in ("rect","circle") and my < 540:
        prev = canvas.copy()
        if mode == "rect":
            pygame.draw.rect(prev, color, (*start, mx-start[0], my-start[1]), brush)
        else:
            r = int(math.hypot(mx-start[0], my-start[1]))
            if r > 0:
                pygame.draw.circle(prev, color, start, r, brush)
        screen.blit(prev, (0,0))

    draw_panel()

    if my < 540:
        pygame.draw.circle(screen, BLACK, (mx,my), brush, 1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
