#Importaciones de las entidades para el type hinting.
from .ball import Ball
from .paddle import Paddle

# Definir el __all__ para controlar qué se exporta al importar el paquete entities con *.
__all__ = [
    "Ball",
    "Paddle"
]