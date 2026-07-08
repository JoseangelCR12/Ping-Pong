from .button import Button
from ..resources.assets_def import UI_CONFIG

def load_ui(state_name, resource_manager):
    """Genera un dict con los botones de cada estado"""
    buttons_dict = {}
    
    #se busca la lista de botones de la pantalla
    state_buttons_data = UI_CONFIG.get(state_name, [])

    for btn_data in state_buttons_data:
        img_n = resource_manager.get_texture(state_name, btn_data["textures"][0])
        img_h = resource_manager.get_texture(state_name, btn_data["textures"][1])
        
        new_button = Button(
            position_type=btn_data["position"],
            offset_x=btn_data["offset_x"],
            offset_y=btn_data["offset_y"],
            image_normal=img_n,
            image_hover=img_h
            )

        buttons_dict[btn_data["name"]] = new_button
    
    return buttons_dict