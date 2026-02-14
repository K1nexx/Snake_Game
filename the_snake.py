from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (20, 20, 20)
CLR = BORDER_COLOR
# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 13

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self):
        """Инициализирует игровой объект."""
        self.position = [320, 240]
        self.body_color = None

    def draw(self):
        """Отрисовывает объект на экране."""
        pass


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        """Инициализирует змейку."""
        self.position = [320, 240]
        self.positions = [[320, 240]]
        self.body_color = SNAKE_COLOR
        self.direction = RIGHT
        self.lenght = 1
        self.next_direction = None
        self.last = None

    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions:
            rect = pygame.Rect(*position, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        if self.last:
            last_rect = pygame.Rect(*self.last, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
            pygame.draw.rect(screen, BORDER_COLOR, last_rect, 1)

    def move(self):
        """Перемещает змейку в текущем направлении."""
        position = self.get_head_position()
        if len(self.positions) == self.lenght:
            self.last = list(self.positions[0])
            self.positions.pop(0)
        x = position[0] + GRID_SIZE * self.direction[0]
        y = position[1] + GRID_SIZE * self.direction[1]
        if x >= 640:
            x = x % 640
        elif x < 0:
            x = 620
        if y >= 480:
            y = y % 480
        elif y < 0:
            y = 460
        self.positions.append([x, y])

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[-1]

    def reset(self):
        """Сбрасывает состояние змейки к начальному."""
        for position in self.positions:
            last_rect = pygame.Rect(*position, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
            pygame.draw.rect(screen, BORDER_COLOR, last_rect, 1)
        last_rect = pygame.Rect(*self.last, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
        pygame.draw.rect(screen, BORDER_COLOR, last_rect, 1)
        self.positions = [[320, 240]]
        self.direction = RIGHT
        self.lenght = 1
        self.next_direction = None
        self.last = None


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self):
        """Инициализирует яблоко."""
        self.position = [320, 240]
        self.randomize_position()
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Устанавливает случайную позицию для яблока."""
        self.position[0] = randint(0, 31) * GRID_SIZE
        self.position[1] = randint(0, 23) * GRID_SIZE

    def draw(self):
        """Отрисовывает яблоко на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция игры."""
    pygame.init()
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, CLR, (x, 0), (x, SCREEN_HEIGHT), 1)
        pygame.draw.line(screen, CLR, (x - 1, 0), (x - 1, SCREEN_HEIGHT), 1)
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, CLR, (0, y), (SCREEN_WIDTH, y), 1)
        pygame.draw.line(screen, CLR, (0, y - 1), (SCREEN_WIDTH, y - 1), 1)
    snake = Snake()
    apple = Apple()
    running = True
    while running:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if (snake.get_head_position() == apple.position):
            apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()
            snake.lenght += 1
        if (snake.get_head_position() in snake.positions[:-1]):
            snake.reset()
        apple.draw()
        snake.draw()
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
