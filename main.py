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


    #TErmnia lo visual de menus y eso, te faltan unos sprites, unos background y listo

    #Integren fisican, hagan gamerules y arregles las cpus, y habran terminado, USTEDES PUEDEN
    #ah, y hagan los creditos
