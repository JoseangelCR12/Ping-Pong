from ..states import *

STATE_ROUTES = {
    "MENU": (MenuState, ["resource_manager"]),
    "PLAY": (PlayState, ["resource_manager", "renderer", "physics", "pseudo_3D", "Paddle", "Ball"]),
    "PAUSE": (PauseState, ["resource_manager"]),
    "GAMEOVER": (GameOverState, ["resource_manager"]),
    "WIN": (WinState, ["resource_manager"]),
    "CREDITS": (CreditsState, ["resource_manager"])
}