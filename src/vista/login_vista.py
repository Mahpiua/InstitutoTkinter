import customtkinter as ctk
from tkinter import messagebox
from src.modelo import gestor_bd as bd


class LoginVista(ctk.CTk):
    """Pantalla de inicio de sesión."""

    def __init__(self):
        super().__init__()
        self.title("Instituto – Acceso")
        self.geometry("420x500")
        self.resizable(False, False)
        self._ventana_principal = None
        self._construir_ui()
        # Centrar en pantalla
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 420) // 2
        y = (self.winfo_screenheight() - 500) // 2
        self.geometry(f"420x500+{x}+{y}")

    # ── Construcción de la UI ─────────────────────────────────────────────────

    def _construir_ui(self) -> None:
        self.configure(fg_color="#0d1f12")

        # Logo / título
        ctk.CTkLabel(self, text="🏫", font=ctk.CTkFont(size=60)).pack(pady=(50, 0))
        ctk.CTkLabel(self, text="Instituto",
                     font=ctk.CTkFont(size=28, weight="bold"),
                     text_color="#e2e8f0").pack(pady=(8, 4))
        ctk.CTkLabel(self, text="Sistema de Gestión",
                     font=ctk.CTkFont(size=14),
                     text_color="#86efac").pack(pady=(0, 30))

        # Formulario
        marco = ctk.CTkFrame(self, fg_color="#122218", corner_radius=16)
        marco.pack(padx=40, fill="x")

        ctk.CTkLabel(marco, text="Usuario", anchor="w",
                     font=ctk.CTkFont(size=13),
                     text_color="#bbf7d0").pack(padx=20, pady=(20, 4), anchor="w")
        self._campo_usuario = ctk.CTkEntry(marco, placeholder_text="admin",
                                           height=40, corner_radius=8)
        self._campo_usuario.pack(padx=20, fill="x")

        ctk.CTkLabel(marco, text="Contraseña", anchor="w",
                     font=ctk.CTkFont(size=13),
                     text_color="#bbf7d0").pack(padx=20, pady=(12, 4), anchor="w")
        self._campo_password = ctk.CTkEntry(marco, placeholder_text="••••••••",
                                            show="•", height=40, corner_radius=8)
        self._campo_password.pack(padx=20, fill="x")
        self._campo_password.bind("<Return>", lambda _: self._iniciar_sesion())

        self._btn_login = ctk.CTkButton(marco, text="Iniciar sesión",
                                        height=42, corner_radius=8,
                                        font=ctk.CTkFont(size=14, weight="bold"),
                                        command=self._iniciar_sesion)
        self._btn_login.pack(padx=20, pady=20, fill="x")

        ctk.CTkLabel(self, text="Usuario: admin  |  Contraseña: admin123",
                     font=ctk.CTkFont(size=11), text_color="#4ade80").pack(pady=(16, 0))

    # ── Lógica ────────────────────────────────────────────────────────────────

    def _iniciar_sesion(self) -> None:
        usuario = self._campo_usuario.get().strip()
        password = self._campo_password.get().strip()
        if not usuario or not password:
            messagebox.showwarning("Campos vacíos", "Introduce usuario y contraseña",
                                   parent=self)
            return
        try:
            if bd.verificar_login(usuario, password):
                self._abrir_principal()
            else:
                messagebox.showerror("Acceso denegado",
                                     "Usuario o contraseña incorrectos", parent=self)
                self._campo_password.delete(0, "end")
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)

    def _abrir_principal(self) -> None:
        # Importación diferida para evitar ciclos
        from src.vista.main_vista import MainVista
        self.withdraw()
        self._ventana_principal = MainVista(self)
        self._ventana_principal.protocol("WM_DELETE_WINDOW", self._cerrar_todo)
        self._ventana_principal.mainloop()

    def _cerrar_todo(self) -> None:
        if self._ventana_principal:
            self._ventana_principal.destroy()
        self.destroy()
