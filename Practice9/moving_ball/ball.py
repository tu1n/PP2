import pygame

class Ball:
    def __init__(self, width, height):
        self.radius= 25
        self.color=(255,0,0)
        self.speed=20
        self.width=width
        self.height=height
        self.x=width//2
        self.y=height//2

    def move(self,d):
        if d=='up' and self.y -self.speed >=self.radius:
            self.y -=self.speed
        elif d=='down' and self.y +self.speed <= self.height - self.radius:
            self.y +=self.speed
        elif d=='left' and self.x - self.speed >=self.radius:
            self.x -=self.speed
        elif d=='right' and self.x + self.speed<= self.width - self.radius:
            self.x +=self.speed

    def draw(self,screen):
        pygame.draw.circle(screen, self.color, (self.x,self.y), self.radius)
