"""Configuración global del juego."""
# Ventana
WINDOW_WIDTH = 320
WINDOW_HEIGHT = 180
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
TITLE = "PingPong"

# Rendimiento
FPS = 60

# Colores
BG_COLOR = (180, 180, 255)

"""Ajustes del juego"""

HORIZON_LINE_Y = 20
FOCAL_LENGTH = WINDOW_WIDTH // 2 #mitad del ancho para un FOV de 90 grados

#medidas de la mesa
HALF_TABLE_LENGTH = 65
NET_Y = 100

TABLE_MIDDLE_X = WINDOW_WIDTH // 2
MIN_X = 40
MAX_X = 280

OPPONENT_SIDE_Y = NET_Y - HALF_TABLE_LENGTH
PLAYER_SIDE_Y = NET_Y + HALF_TABLE_LENGTH

#constantes fisicas
GRAVITY = 280
PADDLE_SPEED_Z = 150
MAX_Z = 120
WHEEL_SENSITIVITY = 15

