MENU = {
        "buttons": [
            {
                "name": "play", "position": "center", "offset_x": 0, "offset_y": 20,
                "textures": ["btn_play", "btn_play_h"]
            },
            { 
                "name": "credits", "position": "bottom_center", "offset_x": 0, "offset_y": -60,
                "textures": ["btn_credits", "btn_credits_h"]
            },
            { 
                "name": "options", "position": "top_left", "offset_x": 16, "offset_y": 16,
                "textures": ["btn_options", "btn_options_h"]
            }

        ],

        "icons": [
            {
                "name": "game_logo", "position": "top_center", "offset_x": 0, "offset_y": 30,
                "texture": "logo"
            }
        ]
}
OPTIONS = { 
        "buttons": [
            {
                "name": "change_theme", "position": "center", "offset_x": -100, "offset_y": 62,
                "textures": ["btn_theme", "btn_theme_h"]
            },
            {
                "name": "change_camera", "position": "center", "offset_x": 100, "offset_y": 62,
                "textures": ["btn_camera", "btn_camera_h"]
            }
            
        ],

        "icons": [
            {
                "name": "menu_underlay", "position": "center", "offset_x": 0, "offset_y": 0,
                "texture": "underlay"
            },
            {
                "name": "music_icon", "position": "center", "offset_x": -145, "offset_y": -85,
                "texture": "music_icon"
            },
            {
                "name": "sound_icon", "position": "center", "offset_x": -145, "offset_y": -45,
                "texture": "sound_icon"
            },
            {
                "name": "w_sensitivity_icon", "position": "center", "offset_x": -145, "offset_y": -5,
                "texture": "w_sensitivity_icon"
            }
        ],

        "sliders": [
            {
                "name": "volume_music", "position": "center", "offset_x": 30, "offset_y": -85,
                "min_value": 0.0, "max_value": 1.0, "init_value": 0.7,
                "textures": ["slider_bar_e", "slider_bar_f", "slider_btn", "slider_btn_h"]
            },
            {
                "name": "volume_sfx", "position": "center", "offset_x": 30, "offset_y": -45,
                "min_value": 0.0, "max_value": 1.0, "init_value": 0.7,
                "textures": ["slider_bar_e", "slider_bar_f", "slider_btn", "slider_btn_h"]
            }, 
            {
                "name": "wheel_sensitivity", "position": "center", "offset_x": 30, "offset_y": -5,
                "min_value": 2, "max_value": 20, "init_value": 15,
                "textures": ["slider_bar_e", "slider_bar_f", "slider_btn", "slider_btn_h"]
            }
        ]
}

PAUSE = { 
        "buttons": [
            {
                "name": "menu", "position": "center", "offset_x": -100, "offset_y": 62,
                "textures": ["btn_home", "btn_home_h"]
            },
            {
                "name": "restart", "position": "center", "offset_x": 100, "offset_y": 62,
                "textures": ["btn_restart", "btn_restart_h"]
            }
            
        ],

        "icons": [
            {
                "name": "underlay", "position": "center", "offset_x": 0, "offset_y": 0,
                "texture": "underlay"
            },
            {
                "name": "music_icon", "position": "center", "offset_x": -145, "offset_y": -85,
                "texture": "music_icon"
            },
            {
                "name": "sound_icon", "position": "center", "offset_x": -145, "offset_y": -45,
                "texture": "sound_icon"
            },
            {
                "name": "w_sensitivity_icon", "position": "center", "offset_x": -145, "offset_y": -5,
                "texture": "w_sensitivity_icon"
            }
        ],

        "sliders": [
            {
                "name": "volume_music", "position": "center", "offset_x": 30, "offset_y": -85,
                "min_value": 0.0, "max_value": 1.0, "init_value": 0.7,
                "textures": ["slider_bar_e", "slider_bar_f", "slider_btn", "slider_btn_h"]
            },
            {
                "name": "volume_sfx", "position": "center", "offset_x": 30, "offset_y": -45,
                "min_value": 0.0, "max_value": 1.0, "init_value": 0.7,
                "textures": ["slider_bar_e", "slider_bar_f", "slider_btn", "slider_btn_h"]
            }, 
            {
                "name": "wheel_sensitivity", "position": "center", "offset_x": 30, "offset_y": -5,
                "min_value": 2, "max_value": 20, "init_value": 15,
                "textures": ["slider_bar_e", "slider_bar_f", "slider_btn", "slider_btn_h"]
            }
        ]
}

SELECTION = { 
        "buttons": [
            {
                "name": "play", "position": "center", "offset_x": 0, "offset_y": 35,
                "textures": ["btn_play", "btn_play_h"]
            }
        ],

        "icons": [
            {
                "name": "underlay", "position": "center", "offset_x": 0, "offset_y": 0,
                "texture": "small_underlay"
            }
        ],

        "sliders": [
            {
                "name": "cpu_level", "position": "center", "offset_x": 0, "offset_y": -25,
                "min_value": 0, "max_value": 3, "init_value": 2,
                "textures": ["slider_bar_e", "cpu_bar_f", "slider_btn", "slider_btn_h"]
            }
        ],

        "texts": [
            {
                "name": "0", "position": "center", "offset_x": 0, "offset_y": -60,
                "message": "¡¡Selecciona una dificultad!!", "size": 20, "color": "white", "font": "main_font", "antialias": True
            },
            {
                "name": "1", "position": "center", "offset_x": 0, "offset_y": -60,
                "message": "Nivel Fácil :D", "size": 20, "color": (153, 229, 80), "font": "main_font", "antialias": True
            },
            {
                "name": "2", "position": "center", "offset_x": 0, "offset_y": -60,
                "message": "Nivel Normal :P", "size": 20, "color": (251, 242, 54), "font": "main_font", "antialias": True
            },
            {
                "name": "3", "position": "center", "offset_x": 0, "offset_y": -60,
                "message": "Nivel Difícil >:C", "size": 20, "color": (172, 50 ,50), "font": "main_font", "antialias": True
            }
        ]
}