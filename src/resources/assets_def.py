class AssetsDef:
    
    def __init__(self):

        self.GLOBAL = {
            
        }

        self.MENU = {
            "sprites": {
                "logo": "assets/ui/logo.png",
                "btn_play": "assets/ui/btn_play.png", 
                "btn_play_h": "assets/ui/btn_play_h.png",
                "btn_credits": "assets/ui/btn_credits.png", 
                "btn_credits_h": "assets/ui/btn_credits_h.png"
            },
            "sound": {},
            "music": {}

        }

            
                
        self.PLAY = {
            "sprites": {
                "table": "assets/entities/table.png",
                "floor": "assets/background/floor.png"
            },
            "spritesheets": {
                "paddle": "assets/entities/paddle.png",
                "ball": "assets/entities/ball.png"
            }, 
            "sound": {},
            "music": {}
        }

ASSETS_DICT = AssetsDef()

UI_CONFIG = { 
    "MENU": [
        {
            "name": "play", "position": "center", "offset_x": 0, "offset_y": 20,
            "textures": ["btn_play", "btn_play_h"]
        },
        { 
            "name": "credits", "position": "bottom_center", "offset_x": 0, "offset_y": -60,
            "textures": ["btn_credits", "btn_credits_h"]
        }
    ]
}

