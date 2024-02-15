from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

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
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс объектов игры"""

    position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
    body_color = None

    def __init__(self, position, body_color):
        """Базовые параметы класса"""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Любой игровой объект имеет отрисовку"""
        pass


class Apple(GameObject):
    """Класс игрового объекта ЯБЛОКО"""

    def __init__(self, position, body_color):
        self.position = position
        self.position = self.randomize_position()
        self.body_color = body_color

    def randomize_position(self):
        """Яблоко появляется в случайном месте на игровом поле"""
        return (randint(0, GRID_WIDTH) * GRID_SIZE,
                randint(0, GRID_HEIGHT) * GRID_SIZE)

    def draw(self, surface):
        """Отрисовка Яблока"""
        rect = pygame.Rect((self.position[0], self.position[1]),
                           (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс игрового объекла ЗМЕЙКА"""

    def __init__(self, body_color):
        """Базовые параметы класса"""
        self.last = None  # Изначально у змейки нет «последнего сегмента»
        self.positions = [GameObject.position]  # Центр экрана
        self.direction = RIGHT
        self.body_color = body_color
        self.length = 1  # Только одна голова в начале игры

    def update_direction(self):
        """Обновление направления движения"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Движение змейки"""
        self.head_position = self.get_head_position()
        new_head_position = self.position
        if new_head_position in self.positions[2:]:
            self.reset()
        else:
            self.position.insert(0, new_head_position)
        if new_head_position > GRID_WIDTH:
            new_head_position = new_head_position % (SCREEN_WIDTH + 1)
        if new_head_position > GRID_HEIGHT:
            new_head_position = new_head_position % (SCREEN_HEIGHT + 1)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def get_head_position(self):
        """Возвращает первый элемент в списке positions(ГОЛОВУ)"""
        return GameObject.position

    def draw(self, surface):
        """Отрисовка Змейки"""
        for position in self.positions[:-1]:
            rect = pygame.Rect((position[0], position[1]),
                               (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]), (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сброс змейки в начальное состояние после столкновения с собой"""
        self.length = 1
        self.positions = GameObject.position
        self.direction = choice(DOWN, UP, RIGHT, LEFT)
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Обработка событий клавиш"""
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
    """
    Создание экземпляров классов(Snake и Apple)
    и описание основной логики игры
    """
    #apple = Apple()
    snake = Snake(SNAKE_COLOR)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        #apple.draw(screen)
        snake.draw(screen)

        #if snake.get_head_position == apple.position:  # съела ли змейка яблоко
        #    snake.length += 1
        #    return apple.randomize_position()

        snake.move()
        snake.update_direction()
        pygame.display.update()


if __name__ == "__main__":
    main()
