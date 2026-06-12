import customtkinter as ctk
from tkinter import messagebox, ttk
from src.vista.vista_base import VistaGestion, rellenar_treeview, crear_treeview
from src.controlador.controlador_matriculas import ControladorMatriculas
from src.modelo import gestor_bd as bd


class MatriculasVista(VistaGestion):
    """Vista para gestionar las matrículas de los alumnos."""

    def __init__(self, parent):
        self._ctrl = ControladorMatriculas()
        super().__init__(parent, "Matrículas")

    def _columnas(self) -> list:
        return [
            ("id",          "ID",          50),
            ("alumno",      "Alumno",     220),
            ("expediente",  "Expediente", 120),
            ("anio",        "Año Acad.",  110),
            ("fecha",       "Fecha matrícula", 130),
        ]

    def _cargar_datos(self) -> None:
        matriculas = self._ctrl.obtener_todas()
        filas = [
            (m.id_matricula, m.nombre_alumno, m.numero_expediente,
             m.anio_academico, m.fecha_matricula)
            for m in matriculas
        ]
        rellenar_treeview(self._tree, filas)

    def _nuevo(self) -> None:
        NuevaMatriculaDialog(self, self._ctrl, callback=self._cargar_datos)

    def _editar(self) -> None:
        messagebox.showinfo("Información",
                            "Para modificar una matrícula, elimínala y créala de nuevo.",
                            parent=self)

    def _eliminar(self) -> None:
        id_sel = self._obtener_id_seleccionado()
        if not id_sel:
            messagebox.showinfo("Sin selección", "Selecciona una matrícula para eliminar",
                                parent=self)
            return
        if not self._confirmar_eliminacion(f"matrícula ID {id_sel}"):
            return
        try:
            self._ctrl.eliminar(int(id_sel))
            self._cargar_datos()
        except Exception as e:
            messagebox.showerror("Error al eliminar", str(e), parent=self)


class NuevaMatriculaDialog(ctk.CTkToplevel):
    """Diálogo para crear una nueva matrícula con selección de clases."""

    def __init__(self, parent, ctrl: ControladorMatriculas, callback):
        super().__init__(parent)
        self.title("Nueva Matrícula")
        self.geometry("600x600")
        self.resizable(False, False)
        self.grab_set()
        self.configure(fg_color="#0d1f12")
        self._ctrl = ctrl
        self._callback = callback
        self._construir_ui()
        self._centrar()

    def _construir_ui(self) -> None:
        ctk.CTkLabel(self, text="Nueva Matrícula",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="#e2e8f0").pack(pady=(16, 8))

        scroll = ctk.CTkScrollableFrame(self, fg_color="#122218", corner_radius=12)
        scroll.pack(fill="both", expand=True, padx=20, pady=8)

        # Alumno
        ctk.CTkLabel(scroll, text="Alumno *", anchor="w",
                     text_color="#86efac").pack(anchor="w", padx=8, pady=(8, 2))
        alumnos = bd.obtener_alumnos()
        self._opciones_alumnos = {
            f"[{a['id']}] {a['nombre']} {a['apellidos']}": a['id'] for a in alumnos
        }
        self._combo_alumno = ctk.CTkComboBox(
            scroll, values=list(self._opciones_alumnos.keys()), height=36)
        self._combo_alumno.pack(fill="x", padx=8, pady=(0, 8))

        # Año académico
        ctk.CTkLabel(scroll, text="Año académico *", anchor="w",
                     text_color="#86efac").pack(anchor="w", padx=8, pady=(4, 2))
        self._entry_anio = ctk.CTkEntry(scroll, placeholder_text="2025-2026", height=36)
        self._entry_anio.pack(fill="x", padx=8, pady=(0, 8))

        # Clases disponibles (multi-selección con Treeview)
        ctk.CTkLabel(scroll, text="Clases a matricular (Ctrl+clic para varios) *",
                     anchor="w", text_color="#86efac").pack(anchor="w", padx=8, pady=(4, 2))

        marco_tree = ctk.CTkFrame(scroll, fg_color="#1a2e1f", corner_radius=8)
        marco_tree.pack(fill="x", padx=8, pady=(0, 8))

        self._tree_clases = ttk.Treeview(
            marco_tree,
            columns=("id", "asignatura", "grupo", "anio", "profesor"),
            show="headings",
            style="Instituto.Treeview",
            selectmode="extended",
            height=8,
        )
        for col, texto, ancho in [
            ("id", "ID", 40), ("asignatura", "Asignatura", 180),
            ("grupo", "Grupo", 60), ("anio", "Año", 90), ("profesor", "Profesor", 160)
        ]:
            self._tree_clases.heading(col, text=texto)
            self._tree_clases.column(col, width=ancho)

        clases = bd.obtener_clases()
        for c in clases:
            self._tree_clases.insert("", "end", values=(
                c["id"], c["nombre_asignatura"], c["grupo"],
                c["anio_academico"], c["nombre_profesor"]
            ))
        self._tree_clases.pack(fill="x", padx=4, pady=4)

        # Botones
        frame_btns = ctk.CTkFrame(self, fg_color="transparent")
        frame_btns.pack(pady=(0, 16))
        ctk.CTkButton(frame_btns, text="Cancelar", width=120, height=38,
                      fg_color="#1e4d2e", hover_color="#2d6a3f",
                      command=self.destroy).pack(side="left", padx=8)
        ctk.CTkButton(frame_btns, text="Guardar", width=120, height=38,
                      fg_color="#15803d", hover_color="#16a34a",
                      command=self._guardar).pack(side="left", padx=8)

    def _guardar(self) -> None:
        alumno_texto = self._combo_alumno.get()
        id_alumno = self._opciones_alumnos.get(alumno_texto)
        anio = self._entry_anio.get().strip()
        ids_clases = [
            int(self._tree_clases.item(sel)["values"][0])
            for sel in self._tree_clases.selection()
        ]
        if not id_alumno:
            messagebox.showwarning("Validación", "Selecciona un alumno", parent=self)
            return
        if not anio:
            messagebox.showwarning("Validación", "Introduce el año académico", parent=self)
            return
        if not ids_clases:
            messagebox.showwarning("Validación", "Selecciona al menos una clase", parent=self)
            return
        try:
            self._ctrl.crear(id_alumno, anio, ids_clases)
            self.destroy()
            self._callback()
        except (ValueError, Exception) as e:
            messagebox.showerror("Error", str(e), parent=self)

    def _centrar(self) -> None:
        self.update_idletasks()
        pw = self.master.winfo_rootx()
        ph = self.master.winfo_rooty()
        pw2 = self.master.winfo_width()
        ph2 = self.master.winfo_height()
        x = pw + (pw2 - 600) // 2
        y = ph + (ph2 - 600) // 2
        self.geometry(f"600x600+{x}+{y}")
