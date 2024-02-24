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
SPEED = 8

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс объектов игры"""

    def __init__(self,
                 position=((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)),
                 body_color=BOARD_BACKGROUND_COLOR,
                 border_color=BORDER_COLOR,
                 board_color=BOARD_BACKGROUND_COLOR):
        """Базовые параметы класса"""
        self.position = position
        self.body_color = body_color
        self.border_color = border_color
        self.board_color = board_color

    def draw(self):
        """Любой игровой объект будет иметь отрисовку"""
        raise (NotImplementedError('Переопределите метод в дочерних классах'))

    def draw_cell(self, surface, cell_coordinates):
        """Отрисовка клеток"""
        head_rect = pygame.Rect(cell_coordinates, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, self.border_color, head_rect, 1)

    def delete_cell(self, surface, cell_coordinates):
        """Затирание клеток"""
        position = pygame.Rect(cell_coordinates, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.board_color, position)


class Apple(GameObject):
    """Класс игрового объекта ЯБЛОКО"""

    def __init__(self, body_color=APPLE_COLOR):
        """Базовые параметы класса"""
        super().__init__(body_color=body_color)
        self.randomize_position(
            forbidden_positions=((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        )

    def randomize_position(self, forbidden_positions):
        """Яблоко появляется в случайном месте на игровом поле"""
        self.position = (randint(0, GRID_WIDTH) * GRID_SIZE,
                         randint(0, GRID_HEIGHT) * GRID_SIZE,)
        while self.position in forbidden_positions:
            self.position = self.randomize_position(forbidden_positions)

    def draw(self, surface):
        """Отрисовка Яблока"""
        super().draw_cell(surface, cell_coordinates=(self.position))


class Snake(GameObject):
    """Класс игрового объекла ЗМЕЙКА"""

    def __init__(self):
        """Базовые параметы класса"""
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()

    def get_head_position(self):
        """Возвращает первый элемент в списке positions(ГОЛОВУ)"""
        return self.positions[0]

    def update_direction(self):
        """Обновление направления движения"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Движение змейки"""
        self.head_position = self.get_head_position()
        self.new_head_position = ((self.head_position[0]
                                  + self.direction[0]
                                  * GRID_SIZE)
                                  % SCREEN_WIDTH,
                                  (self.head_position[1]
                                  + self.direction[1]
                                  * GRID_SIZE)
                                  % SCREEN_HEIGHT)

        if self.new_head_position in self.positions[2:]:
            # Если змейка съела себя(кроме головы и шеи) - СБРОС
            # Для сброса Змейка должна состоять минимум из 3 секций
            self.reset()
        else:
            # Если столкновения не произошло,
            # новая позиция головы вставляется в начало списка
            self.positions.insert(0, self.new_head_position)

        if self.length < len(self.positions):
            self.last = self.positions.pop()  # Последний элемент удаляется

    def draw(self, surface):
        """Отрисовка Змейки"""
        super().draw_cell(surface, cell_coordinates=(self.get_head_position()))

        if self.last:
            super().delete_cell(surface, cell_coordinates=(self.last))

    def reset(self):
        """Сброс змейки в начальное состояние после столкновения с собой"""
        self.next_direction = None  # При запуске игры еще не определено
        self.last = None  # Изначально у змейки нет «последнего сегмента»
        self.length = 1  # Только одна голова в начале игры и при сбросе
        self.positions = [self.position]
        self.direction = choice((DOWN, UP, RIGHT, LEFT))
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
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        snake.draw(screen)
        apple.draw(screen)

        snake.move()
        handle_keys(snake)

        if snake.new_head_position == apple.position:  # Cъела ли змейка яблоко
            snake.length += 1  # Если съела, то выросла
            # яблоко рандомится, но не на позициях змейки
            apple.randomize_position(snake.positions)
            apple.draw(screen)

        # if snake.new_head_position in snake.positions[2:]:
        #    apple.randomize_position(snake.positions)
        #    apple.draw(screen)

        snake.update_direction()
        pygame.display.update()


if __name__ == "__main__":
    main()
