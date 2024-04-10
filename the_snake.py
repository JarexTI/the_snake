from random import randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 200, 200
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTRAL_POINT = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет линий - желтый:
LINE_COLOR = (248, 253, 43)

# Цвет границы ячейки.
BORDER_COLOR = (93, 216, 228)

# Цвет яблока.:
APPLE_COLOR = (255, 0, 0)

# Цвет змейки:
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Класс - родитель, от которого наследуются друие игровые объекты."""

    def __init__(self, position=CENTRAL_POINT, body_color=LINE_COLOR):
        self.position = position
        self.body_color = body_color

    def draw(self) -> None:
        """Отрисовывает сетку, границу каждого поля."""
        # Горизонтальные линии.
        for i in range(1, GRID_HEIGHT):
            pygame.draw.line(
                screen,
                LINE_COLOR,
                (0, i * GRID_SIZE),
                (SCREEN_WIDTH, i * GRID_SIZE),
                3
            )

        # Вертикальные линии.
        for i in range(1, GRID_WIDTH):
            pygame.draw.line(
                screen,
                LINE_COLOR,
                (i * GRID_SIZE, 0),
                (i * GRID_SIZE, SCREEN_HEIGHT),
                3
            )


class Apple(GameObject):
    """Класс описывает яблоко и действия с ним."""

    def __init__(self, position=CENTRAL_POINT, body_color=APPLE_COLOR):
        super().__init__(position, body_color)
        self.position = position
        self.body_color = body_color

    def randomize_position(self, snake_positions) -> None:
        """Устанавливает случайное положение яблока на игровом поле."""
        apple_position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                          randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        # Если яблоко появилось в змейке.
        if apple_position in snake_positions:
            self.randomize_position(snake_positions)
        else:
            self.position = apple_position

    def draw(self) -> None:
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Описывает механику змеи."""

    def __init__(self, length=1, position=CENTRAL_POINT,
                 direction=RIGHT, next_direction=None,
                 body_color=SNAKE_COLOR):
        super().__init__(position, body_color)
        self.length = length
        self.positions = position
        self.direction = direction
        self.next_direction = next_direction
        self.body_color = body_color
        self.last = None

    def update_direction(self) -> None:
        """Устанавливает новое направление змеи."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Реализует механику движения змеи."""
        self.last = self.positions[-1]
        first_coordinate, second_coordinate = self.positions[0]

        # Изменяем положение змеи.
        if self.direction == UP:
            second_coordinate -= GRID_SIZE
        elif self.direction == DOWN:
            second_coordinate += GRID_SIZE
        elif self.direction == LEFT:
            first_coordinate -= GRID_SIZE
        elif self.direction == RIGHT:
            first_coordinate += GRID_SIZE

        # Корректируем положение змеи, если она вышла за пределы поля.
        first_coordinate = (first_coordinate + SCREEN_WIDTH) % SCREEN_WIDTH
        second_coordinate = (second_coordinate + SCREEN_HEIGHT) % SCREEN_HEIGHT

        new_coordinate = (first_coordinate, second_coordinate)
        self.positions.insert(0, new_coordinate)
        self.positions = self.positions[:-1]

    def draw(self) -> None:
        """Отрисовывает змею и стираем её след."""
        # Отрисовка тела змеи.
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки.
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента.
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self) -> tuple[int, int]:
        """Получаем координаты головы змеи."""
        return self.positions[0]

    def reset(self) -> None:
        """Возвращаем змею к настройкам по умолчанию."""
        self.length = 1
        self.positions = self.positions[:1]


def handle_keys(snake: Snake) -> None:
    """Функция обрабатывает закрытие игрового окна и
    нажатие клавиш для передачи направления движения.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main() -> None:
    """Описыват основную логику игры."""
    # Объявляем экземпляры классов.
    game_object = GameObject(CENTRAL_POINT, (50, 50, 50))
    apple = Apple(CENTRAL_POINT, APPLE_COLOR)
    snake = Snake(1, [CENTRAL_POINT], UP, None, SNAKE_COLOR)
    while True:
        clock.tick(SPEED)
        # Обработка управления змейкой.
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        # Если змея съела яблоко.
        if snake.get_head_position() == apple.position:
            # увеличиваем длину змеи.
            snake.positions.append(snake.positions[-1])
            snake.length += 1
            # Генерируем новое яблоко
            apple.randomize_position(snake.positions)
            apple.draw()
        # Проверяйте столкновения змейки с собой.
        if (snake.length > 2
                and snake.get_head_position() in snake.positions[1:]):
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        game_object.draw()
        apple.draw()
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
