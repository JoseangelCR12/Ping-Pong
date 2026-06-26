class AssetsDef:
    
    def __init__(self):

        self.GLOBAL = {
            
        }

        self.MENU = {
            "sprites": {
                "btn_play": "assets/ui/btn_play.png", 
                "btn_play_h": "assets/ui/btn_play_h.png",
                "btn_play_p": "assets/ui/btn_play_p.png",
                "btn_credits": "assets/ui/btn_credits.png", 
                "btn_credits_h": "assets/ui/btn_credits_h.png",
                "btn_credits_p": "assets/ui/btn_credits_p.png"
            },
            "sound": {},
            "music": {}

        }

            
                
        self.PLAY = {
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
            "name": "play", "position": "bottom_center", "offset_x": 0, "offset_y": -40,
            "textures": ["btn_play", "btn_play_h", "btn_play_p"]
        },
        { 
            "name": "credits", "position": "center", "offset_x": 0, "offset_y": 0,
            "textures": ["btn_credits", "btn_credits_h", "btn_credits_p"]
        }
    ]
}

