import random
import pygame

CELL_SIZE = 20
FPS = 10

class SnakeGame:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.snake = [(0, 0)]
        self.direction = (0, 1)
        self.running = True
        self.set_random_fruit()

    def set_random_fruit(self):
        while True:
            fruit = (random.randint(0, self.height - 1), random.randint(0, self.width - 1))
            if fruit not in self.snake:
                self.fruit = fruit
                break

    def move(self):
        head_r, head_c = self.snake[-1]
        dr, dc = self.direction
        new_r, new_c = head_r + dr, head_c + dc

        if not (0 <= new_r < self.height and 0 <= new_c < self.width) or (new_r, new_c) in self.snake:
            self.running = False
            return

        self.snake.append((new_r, new_c))

        if (new_r, new_c) == self.fruit:
            self.set_random_fruit()
        else:
            self.snake.pop(0)

    def change_direction(self, new_direction):
        x1, y1 = self.direction
        x2, y2 = new_direction
        if x1 * x2 + y1 * y2 != -1:
            self.direction = new_direction

class GameView:
    def __init__(self, game):
        pygame.init()
        self.game = game
        self.screen = pygame.display.set_mode((game.width * CELL_SIZE, game.height * CELL_SIZE))
        self.clock = pygame.time.Clock()

    def draw(self):
        self.screen.fill((0, 0, 0))
        for r, c in self.game.snake:
            pygame.draw.rect(self.screen, (0, 255, 0), (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, (255, 0, 0), (self.game.fruit[1] * CELL_SIZE, self.game.fruit[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.flip()

class GameController:
    def __init__(self, game, view):
        self.game = game
        self.view = view

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.game.change_direction((-1, 0))
                elif event.key == pygame.K_DOWN:
                    self.game.change_direction((1, 0))
                elif event.key == pygame.K_LEFT:
                    self.game.change_direction((0, -1))
                elif event.key == pygame.K_RIGHT:
                    self.game.change_direction((0, 1))

    def run(self):
        while self.game.running:
            self.handle_events()
            self.game.move()
            self.view.draw()
            self.view.clock.tick(FPS)
        pygame.quit()


if __name__ == "__main__":
    game = SnakeGame(20, 15)
    view = GameView(game)
    controller = GameController(game, view)
    controller.run()
