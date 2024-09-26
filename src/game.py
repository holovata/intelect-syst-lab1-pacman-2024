import pygame
from src.level_generator import LevelGenerator
from src.pacman import PacMan
from src.ghost import Ghost
from src.utils import load_assets
import sys
import random


class Game:
    TILE_SIZE = 30

    def __init__(self, level_number=1):
        self.level_number = level_number

        # Ініціалізація Pygame
        pygame.init()

        # Створення вікна гри
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pac-Man")

        # Завантаження асетів
        self.assets = load_assets()

        # Перевірка, що всі необхідні асети завантажені
        required_assets = ['pacman', 'ghost_red', 'ghost_pink', 'ghost_blue', 'ghost_orange', 'maze_tiles']
        missing_assets = [asset for asset in required_assets if asset not in self.assets]
        if missing_assets:
            raise ValueError(f"Не вдалося завантажити асети: {', '.join(missing_assets)}")

        # Ініціалізація годин для контролю FPS
        self.clock = pygame.time.Clock()

        # Ініціалізація стану гри
        self.state = 'start'  # Можливі стани: 'start', 'playing', 'game_over'

        # Ініціалізація змінних, які будуть встановлені при запуску гри
        self.maze = None
        self.pacman = None
        self.ghosts = []
        self.scale = 1  # Масштаб лабіринту
        self.running = True

    def run(self):
        while self.running:
            if self.state == 'start':
                self.show_start_screen()
            elif self.state == 'playing':
                self.handle_events()
                self.update()
                self.draw()
                self.clock.tick(60)  # Обмеження до 60 FPS
            elif self.state == 'game_over':
                self.show_game_over_screen()

        pygame.quit()
        sys.exit()

    def show_start_screen(self):
        self.screen.fill((0, 0, 0))  # Чорний фон
        font = pygame.font.SysFont(None, 48)
        text = font.render("Натисніть будь-яку клавішу для початку", True, (255, 255, 255))  # Білий текст
        text_rect = text.get_rect(center=(self.screen_width//2, self.screen_height//2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

        # Очікування натискання будь-якої клавіші для початку гри
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    self.start_game()
                    waiting = False
            self.clock.tick(60)

    def show_game_over_screen(self):
        self.screen.fill((0, 0, 0))  # Чорний фон
        font = pygame.font.SysFont(None, 48)
        text_game_over = font.render("Гра завершена", True, (255, 0, 0))  # Червоний текст
        text_restart = font.render("Натисніть будь-яку клавішу для повторного запуску", True, (255, 255, 255))  # Білий текст
        text_game_over_rect = text_game_over.get_rect(center=(self.screen_width//2, self.screen_height//2 - 30))
        text_restart_rect = text_restart.get_rect(center=(self.screen_width//2, self.screen_height//2 + 30))
        self.screen.blit(text_game_over, text_game_over_rect)
        self.screen.blit(text_restart, text_restart_rect)
        pygame.display.flip()

        # Очікування натискання будь-якої клавіші для перезапуску гри
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    self.level_number += 1  # Збільшення номера рівня для ускладнення
                    self.start_game()
                    waiting = False
            self.clock.tick(60)

    def start_game(self):
        try:
            # Ініціалізація або скидання ігрових об'єктів для нового рівня
            self.state = 'playing'

            # Генерація рівня
            level_generator = LevelGenerator(self.level_number)
            self.maze, ghost_speed, ghost_behaviour, number_of_ghosts = level_generator.generate_level()

            # Забезпечуємо, що позиція привидів вільна
            self.maze.grid[self.maze.ghost_start_position[1]][self.maze.ghost_start_position[0]] = 0

            # Обмеження масштабу лабіринту
            maze_width = self.maze.width
            maze_height = self.maze.height
            scale_x = self.screen_width / (maze_width * self.TILE_SIZE)
            scale_y = self.screen_height / (maze_height * self.TILE_SIZE)
            self.scale = min(scale_x, scale_y, 1)

            # Розміщення точок (їжі) в лабіринті
            self.maze.place_dots()

            # Створення Пакмена
            self.pacman = PacMan(self.maze, self.assets['pacman'], self.level_number, self.ghosts)
            self.maze.pacman = self.pacman  # Зв'язуємо Пакмена з лабіринтом для перевірки зайнятості

            # Визначення кольорів привидів
            ghost_colors = ['red', 'pink', 'blue', 'orange']

            # Визначення стартових позицій привидів
            base_x, base_y = self.maze.ghost_start_position
            offset_positions = [
                (base_x, base_y),
                (base_x + 1, base_y),
                (base_x, base_y + 1),
                (base_x + 1, base_y + 1)
            ]

            # Створення привидів
            self.ghosts = []
            self.maze.ghosts = []  # Очищення списку привидів в лабіринті перед додаванням
            for i in range(number_of_ghosts):
                color = ghost_colors[i % len(ghost_colors)]
                ghost_image_key = f'ghost_{color}'
                if ghost_image_key not in self.assets:
                    print(f"Відсутній асет для {ghost_image_key}, пропускаємо створення цього привида.")
                    continue  # Пропустити створення, якщо асет відсутній

                # Отримання унікальної позиції для кожного привида
                if i < len(offset_positions):
                    position = offset_positions[i]
                else:
                    # Якщо привидів більше, ніж визначено позицій, генеруємо випадкові
                    position = self.get_random_ghost_position()

                # Перевірка, що позиція не зайнята стіною та знаходиться в межах лабіринту
                if self.maze.is_path(position) and not self.is_position_occupied(position):
                    ghost = Ghost(self.maze, self.assets[ghost_image_key], ghost_speed, self.level_number, position)
                    self.ghosts.append(ghost)
                    self.maze.ghosts.append(ghost)
                else:
                    print(f"Недопустима або зайнята позиція для привида: {position}")
                    # Спробувати знайти іншу позицію
                    position = self.get_random_ghost_position()
                    if self.maze.is_path(position) and not self.is_position_occupied(position):
                        ghost = Ghost(self.maze, self.assets[ghost_image_key], ghost_speed, self.level_number, position)
                        self.ghosts.append(ghost)
                        self.maze.ghosts.append(ghost)
                    else:
                        print(f"Не вдалося розмістити привида на позиції: {position}")

            print(f"Створено привидів: {len(self.ghosts)}")  # Відлагоджувальне повідомлення

            # Призначення списку привидів Пакмену для обчислення відстаней
            self.pacman.ghosts = self.ghosts

        except Exception as e:
            print(f"Помилка при запуску гри: {e}")
            self.running = False

    def get_random_ghost_position(self):
        # Генеруємо випадкову позицію для привида, уникаючи стартових позицій
        attempts = 0
        max_attempts = 100
        while attempts < max_attempts:
            x = random.randint(1, self.maze.width - 2)
            y = random.randint(1, self.maze.height - 2)
            if (x, y) != self.maze.start_position and (x, y) != self.maze.ghost_start_position and self.maze.is_path((x, y)):
                return (x, y)
            attempts += 1
        return self.maze.ghost_start_position  # У крайньому випадку

    def is_position_occupied(self, position):
        # Перевіряємо, чи зайнята позиція іншим привидом або Пакменом
        if self.pacman and self.pacman.position == position:
            return True
        for ghost in self.ghosts:
            if ghost.position == position:
                return True
        return False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                try:
                    self.pacman.handle_key_event(event)  # Припускається, що PacMan обробляє події клавіатури
                except Exception as e:
                    print(f"Помилка при обробці події клавіатури: {e}")

    def update(self):
        try:
            # Оновлення Пакмена
            self.pacman.update()

            # Оновлення привидів
            for ghost in self.ghosts:
                ghost.update(self.pacman)

            # Перевірка зіткнень між Пакменом та привидами
            for ghost in self.ghosts:
                if ghost.position == self.pacman.position:
                    self.state = 'game_over'
                    break

            # Перевірка, чи зібрані всі точки (їжа)
            if not self.maze.dots:
                self.state = 'game_over'  # Або перехід на наступний рівень автоматично
        except Exception as e:
            print(f"Помилка при оновленні гри: {e}")
            self.state = 'game_over'

    def draw(self):
        try:
            # Очищення екрану
            self.screen.fill((0, 0, 0))  # Чорний фон

            # Відтворення лабіринту з урахуванням масштабу
            self.maze.draw(self.screen, self.scale)

            # Відтворення точок (їжі)
            self.draw_dots()

            # Відтворення Пакмена
            self.pacman.draw(self.screen, self.scale)

            # Відтворення привидів
            for ghost in self.ghosts:
                ghost.draw(self.screen, self.scale)

            # Оновлення дисплею
            pygame.display.flip()
        except Exception as e:
            print(f"Помилка при відтворенні гри: {e}")
            self.state = 'game_over'

    def draw_dots(self):
        try:
            # Відтворення точок (їжі) як маленьких жовтих кіл
            dot_color = (255, 255, 0)  # Жовтий колір
            dot_radius = 5 * self.scale  # Масштабуємо радіус точки
            for dot in self.maze.dots:
                pixel_pos = self.maze.get_pixel_position(dot, self.scale)
                center = (int(pixel_pos[0] + self.TILE_SIZE * self.scale / 2),
                          int(pixel_pos[1] + self.TILE_SIZE * self.scale / 2))
                pygame.draw.circle(self.screen, dot_color, center, int(dot_radius))
        except Exception as e:
            print(f"Помилка при відтворенні точок: {e}")
