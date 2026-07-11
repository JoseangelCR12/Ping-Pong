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
                "name": "game_logo", "position": "top_center", "offset_x": 0, "offset_y": 40,
                "texture": "logo"
            }
        ]
}
OPTIONS = { 
        "buttons": [
            {
                "name": "change_theme", "position": "bottom_center", "offset_x": -120, "offset_y": -90,
                "textures": ["btn_theme", "btn_theme_h"]
            },
            {
                "name": "change_camera", "position": "bottom_center", "offset_x": 120, "offset_y": -90,
                "textures": ["btn_theme", "btn_theme_h"]
            }
            
        ],

        "icons": [
            {
                "name": "menu_underlay", "position": "center", "offset_x": 0, "offset_y": 0,
                "texture": "underlay"
            }
        ],

        "sliders": [
            {
                "name": "volume_music", "position": "top_center", "offset_x": 30, "offset_y": 90,
                "min_value": 0.0, "max_value": 1.0, "init_value": 0.7,
                "textures": ["btn_theme_h", "btn_theme", "btn_theme", "btn_theme_h"]
            },
            {
                "name": "volume_sfx", "position": "center", "offset_x": 30, "offset_y": 0,
                "min_value": 0.0, "max_value": 1.0, "init_value": 0.7,
                "textures": ["btn_theme_h", "btn_theme", "btn_theme", "btn_theme_h"]
            }
        ]
}

PAUSE = { 
        "buttons": [
            {
                "name": "menu", "position": "bottom_center", "offset_x": -120, "offset_y": -90,
                "textures": ["btn_theme", "btn_theme_h"]
            },
            {
                "name": "restart", "position": "bottom_center", "offset_x": 120, "offset_y": -90,
                "textures": ["btn_theme", "btn_theme_h"]
            }
            
        ],

        "icons": [
            {
                "name": "underlay", "position": "center", "offset_x": 0, "offset_y": 0,
                "texture": "underlay"
            }
        ],

        "sliders": [
            {
                "name": "volume_music", "position": "top_center", "offset_x": 30, "offset_y": 90,
                "min_value": 0.0, "max_value": 1.0, "init_value": 0.7,
                "textures": ["btn_theme_h", "btn_theme", "btn_theme", "btn_theme_h"]
            },
            {
                "name": "volume_sfx", "position": "center", "offset_x": 30, "offset_y": 0,
                "min_value": 0.0, "max_value": 1.0, "init_value": 0.7,
                "textures": ["btn_theme_h", "btn_theme", "btn_theme", "btn_theme_h"]
            }
        ]
}
