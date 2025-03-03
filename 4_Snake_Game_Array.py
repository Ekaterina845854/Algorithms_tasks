import random
import pygame

CELL_SIZE = 20
FPS = 10

class SnakeGame:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.snake = [(0, 0)] 
        self.board[0][0] = 1 
        self.direction = (0, 1) 
        self.set_random_fruit()
        self.running = True

    def set_random_fruit(self):
        empty_cells = [(r, c) for r in range(self.height) for c in range(self.width) if self.board[r][c] == 0]
        if empty_cells:
            fruit_pos = random.choice(empty_cells)
            self.board[fruit_pos[0]][fruit_pos[1]] = -1

    def move(self):
        head_r, head_c = self.snake[-1]
        dr, dc = self.direction
        new_r, new_c = head_r + dr, head_c + dc
        if not (0 <= new_r < self.height and 0 <= new_c < self.width) or self.board[new_r][new_c] > 0:
            self.running = False
            return
        self.snake.append((new_r, new_c))
        if self.board[new_r][new_c] == -1: 
            self.set_random_fruit()
        else:
            tail_r, tail_c = self.snake.pop(0)
            self.board[tail_r][tail_c] = 0
        for i, (r, c) in enumerate(self.snake):
            self.board[r][c] = i + 1

    def up(self):
        if self.direction != (1, 0):
            self.direction = (-1, 0)
    def down(self):
        if self.direction != (-1, 0):
            self.direction = (1, 0)
    def left(self):
        if self.direction != (0, 1):
            self.direction = (0, -1)
    def right(self):
        if self.direction != (0, -1):
            self.direction = (0, 1)

class GameView:
    def __init__(self, game):
        pygame.init()
        self.game = game
        self.screen = pygame.display.set_mode((game.width * CELL_SIZE, game.height * CELL_SIZE))
        self.clock = pygame.time.Clock()

    def draw(self):
        self.screen.fill((0, 0, 0))
        for r in range(self.game.height):
            for c in range(self.game.width):
                if self.game.board[r][c] > 0:
                    pygame.draw.rect(self.screen, (0, 255, 0), (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                elif self.game.board[r][c] == -1:
                    pygame.draw.rect(self.screen, (255, 0, 0), (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))
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
                    self.game.up()
                elif event.key == pygame.K_DOWN:
                    self.game.down()
                elif event.key == pygame.K_LEFT:
                    self.game.left()
                elif event.key == pygame.K_RIGHT:
                    self.game.right()
    
    def run(self):
        while self.game.running:
            self.handle_events()
            self.game.move()
            self.view.draw()
            self.view.clock.tick(FPS)
        pygame.quit()

# Запуск игры
if __name__ == "__main__":
    game = SnakeGame(20, 15)
    view = GameView(game)
    controller = GameController(game, view)
    controller.run()
