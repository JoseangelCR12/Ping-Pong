from .button import Button
from .icon import Icon
from .slider import Slider
from .text import Text
from . import ui_config
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..resources.resource_manager import ResourceManager
    from ..systems.audio import Audio

def load_ui(state_name, resource_manager: "ResourceManager", audio_manager: "Audio"):
    """Genera un dict con los botones e iconos de cada estado"""
    ui_elements = {
        "buttons": {},
        "icons": {},
        "sliders": {},
        "texts": {}
    }

    state_dict = getattr(ui_config, state_name)

    
    #se busca la lista de botones de la pantalla
    state_buttons_data = state_dict.get("buttons", [])

    #Funcion envoltorio que reproduce sonidos al clickear un boton
    def click_wrapper():
        audio_manager.play_sound(state_name, "click_sound")

    for btn_data in state_buttons_data:
        img_n = resource_manager.get_texture(state_name, btn_data["textures"][0])
        img_h = resource_manager.get_texture(state_name, btn_data["textures"][1])
        
        new_button = Button(
            position_type=btn_data["position"],
            offset_x=btn_data["offset_x"],
            offset_y=btn_data["offset_y"],
            image_normal=img_n,
            image_hover=img_h,
            on_click=click_wrapper
            )

        ui_elements["buttons"][btn_data["name"]] = new_button

    #se busca la lista de iconos de la pantalla
    state_icons_data = state_dict.get("icons", [])

    for icon_data in state_icons_data:
        img = resource_manager.get_texture(state_name, icon_data["texture"])
       
        
        new_icon = Icon(
            position_type=icon_data["position"],
            offset_x=icon_data["offset_x"],
            offset_y=icon_data["offset_y"],
            image=img
            )
        
        ui_elements["icons"][icon_data["name"]] = new_icon
        
    #se busca la lista de botones de la pantalla
    state_sliders_data = state_dict.get("sliders", [])

     #Funcion envoltorio que reproduce sonidos al deslizar una barra
    def slider_wrapper():
        audio_manager.play_sound(state_name, "slider_sound")

    for slider_data in state_sliders_data:
        img_bar_empty = resource_manager.get_texture(state_name, slider_data["textures"][0])
        img_bar_full = resource_manager.get_texture(state_name, slider_data["textures"][1])
        img_btn_n = resource_manager.get_texture(state_name, slider_data["textures"][2])
        img_btn_h = resource_manager.get_texture(state_name, slider_data["textures"][3])
        
        new_slider = Slider(
            position_type=slider_data["position"],
            offset_x=slider_data["offset_x"],
            offset_y=slider_data["offset_y"],
            min_value=slider_data["min_value"],
            max_value=slider_data["max_value"],
            init_value=slider_data["init_value"],
            image_empty=img_bar_empty,
            image_full=img_bar_full,
            image_btn=img_btn_n,
            image_btn_h=img_btn_h,
            on_slide=slider_wrapper
            )

        ui_elements["sliders"][slider_data["name"]] = new_slider

         #se busca la lista de textos de la pantalla
    state_texts_data = state_dict.get("texts", [])

    for text_data in state_texts_data:
        font = resource_manager.get_font(state_name, text_data["font"], text_data["size"])
       
        
        new_text = Text(
            position_type=text_data["position"],
            offset_x=text_data["offset_x"],
            offset_y=text_data["offset_y"],
            message=text_data["message"],
            color=text_data["color"],
            font=font,
            antialias=text_data["antialias"]
            )
        
        ui_elements["texts"][text_data["name"]] = new_text
    
    return ui_elements