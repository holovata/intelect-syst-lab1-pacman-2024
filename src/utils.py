# src/utils.py

import pygame
import os


def load_assets():
    assets = {}
    try:
        # Отримуємо шлях до поточного файлу
        base_path = os.path.dirname(os.path.abspath(__file__))
        # Формуємо шлях до папки з зображеннями
        images_path = os.path.join(base_path, '..', 'assets', 'images')

        # Бажаний розмір зображень
        image_size = (30, 30)

        # Завантаження та масштабування зображень
        assets['pacman'] = pygame.image.load(os.path.join(images_path, 'pacman.png')).convert_alpha()
        assets['pacman'] = pygame.transform.scale(assets['pacman'], image_size)

        assets['ghost_red'] = pygame.image.load(os.path.join(images_path, 'ghost_red.png')).convert_alpha()
        assets['ghost_red'] = pygame.transform.scale(assets['ghost_red'], image_size)

        assets['ghost_pink'] = pygame.image.load(os.path.join(images_path, 'ghost_pink.png')).convert_alpha()
        assets['ghost_pink'] = pygame.transform.scale(assets['ghost_pink'], image_size)

        assets['ghost_blue'] = pygame.image.load(os.path.join(images_path, 'ghost_blue.png')).convert_alpha()
        assets['ghost_blue'] = pygame.transform.scale(assets['ghost_blue'], image_size)

        assets['ghost_orange'] = pygame.image.load(os.path.join(images_path, 'ghost_orange.png')).convert_alpha()
        assets['ghost_orange'] = pygame.transform.scale(assets['ghost_orange'], image_size)

        assets['maze_tiles'] = pygame.image.load(os.path.join(images_path, 'maze_tiles.png')).convert_alpha()
        assets['maze_tiles'] = pygame.transform.scale(assets['maze_tiles'], image_size)

        assets['dot'] = pygame.image.load(os.path.join(images_path, 'dot.png')).convert_alpha()
        assets['dot'] = pygame.transform.scale(assets['dot'], image_size)

        # Завантаження звуків та інших ресурсів за потреби
        # Приклад:
        # assets['eat_pellet'] = pygame.mixer.Sound(os.path.join(base_path, '..', 'assets', 'sounds', 'eat_pellet.wav'))
    except pygame.error as e:
        print(f"Помилка завантаження ресурсу: {e}")
    except FileNotFoundError as e:
        print(f"Файл не знайдено: {e}")
    return assets
