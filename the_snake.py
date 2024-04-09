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
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    
    def __init__(self, position, body_color):
        self.position = position
        self.body_color = body_color

    def draw(self):
        # Горизонтальные линии.
        for i in range(1, GRID_HEIGHT):
            pygame.draw.line(
                screen,
                (55, 55, 55),
                (0, i * GRID_SIZE),
                (SCREEN_WIDTH, i * GRID_SIZE),
                3
            )

        # Вертикальные линии.
        for i in range(1, GRID_WIDTH):
            pygame.draw.line(
                screen,
                (55, 55, 55),
                (i * GRID_SIZE, 0),
                (i * GRID_SIZE, SCREEN_HEIGHT),
                3
            )


class Apple(GameObject):

    def __init__(self, position, body_color):
        #super().__init__(position, body_color)
        self.position = position
        self.body_color = body_color

    def randomize_position(self) -> None:
        apple_position = (randint(0, GRID_WIDTH)*GRID_SIZE, 
                          randint(0, GRID_HEIGHT)*GRID_SIZE)
        self.position = apple_position

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    
    def __init__(self, length, positions, direction, next_direction, body_color):
        #super().__init__(position, body_color)
        self.length = length
        self.positions = positions
        self.direction = direction
        self.next_direction = next_direction
        self.body_color = body_color
        self.last = self.positions[-1]

    # Метод обновления направления после нажатия на кнопку.
    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        print(self.positions)
        #[ for position in self.positions]
        if self.direction == UP:
            new_coordinate = (self.positions[0][0], 
                              self.positions[0][1]+GRID_SIZE)
            self.positions.insert(0, new_coordinate) 

    def draw(self) -> None:
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        return self.positions[0]

    def reset(self):
        self.positions = self.positions[:1]


# Функция обработки действий пользователя.
def handle_keys(snake):
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


def main():
    # Тут нужно создать экземпляры классов.
    game_object = GameObject((320, 240), (50, 50, 50))
    apple = Apple((40, 340), APPLE_COLOR)
    snake = Snake(1, [(100, 200)], UP, None, SNAKE_COLOR)
    running = True
    snake.draw()
    #apple.draw()
    game_object.draw()
    #pygame.display.update()
    while running:
        clock.tick(20)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        # движение змеи
        snake.draw()

        # когда змея съела яблоко 
        if snake.positions[0] == apple:
            # удаляем яблоко на текущей сетке
            # генерируем и рисуем новое яблоко
            # увеличиваем длину змеи 
            pass
        
        snake.draw()
        #apple.randomize_position()
        #apple.draw()
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
