import os
from src.utils.paths import BASE_DIR

os.chdir(BASE_DIR)

from src.core.game import Game


def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()



