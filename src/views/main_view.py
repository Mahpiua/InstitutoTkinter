import customtkinter as ctk
from config import *


class MainView(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry(WINDOW_SIZE)
        self.iconbitmap(ICON_PATH)
        self.resizable(RESIZEABLE_W, RESIZEABLE_H)

        ctk.CTkLabel(self, text="HOLA MUNDO").pack()