SCREEN_WIDTH = 800
SCREEN_HEIGHT=600

CELL_SIZE = 20  # Размер одной клетки сетки

#количество клеток по горизонтали и вертикали
COLS=SCREEN_WIDTH // CELL_SIZE
ROWS = SCREEN_HEIGHT // CELL_SIZE

FPS = 60  # Кадров в секунду

# Базовая скорость змейки
BASE_SPEED = 8
SPEED_PER_LEVEL = 1  # Насколько ускоряется каждый уровень

#cколько еды нужно съесть, чтобы перейти на следующий уровень
FOOD_PER_LEVEL = 5

# Цвета (RGB)
BLACK = (0, 0, 0)
WHITE=(255,255,255)
GREEN = (0, 200, 0)
DARK_GREEN=(0,150,0)
RED = (220, 0, 0)
DARK_RED = (100, 0, 0)      # Цвет яда
YELLOW=(255, 220, 0)
ORANGE = (255, 140, 0)
BLUE = (50, 100, 255)
CYAN = (0, 220, 220)
PURPLE=(160, 0, 200)
GRAY = (80, 80, 80)
DARK_GRAY = (40, 40, 40)
LIGHT_GRAY = (160, 160, 160)

# Очки за разные виды еды
FOOD_POINTS = {
    "normal":10,
    "bonus": 25,   #бонусная еда — даёт больше очков
    "poison": 0,   # яд — очков не даёт, только вред
}

# Сколько живёт еда / пауэр-ап на поле
FOOD_LIFETIME=8000      # 8 секунд в миллисекундах
POWERUP_LIFETIME = 8000   # Тоже 8 секунд

# Длительность эффекта пауэр-апа
POWERUP_DURATION = 5000   # 5 секунд