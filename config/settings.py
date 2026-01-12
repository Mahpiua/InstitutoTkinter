"""
Configuración de la aplicación
"""
APP_NAME = "App_MVC_Paquetes_Python"
WINDOW_SIZE = "400x300"
APP_VERSION = "1.0.0"
RESIZEABLE_W = False
RESIZEABLE_H = False


# ruta para Configurar icono de la ventana (se configura en el main)
from resources import resource_path
try:
    ICON_PATH = resource_path("resources/icons/icono_exe.ico")
except Exception as e:
    print(f"Error al cargar icono:  {e}")