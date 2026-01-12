import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS # Para el exe. MEIPASS es una variable donde PyInstaller guarda la ruta temporal
    except:
        base_path = os. path.abspath(".") #para el desarrollo en .py. Excepp porque si no exite la variable estamos en desarrollo.
    return os.path.join(base_path, relative_path)