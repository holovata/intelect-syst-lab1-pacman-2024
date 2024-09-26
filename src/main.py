# src/main.py

from src.game import Game


def main():
    level_number = 1
    game = Game(level_number)
    game.run()


if __name__ == "__main__":
    main()
