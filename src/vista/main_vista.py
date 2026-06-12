import customtkinter as ctk


class MainVista(ctk.CTkToplevel):
    """Ventana principal con barra lateral de navegación."""

    # Color de fondo de la barra lateral
    _COLOR_SIDEBAR = "#122218"
    # Color activo del botón seleccionado
    _COLOR_ACTIVO = "#166534"

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Instituto – Gestión")
        self.geometry("1280x720")
        self.minsize(900, 600)
        self._vista_actual = None
        self._botones_nav: dict = {}
        self._construir_ui()
        self._mostrar_vista("alumnos")

    # ── Construcción de la UI ─────────────────────────────────────────────────

    def _construir_ui(self) -> None:
        self.configure(fg_color="#0d1f12")

        # Contenedor principal: sidebar | contenido
        self._sidebar = ctk.CTkFrame(self, width=210, corner_radius=0,
                                     fg_color=self._COLOR_SIDEBAR)
        self._sidebar.pack(side="left", fill="y")
        self._sidebar.pack_propagate(False)

        self._area_contenido = ctk.CTkFrame(self, corner_radius=0, fg_color="#0d1f12")
        self._area_contenido.pack(side="left", fill="both", expand=True)

        self._construir_sidebar()

    def _construir_sidebar(self) -> None:
        # Título
        ctk.CTkLabel(self._sidebar, text="🏫 Instituto",
                     font=ctk.CTkFont(size=17, weight="bold"),
                     text_color="#e2e8f0").pack(pady=(24, 4))
        ctk.CTkLabel(self._sidebar, text="Panel de Gestión",
                     font=ctk.CTkFont(size=11), text_color="#4ade80").pack(pady=(0, 24))

        ctk.CTkFrame(self._sidebar, height=1, fg_color="#1e4d2e").pack(fill="x", padx=16)

        # Secciones del menú
        secciones = [
            ("Alumnos",     "alumnos"),
            ("Profesores",   "profesores"),
            ("Dirección",    "direccion"),
            ("Aulas",        "aulas"),
            ("Asignaturas",  "asignaturas"),
            ("Clases",       "clases"),
            ("Materiales",   "materiales"),
            ("Matrículas",   "matriculas"),
            ("Calificaciones", "calificaciones"),
        ]

        frame_nav = ctk.CTkScrollableFrame(self._sidebar, fg_color="transparent")
        frame_nav.pack(fill="both", expand=True, padx=8, pady=8)

        for texto, clave in secciones:
            btn = ctk.CTkButton(
                frame_nav,
                text=texto,
                anchor="w",
                height=40,
                corner_radius=8,
                fg_color="transparent",
                hover_color="#1a3d28",
                text_color="#bbf7d0",
                font=ctk.CTkFont(size=13),
                command=lambda c=clave: self._mostrar_vista(c),
            )
            btn.pack(fill="x", pady=2)
            self._botones_nav[clave] = btn

        # Botón cerrar sesión al fondo
        ctk.CTkFrame(self._sidebar, height=1, fg_color="#1e4d2e").pack(
            fill="x", padx=16, side="bottom", pady=(0, 8))
        ctk.CTkButton(
            self._sidebar,
            text="Cerrar aplicación",
            anchor="w",
            height=40,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#7f1d1d",
            text_color="#f87171",
            font=ctk.CTkFont(size=13),
            command=self._cerrar,
        ).pack(side="bottom", fill="x", padx=8, pady=(0, 8))

    # ── Navegación ────────────────────────────────────────────────────────────

    def _mostrar_vista(self, clave: str) -> None:
        """Destruye la vista actual y carga la nueva."""
        # Resaltar botón activo
        for k, btn in self._botones_nav.items():
            btn.configure(fg_color=self._COLOR_ACTIVO if k == clave else "transparent")

        if self._vista_actual:
            self._vista_actual.destroy()

        vista_clase = self._obtener_clase_vista(clave)
        if vista_clase:
            self._vista_actual = vista_clase(self._area_contenido)
            self._vista_actual.pack(fill="both", expand=True)

    @staticmethod
    def _obtener_clase_vista(clave: str):
        """Importación diferida de cada vista para evitar ciclos y mejorar el arranque."""
        if clave == "alumnos":
            from src.vista.alumnos_vista import AlumnosVista
            return AlumnosVista
        if clave == "profesores":
            from src.vista.profesores_vista import ProfesoresVista
            return ProfesoresVista
        if clave == "direccion":
            from src.vista.direccion_vista import DireccionVista
            return DireccionVista
        if clave == "aulas":
            from src.vista.aulas_vista import AulasVista
            return AulasVista
        if clave == "asignaturas":
            from src.vista.asignaturas_vista import AsignaturasVista
            return AsignaturasVista
        if clave == "clases":
            from src.vista.clases_vista import ClasesVista
            return ClasesVista
        if clave == "materiales":
            from src.vista.materiales_vista import MaterialesVista
            return MaterialesVista
        if clave == "matriculas":
            from src.vista.matriculas_vista import MatriculasVista
            return MatriculasVista
        if clave == "calificaciones":
            from src.vista.calificaciones_vista import CalificacionesVista
            return CalificacionesVista
        return None

    def _cerrar(self) -> None:
        self.destroy()
