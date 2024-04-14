from random import randint

import pygame as pg


pg.init()

SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE
INITIAL_LENGH_SNAKE: int = 1

POINTER = tuple[int, int]
CENTRAL_POINT: POINTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
UP: POINTER = (0, -1)
DOWN: POINTER = (0, 1)
LEFT: POINTER = (-1, 0)
RIGHT: POINTER = (1, 0)

CHOOSING_DIRECTION: dict[tuple[int, POINTER], POINTER] = {
    (pg.K_UP, LEFT): UP,
    (pg.K_UP, RIGHT): UP,
    (pg.K_DOWN, LEFT): DOWN,
    (pg.K_DOWN, RIGHT): DOWN,
    (pg.K_LEFT, UP): LEFT,
    (pg.K_LEFT, DOWN): LEFT,
    (pg.K_RIGHT, UP): RIGHT,
    (pg.K_RIGHT, DOWN): RIGHT
}

COLOR = tuple[int, int, int]
BOARD_BACKGROUND_COLOR: COLOR = (0, 0, 0)
LINE_COLOR: COLOR = (248, 253, 43)
BORDER_COLOR: COLOR = (93, 216, 228)
APPLE_COLOR: COLOR = (255, 0, 0)
SNAKE_COLOR: COLOR = (0, 255, 0)
TEXT_COLOT: COLOR = (3, 252, 190)

SPEED: int = 20

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption(f"Змейка; Скорость: {SPEED}; Выход 'X' ->")
clock = pg.time.Clock()


class GameObject:
    """Класс - родитель, от которого наследуются друие игровые объекты."""

    def __init__(self, position: POINTER = CENTRAL_POINT,
                 body_color: COLOR = LINE_COLOR):
        self.position = position
        self.body_color = body_color

    def draw(self) -> None:
        """Функция для переопределения в дочерних классах"""
        raise NotImplementedError()


class Apple(GameObject):
    """Класс описывает яблоко и действия с ним."""

    def __init__(self, position: POINTER = CENTRAL_POINT,
                 body_color: COLOR = APPLE_COLOR):
        super().__init__(position, body_color)
        self.position = position
        self.body_color = body_color

    def randomize_position(self, snake_positions) -> None:
        """Устанавливает случайное положение яблока на игровом поле."""
        while True:
            apple_position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                              randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if apple_position not in snake_positions:
                self.position = apple_position
                break

    def draw(self) -> None:
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Описывает механику змеи."""

    def __init__(self, length: int = INITIAL_LENGH_SNAKE,
                 position: POINTER = CENTRAL_POINT,
                 direction: POINTER = RIGHT,
                 next_direction: POINTER = RIGHT,
                 body_color=SNAKE_COLOR):
        super().__init__(position, body_color)
        self.length = length
        self.positions = [position]
        self.direction = direction
        self.next_direction = next_direction
        self.body_color = body_color
        self.last = self.position

    def update_direction(self) -> None:
        """Устанавливает новое направление змеи."""
        if self.next_direction:
            self.direction = self.next_direction

    def move(self) -> None:
        """Реализует механику движения змеи."""
        self.last = self.positions[-1]
        first_coordinate, second_coordinate = self.get_head_position()

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
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки.
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента.
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

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
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            snake.next_direction = CHOOSING_DIRECTION.get(
                (event.key, snake.direction),
                snake.direction
            )


def main() -> None:
    """Описыват основную логику игры."""
    apple = Apple(CENTRAL_POINT, APPLE_COLOR)
    snake = Snake(INITIAL_LENGH_SNAKE, CENTRAL_POINT, UP, RIGHT, SNAKE_COLOR)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.positions.append(snake.positions[-1])
            snake.length += 1
            apple.randomize_position(snake.positions)
            apple.draw()
        if (snake.length > 2
                and snake.get_head_position() in snake.positions[1:]):
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
