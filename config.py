"""Configuración global del juego."""
# Ventana
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 360
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
TITLE = "PingPong"

# Rendimiento
FPS = 60

# Colores
BG_COLOR = (180, 180, 255)

"""Ajustes del juego"""

#AJUSTES PSEUDO 3D
HORIZON_LINE_SY = 30
CAMERA_DEPTH = -120 #Profundidad de la camara en el eje Y, desde el lado del jugador (a 30 unidades del borde de la mesa), negativo para que la camara este detras del jugador
CAMERA_HEIGHT = 254 #Altura de la camara en el eje Z, desde el lado del jugador
Y_MAX = 508 #Profundidad maxima en el eje Y, tamaño en Y de la mesa además de 30 unidades de cada lado de la mesa
FOCAL_LENGTH = 381 #Distancia focal para la proyeccion pseudo 3D, mayor distancia focal significa menor escalado en la distancia
K_PADDING = FOCAL_LENGTH / 2 #Constante para evitar division por cero en la proyeccion pseudo 3D y suavizar el escalado en la distancia

#medidas de la mesa en el espacio 3d

HALF_TABLE_LENGTH = 224 #Largo total de la mesa = 448
HALF_TABLE_WIDTH = 152 #Ancho total de la mesa = 304
TABLE_THICKNESS = 8 #Grosor de la mesa en Z

#Posiciones fijas en el eje de profundidad (Y)

PLAYER_SIDE_Y = 30 
NET_Y = PLAYER_SIDE_Y + HALF_TABLE_LENGTH
OPPONENT_SIDE_Y = NET_Y + HALF_TABLE_LENGTH

#Medidas de la malla
NET_THICKNESS = 8 #Grosor de la malla en Y
HALF_NET_WIDTH = HALF_TABLE_WIDTH + 15
NET_HEIGHT = 16

#Las dimensiones de las raquetas en el espacio 3D
PADDLE_THICKNESS = 8
PADDLE_WIDTH = 30
PADDLE_HEIGHT = 36

#Radio de la pelota
BALL_RADIUS = 4

#Constantes fisicas
GRAVITY = 280
MIN_PADDLE_Z = PADDLE_HEIGHT // 2
MAX_PADDLE_Z = 150
WHEEL_SENSITIVITY = 15

