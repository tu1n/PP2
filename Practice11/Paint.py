import pygame
import math

pygame.init()

screen =pygame.display.set_mode((800, 600))
pygame.display.set_caption("Paint - Shapes")
clock =pygame.time.Clock()

WHITE =(255, 255, 255)
BLACK=(0, 0, 0)

canvas =pygame.Surface((800, 540))
canvas.fill(WHITE)

color =BLACK
mode = "square"  # square, rtriangle, etriangle, rhombus

start =None
holding = False

font = pygame.font.SysFont(None, 22)

#цвета для выбора
colors = [
    (0,0,0), (255,0,0), (0,200,0), (0,0,255),
    (255,165,0), (128,0,128), (255,255,0), (0,200,200)
]


def draw_square(surface, col, s, e):
    #квадрат-берём минимальную сторону чтобы был квадрат а не прямоугольник
    size = min(abs(e[0]-s[0]), abs(e[1]-s[1]))
    dx =size if e[0] >= s[0] else -size
    dy =  size if e[1] >= s[1] else -size
    pygame.draw.rect(surface, col, (s[0], s[1], dx, dy), 2)


def draw_right_triangle(surface, col, s, e):
    # прямоугольный треугольник прямой угол в левом нижнем углу
    p1 = s                   # верхний левый
    p2 = (s[0], e[1])        # нижний левый (прямой угол тут)
    p3 = (e[0], e[1])        # нижний правый
    pygame.draw.polygon(surface, col, [p1, p2, p3], 2)


def draw_equilateral_triangle(surface, col, s, e):
    #равносторонний треугольник
    # основание снизу, вершина сверху по центру
    base = e[0] - s[0]
    p1 = (s[0], e[1])                        # нижний левый
    p2 = (e[0], e[1])                        # нижний правый
    p3 = (s[0] + base // 2, s[1])            # верхний центр
    pygame.draw.polygon(surface, col, [p1, p2, p3], 2)


def draw_rhombus(surface, col, s, e):
    #ромб- 4 точки: верх низ лево право
    cx = (s[0] + e[0]) // 2
    cy = (s[1] + e[1]) // 2
    top    = (cx, s[1])
    bottom = (cx, e[1])
    left   = (s[0], cy)
    right  = (e[0], cy)
    pygame.draw.polygon(surface, col, [top, right, bottom, left], 2)


def draw_panel():
    pygame.draw.rect(screen, (210,210,210), (0, 540, 800, 60))

    # цвета
    for i, c in enumerate(colors):
        x = 10 + i * 45
        pygame.draw.rect(screen, c, (x, 550, 38, 38))
        if c == color:
            pygame.draw.rect(screen, WHITE, (x, 550, 38, 38), 3)

    # кнопки фигур
    tools = [("Square","square"), ("R.Tri","rtriangle"), ("E.Tri","etriangle"), ("Rhombus","rhombus")]
    for i, (name, m) in enumerate(tools):
        x = 400 + i * 95
        col = (100,200,100) if mode == m else (180,180,180)
        pygame.draw.rect(screen, col, (x, 550, 85, 38))
        t = font.render(name, True, BLACK)
        screen.blit(t, (x+8, 562))


running = True
while running:
    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if my >= 540:
                # клик по цветам
                for i, c in enumerate(colors):
                    x = 10 + i * 45
                    if x <= mx <= x+38:
                        color = c
                # клик по кнопкам фигур
                tools = ["square","rtriangle","etriangle","rhombus"]
                for i, m in enumerate(tools):
                    x = 400 + i * 95
                    if x <= mx <= x+85:
                        mode = m
            else:
                holding = True
                start = (mx, my)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # когда отпускаем - рисуем фигуру на холсте
            if holding and start:
                end = (mx, my)
                if mode == "square":         draw_square(canvas, color, start, end)
                elif mode == "rtriangle":    draw_right_triangle(canvas, color, start, end)
                elif mode == "etriangle":    draw_equilateral_triangle(canvas, color, start, end)
                elif mode == "rhombus":      draw_rhombus(canvas, color, start, end)
            holding = False
            start = None

    screen.blit(canvas, (0,0))

    # превью пока тащим мышку
    if holding and start and my < 540:
        preview = canvas.copy()
        end = (mx, my)
        if mode == "square":         draw_square(preview, color, start, end)
        elif mode=="rtriangle":    draw_right_triangle(preview, color, start, end)
        elif mode== "etriangle":    draw_equilateral_triangle(preview, color, start, end)
        elif mode == "rhombus":      draw_rhombus(preview, color, start, end)
        screen.blit(preview, (0,0))

    draw_panel()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
