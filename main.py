import customtkinter as ctk
from src.modelo.gestor_bd import crear_bd, iniciar_carga, obtener_aulas
from src.vista.login_vista import LoginVista

# Tema oscuro con acentos verdes
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

if __name__ == "__main__":
    crear_bd()
    iniciar_carga()

    # Primera vez: cargar datos de ejemplo si la BD está vacía
    if not obtener_aulas():
        from datos_iniciales import cargar_datos_iniciales
        cargar_datos_iniciales()

    app = LoginVista()
    app.mainloop()
