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
            "sfx": {},
            "music": {}

        }

            
                
        self.PLAY = {
            #--SPRITESHEETS-- 
            "raqueta": ("assets/entities/raqueta.png", (24, 24), 10),
            "pelota": ("assets/entities/pelota.png", (8, 8), 0)
        }
        # si se quiere dar una vuelta al sprite usa un int, si solo quieres ciertos angulos, una tupla con esos angulos
        # mapa cargado: clave -> dict {ruta, tam, ang_aumento/angulos a pedir}
        # si se usa int 0 se recorta el spritesheet y se utiliza como animaciones

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

