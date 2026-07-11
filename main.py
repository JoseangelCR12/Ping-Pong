import os
from src.utils.paths import BASE_DIR

os.chdir(BASE_DIR)

from src.core.game import Game


def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()


    #SIGUE DOCUMENTANDO FLOJOOOOOOO

    #REVISA LO QUE VA CAMBIANDO DIEGO Y COMPAGINEN BIEN LOS CAMBIOS Y LAS FISICAS

    #AGREGA IMPLEMENTACIONES A ENTER Y EXIT EN LOS STATES(PARA QUE GUARDEN Y BORREN CACHE)