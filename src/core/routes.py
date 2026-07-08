from ..states import *

STATE_ROUTES = {
    "MENU": (MenuState, ["resource_manager", "renderer"]),
    "PLAY": (PlayState, ["resource_manager", "renderer", "physics", "world_renderer", "Paddle", "Ball", "Table"]),
    "PAUSE": (PauseState, ["resource_manager"]),
    "GAMEOVER": (GameOverState, ["resource_manager"]),
    "WIN": (WinState, ["resource_manager"]),
    "CREDITS": (CreditsState, ["resource_manager"])
}