"""Configuración global del juego."""
#Ventana
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 360
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
TITLE = "PingPong"

# Rendimiento
FPS = 60

# Colores
BG_COLOR = (75, 156, 211)

"""Ajustes del juego"""

#medidas de la mesa en el espacio 3d

HALF_TABLE_LENGTH = 274 #Largo total de la mesa = 548
HALF_TABLE_WIDTH = 152 #Ancho total de la mesa = 304
TABLE_THICKNESS = 8 #Grosor de la mesa en Z

#Posiciones fijas en el eje de profundidad (Y)
PLAYER_SIDE_Y = 30 
NET_Y = PLAYER_SIDE_Y + HALF_TABLE_LENGTH
OPPONENT_SIDE_Y = NET_Y + HALF_TABLE_LENGTH
Y_MAX = OPPONENT_SIDE_Y + PLAYER_SIDE_Y #Profundidad maxima de las raquetas en el eje Y, tamaño en Y de la mesa además de 30 unidades de cada lado de la mesa

#Medidas de la malla
HALF_NET_THICKNESS = 4 #Grosor de la malla en Y
HALF_NET_WIDTH = HALF_TABLE_WIDTH + 24
NET_HEIGHT = 25

#Las dimensiones de las raquetas en el espacio 3D
PADDLE_THICKNESS = 8
PADDLE_WIDTH = 30
PADDLE_HEIGHT = 36

#Radio de la pelota
BALL_RADIUS = 4

MAX_Z = 150 
Z_TABLE = 0
MIN_PADDLE_Z = Z_TABLE + PADDLE_HEIGHT // 2
MAX_PADDLE_Z = 152
FLOOR_Z = -152  

DEFAULT_CPU_CENTER_Y = OPPONENT_SIDE_Y - 30
DEFAULT_CPU_CENTER_Z = 30 + MIN_PADDLE_Z

#Constantes fisicas
GRAVITY = 160
WHEEL_SENSITIVITY = 15
BALL_RESTITUTION = 0.9
PADDLE_RESTITUTION = 0.5
PADDLE_BACK_RESTITUTION = 0.3
NET_RESTITUTION = 0.2
VERTICAL_BRAKING = 0.5
FRICTION = 0.985
MIN_REACTION_SPEED = 5.0
CPU_MOVE_SPEED = 180
