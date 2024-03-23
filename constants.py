primary_color = "#4251f5"
primary_lighter_color = "#6370ff"
primary_variant_color = "#2d39ba"
secondary_color = "#03DAC6"
background_color = "#000000"
surface_color = "#111111"
surface2_color = "#222222"
surface3_color = "#333333"
surface4_color = "#444444"
error_color = "#B00020"
on_primary_color = "#FFFFFF"
on_secondary_color = "#000000"
on_background_color = "#FFFFFF"
on_surface_color = "#FFFFFF"
on_error_color = "#FFFFFF"

AVAIABLE_MODELS = [{"name": "runwayml/stable-diffusion-v1-5", "branch": "fp16"}]

LINK_STYLE = f"color: {primary_color}; font-weight: bold;"

PROMPT_LAYOUT_STYLE = f"""
    QWidget {{
        background-color: {surface_color};
        color: {on_surface_color};
        border: 1px solid {surface_color};
        font-size: 14px;
        border-radius: 0px;
    }}
    QPushButton {{
        background-color: {primary_color};
        color: {on_primary_color};
        border-radius: 0px;
    }}
    
    QPushButton:hover {{
        background-color: {primary_variant_color};
    }}

"""

MODELS_TAB_STYLES = f"""
    QListWidget {{
        font-size: 14px;
        background-color: #333;
        color: white;
        border-radius: 5px;
        margin: 5px;
    }}
"""

LOCAL_MODEL_STYLES = f"""
    QWidget{{
        background-color: {surface_color};
        border-radius: 0px;
        border: 1px solid {surface3_color};
    }}
    QLabel {{
        font-size: 14px;
        color: {on_surface_color};
        border: none;
    }}
    
    QProgressBar {{
        border-radius: 2px;
        text-align: center;
        background-color: {surface2_color};
        border: none;
    }}
    
    QProgressBar::chunk {{
        background-color: {primary_color};
        width: 10px;
        border: none;
    }}
"""

SETTINGS_STYLES = f"""
    QPushButton {{
        background-color: {surface2_color};
        color: {on_surface_color};
        border-radius: 5px;
        border: 1px solid {surface3_color};
        padding: 8px;
    }}
    
    QPushButton:hover {{
        background-color: {surface3_color};
    }}
    
    QLineEdit{{
        padding: 8px;
    }}
    
"""

MODEL_WIDGET_STYLES = f"""
    QWidget {{
        background-color: {surface2_color};
        border-radius: 10px;
    }} 
    QLabel {{
        color: {on_surface_color};
        font-size: 14px;
    }}
    QPushButton {{
        background-color: {primary_color};
        color: {on_primary_color};
        font-size: 12px;
        border-radius: 5px;
        margin-top: 5px;
        border: none;
    }}
    QPushButton:disabled{{
        background-color: {surface3_color};
    }}
    QPushButton:hover {{
        background-color: {primary_lighter_color};
    }}
    QPushButton:pressed {{
        background-color: {primary_variant_color};
    }}
"""

CONFIGURATION_BAR_STYLES = f"""
    QVBoxLayout{{
        background-color: {surface_color};
    }}
"""

STYLESHEETS = f"""
    *{{
        font-family: "Inter", sans-serif;
        font-weight: 500;
        outline: none;
    }} 
    QMainWindow {{
        background-color: {background_color};
    }}
    QComboBox {{
        background-color: {surface_color};
        color: {on_surface_color};
        border: 1px solid {surface2_color};
        border-radius: 0px;
        padding: 5px;
    }}
    QComboBox::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 15px;
    }}
    QComboBox::hover {{
        background-color: {surface2_color};
    }}
    QComboBox::down-arrow {{
        image: url('assets/down_arrow_icon.png');
    }}
    QComboBox QAbstractItemView {{
        background: {surface_color};
        selection-background-color: {primary_lighter_color};
    }}

    QLabel {{
        color: {on_background_color};
        font-size: 14px;
    }}
    
    QLineEdit {{
        background-color: {surface2_color};
        color: {on_surface_color};
        border: 1px solid {surface3_color};
        border-radius: 5px;
        padding: 5px;
    }}
    QListView {{
        background: {surface_color};
        border: none;
        padding: 10px;
        font-weight: 600;
    }}
    
    QListView::item {{
        background: {surface2_color};
        color: {on_surface_color};
        padding: 0px 10px 0px 10px;
        border-radius: 0px;
        height: 20px;
    }}
    
    QListView::item:hover {{
        background: {surface3_color};
        color: {on_primary_color};
    }}
    
    QListView::item:selected {{
        background: {primary_color};
        color: {on_primary_color};
    }}
    
    QMenu {{
        background-color: {surface2_color}; 
        color: #dcdcdc;
        border: 1px solid {surface3_color};
    }}
    
    QMenu::item {{
        background-color: transparent;
        padding: 10px 20px;
        font-size: 13px;
    }}
    
    QMenu::item:selected {{
        background-color: {surface3_color};
        color: white;
    }}
    
    QMenu::icon {{
        left: 5px; 
    }}
    
    QMenu::separator {{
        height: 1px;
        background: #767676; 
        margin-left: 10px;
        margin-right: 10px;
    }}

    QGraphicsView {{
        color: white;
        background-color: {surface_color};
        border: 2px dashed {surface3_color};
        font-size: 16px;
    }}
    QMessageBox {{
        background-color: {surface_color};
        color: {on_surface_color};
        font-size: 14px;
    }}
    
    QMessageBox QPushButton {{
        background-color: {primary_color};
        color: {on_primary_color};
        border-radius: 5px;
        padding: 5px 10px;
        margin: 5px;
    }}
    
    QMessageBox QPushButton:hover {{
        background-color: {primary_lighter_color};
    }}
    
    QMessageBox QLabel {{
        color: {on_surface_color};
    }}
    
    ConfigurationBar {{
        background-color: {surface_color};
    }}

    QProgressBar {{
        border-radius: 1px; 
        background-color: {background_color}; 
        height: 1px;
    }}
    QProgressBar::chunk {{
        background-color: {primary_color}; 
        width: 20px;
    }}

    QScrollArea {{
        border: none;
    }}
    QScrollBar:vertical {{
        background: {surface_color};
        width: 10px;
        margin: 10px 0 10px 0;
        border: 1px solid {surface2_color};
    }}
    
    QScrollBar::handle:vertical {{
        background: {surface3_color};
        min-height: 20px;
        border-radius: 5px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background: {surface3_color};
    }}
    
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
        background: none;
        border: none;
    }}
    
    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
        background: none;
        width: 0px;
        height: 0px;
    }}
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        border: none;
        background: none;
        width: 0px;
        height: 0px;
    }}

    QScrollBar:horizontal {{
        background: {surface_color};
        height: 10px;
        margin: 0 10px 0 10px;
        border: 1px solid {surface2_color};
    }}
    
    QScrollBar::handle:horizontal {{
        background: {surface3_color};
        min-width: 20px;
        border-radius: 5px;
    }}
    
    QScrollBar::handle:horizontal:hover {{
        background: {surface3_color};
    }}
    
    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
        background: none;
        border: none;
    }}
    
    QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal {{
        background: none;
        width: 0px;
        height: 0px;
    }}
    
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        border: none;
        background: none;
        width: 0px;
        height: 0px;
    }}
"""


def hex_to_rgb(color):
    color = color.replace("#", "")
    rgb = []
    for i in (0, 2, 4):
        decimal = int(color[i : i + 2], 16)
        rgb.append(decimal)

    return tuple(rgb)
