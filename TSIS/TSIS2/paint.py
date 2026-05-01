import pygame
import sys
from datetime import datetime
from tools import flood_fill

pygame.init()

#размер окна
WIDTH =900
HEIGHT =600
PANEL = 120  # левая панель

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()

# белый холст
canvas = pygame.Surface((WIDTH - PANEL, HEIGHT))
canvas.fill((255, 255, 255))

font = pygame.font.SysFont("arial", 13)

#текущие настройки
tool = "pencil"
color = (0, 0, 0)
size = 3

drawing = False
start = (0, 0)
prev = (0, 0)

#для текста
typing = False
text = ""
text_pos = (0, 0)

# цвета  палитры
colors = [
    (0,0,0),(255,255,255),(255,0,0), (0,200,0),
    (0,0,255), (255,255,0), (255,165,0),(200,0,200),
]

# список инструментов
tools=["pencil","line","rect","circle","square","triangle","rhombus","fill","eraser","text"]

save_msg = ""
save_timer= 0

while True:
    clock.tick(60)
    mx, my =pygame.mouse.get_pos()
    cx = mx - PANEL  # позиция на холсте
    cy = my

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            # сохранение
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                name = "canvas_" + datetime.now().strftime("%H%M%S") + ".png"
                pygame.image.save(canvas, name)
                save_msg = "saved: " + name
                save_timer = 120

            elif event.key == pygame.K_1:
                size = 2
            elif event.key ==pygame.K_2:
                size = 5
            elif event.key ==pygame.K_3:
                size = 10

            # ввод текста
            elif typing:
                if event.key == pygame.K_RETURN:
                    t = font.render(text, True, color)
                    canvas.blit(t, text_pos)
                    typing = False
                    text = ""
                elif event.key == pygame.K_ESCAPE:
                    typing = False
                    text = ""
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    if event.unicode:
                        text += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            
            # клик по панели
            if mx < PANEL:
                # кнопки инструментов
                for i, t in enumerate(tools):
                    if 5 <= mx <= 115 and 30 + i*28 <= my <= 55 + i*28:
                        tool = t

                # кнопки размера
                if 5 <= mx <= 35 and 330 <= my <= 350:
                    size = 2
                if 40 <= mx <= 70 and 330 <= my <= 350:
                    size = 5
                if 75 <= mx <= 115 and 330 <= my <= 350:
                    size = 10

                # палитра
                for i, c in enumerate(colors):
                    px = (i % 2) * 50 + 5
                    py = 370 + (i // 2) * 35
                    if px <= mx <= px+45 and py <= my <= py+30:
                        color = c

            # клик по холсту
            else:
                if tool == "fill":
                    flood_fill(canvas, cx, cy, color)
                elif tool == "text":
                    text_pos = (cx, cy)
                    typing = True
                    text = ""
                elif tool in ("pencil", "eraser"):
                    drawing = True
                    prev = (cx, cy)
                else:
                    drawing = True
                    start = (cx, cy)

        if event.type == pygame.MOUSEMOTION and drawing:
            if mx > PANEL:
                if tool == "pencil":
                    pygame.draw.line(canvas, color, prev, (cx, cy), size)
                    prev = (cx, cy)
                elif tool == "eraser":
                    pygame.draw.line(canvas, (255,255,255), prev, (cx,cy), size*5)
                    prev = (cx, cy)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if drawing and mx > PANEL:
                if tool == "line":
                    pygame.draw.line(canvas, color, start, (cx,cy), size)

                elif tool == "rect":
                    x = min(start[0], cx)
                    y = min(start[1], cy)
                    w = abs(cx - start[0])
                    h = abs(cy - start[1])
                    pygame.draw.rect(canvas, color, (x, y, w, h), size)

                elif tool == "circle":
                    cx2 = (start[0] + cx) // 2
                    cy2 = (start[1] + cy) // 2
                    r = int(((cx-start[0])**2 + (cy-start[1])**2)**0.5 // 2)
                    if r > 0:
                        pygame.draw.circle(canvas, color, (cx2,cy2), r, size)

                elif tool == "square":
                    side = min(abs(cx-start[0]), abs(cy-start[1]))
                    sx = start[0] if cx > start[0] else start[0]-side
                    sy = start[1] if cy > start[1] else start[1]-side
                    pygame.draw.rect(canvas, color, (sx, sy, side, side), size)

                elif tool == "triangle":
                    pts = [start, (start[0], cy), (cx, cy)]
                    pygame.draw.polygon(canvas, color, pts, size)

                elif tool == "rhombus":
                    mx2 = (start[0]+cx)//2
                    my2 = (start[1]+cy)//2
                    pts = [(mx2,start[1]),(cx,my2),(mx2,cy),(start[0],my2)]
                    pygame.draw.polygon(canvas, color, pts, size)

            drawing = False

    # --- рисуем всё ---
    screen.fill((50, 50, 50))

    # предпросмотр фигуры пока тянешь
    if drawing and tool not in ("pencil","eraser","fill","text"):
        temp = canvas.copy()
        if tool == "line":
            pygame.draw.line(temp, color, start, (cx,cy), size)
        elif tool == "rect":
            x = min(start[0],cx); y = min(start[1],cy)
            pygame.draw.rect(temp, color, (x,y,abs(cx-start[0]),abs(cy-start[1])), size)
        elif tool == "circle":
            cx2=(start[0]+cx)//2; cy2=(start[1]+cy)//2
            r=max(1,int(((cx-start[0])**2+(cy-start[1])**2)**0.5//2))
            pygame.draw.circle(temp, color, (cx2,cy2), r, size)
        elif tool == "square":
            side=min(abs(cx-start[0]),abs(cy-start[1]))
            sx=start[0] if cx>start[0] else start[0]-side
            sy=start[1] if cy>start[1] else start[1]-side
            pygame.draw.rect(temp,color,(sx,sy,side,side),size)
        elif tool == "triangle":
            pygame.draw.polygon(temp,color,[start,(start[0],cy),(cx,cy)],size)
        elif tool == "rhombus":
            mx2=(start[0]+cx)//2; my2=(start[1]+cy)//2
            pygame.draw.polygon(temp,color,[(mx2,start[1]),(cx,my2),(mx2,cy),(start[0],my2)],size)
        screen.blit(temp, (PANEL, 0))
    else:
        screen.blit(canvas, (PANEL, 0))

    # текст в процессе набора
    if typing:
        t = font.render(text + "|", True, color)
        screen.blit(t, (PANEL + text_pos[0], text_pos[1]))

    #панель слева
    pygame.draw.rect(screen, (40,40,40), (0,0,PANEL,HEIGHT))
    lbl = font.render("TOOLS:", True, (200,200,200))
    screen.blit(lbl, (5, 10))

    for i, t in enumerate(tools):
        col = (70,120,200) if t == tool else (80,80,80)
        pygame.draw.rect(screen, col, (5, 30+i*28, 110, 24), border_radius=3)
        txt = font.render(t, True, (255,255,255))
        screen.blit(txt, (10, 34+i*28))

    # размер
    size_lbl = font.render("size:", True, (200,200,200))
    screen.blit(size_lbl, (5, 315))
    for i, (s, lbl) in enumerate([(2,"S"),(5,"M"),(10,"L")]):
        col = (70,120,200) if s == size else (80,80,80)
        pygame.draw.rect(screen, col, (5+i*37, 330, 33, 20), border_radius=3)
        screen.blit(font.render(lbl, True, (255,255,255)), (13+i*37, 333))

    #палитра
    clbl = font.render("color:", True, (200,200,200))
    screen.blit(clbl, (5, 358))
    pygame.draw.rect(screen, color, (5, 358, 110, 10))
    for i, c in enumerate(colors):
        px = (i%2)*50+5
        py = 370+(i//2)*35
        pygame.draw.rect(screen, c, (px,py,45,30), border_radius=3)
        if c == color:
            pygame.draw.rect(screen,(255,255,0),(px-1,py-1,47,32),2)

    #сообщение сохранения
    if save_timer > 0:
        save_timer -= 1
        s = font.render(save_msg, True, (0,255,0))
        screen.blit(s, (PANEL+10, 10))

    pygame.display.flip()