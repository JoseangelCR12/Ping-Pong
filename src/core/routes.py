from ..states import *

STATE_ROUTES = {
    "MENU": (MenuState, ["resource_manager", "audio"]),
    "PLAY": (PlayState, ["resource_manager", "audio", "renderer", "physics", "world_renderer", "Paddle", "Ball", "Table", "Net"]),
    "PAUSE": (PauseState, ["resource_manager", "audio", "renderer"]),
    "OPTIONS": (OptionsState, ["resource_manager", "audio", "renderer"]),
    "SELECTION": (SelectionState, ["resource_manager", "audio", "renderer"]),
    "GAMEOVER": (GameOverState, ["resource_manager", "audio", "renderer"]),
    "WIN": (WinState, ["resource_manager", "audio", "renderer"]),
    "CREDITS": (CreditsState, ["resource_manager", "audio", "renderer"])
}