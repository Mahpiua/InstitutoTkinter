import customtkinter as ctk
from tkinter import messagebox, filedialog, ttk
from src.controlador.controlador_calificaciones import ControladorCalificaciones
from src.modelo import gestor_bd as bd


class CalificacionesVista(ctk.CTkFrame):
    """
    Vista para consultar y editar calificaciones.
    Muestra una cuadrícula con todas las asignaturas de un alumno en un año.
    Permite navegar entre alumnos, editar notas y exportar a CSV.
    """

    def __init__(self, parent):
        super().__init__(parent, fg_color="#0d1f12", corner_radius=0)
        self._ctrl = ControladorCalificaciones()
        self._alumnos: list = []          # lista de dicts con datos de alumnos
        self._indice_alumno: int = 0
        self._convocatorias: list = []    # lista de dicts {id, nombre}
        self._entradas_notas: dict = {}   # (id_clase, id_conv) → CTkEntry
        self._construir_ui()
        self._cargar_alumnos()

    # ── Construcción de la UI ─────────────────────────────────────────────────

    def _construir_ui(self) -> None:
        # Cabecera
        cab = ctk.CTkFrame(self, fg_color="#132a1a", height=64, corner_radius=0)
        cab.pack(fill="x")
        cab.pack_propagate(False)
        ctk.CTkLabel(cab, text="🎓  Calificaciones",
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="#e2e8f0").pack(side="left", padx=24)

        # Barra de controles
        barra = ctk.CTkFrame(self, fg_color="#1a2e20", height=56, corner_radius=0)
        barra.pack(fill="x")
        barra.pack_propagate(False)

        # Navegación alumno
        ctk.CTkButton(barra, text="◀", width=40, height=36, corner_radius=8,
                      command=self._anterior).pack(side="left", padx=(16, 4), pady=10)

        self._lbl_alumno = ctk.CTkLabel(barra, text="—",
                                         font=ctk.CTkFont(size=14, weight="bold"),
                                         text_color="#e2e8f0", width=280, anchor="w")
        self._lbl_alumno.pack(side="left", padx=4)

        ctk.CTkButton(barra, text="▶", width=40, height=36, corner_radius=8,
                      command=self._siguiente).pack(side="left", padx=(4, 16), pady=10)

        # Separador
        ctk.CTkFrame(barra, width=2, fg_color="#1e4d2e").pack(side="left", fill="y", pady=8)

        # Selector de año
        ctk.CTkLabel(barra, text="Año:", text_color="#86efac",
                     font=ctk.CTkFont(size=13)).pack(side="left", padx=(12, 4))
        self._combo_anio = ctk.CTkComboBox(barra, width=140, height=36,
                                            values=[],
                                            command=self._al_cambiar_anio)
        self._combo_anio.pack(side="left", padx=(0, 16))

        # Botones de acción
        ctk.CTkButton(barra, text="💾 Guardar notas", height=36, corner_radius=8,
                      command=self._guardar_notas).pack(side="left", padx=4)

        ctk.CTkButton(barra, text="📤 Exportar asignatura", height=36, corner_radius=8,
                      fg_color="#166534", hover_color="#15803d",
                      command=self._exportar).pack(side="left", padx=4)

        # Área de la cuadrícula (scrollable)
        self._area_grid = ctk.CTkScrollableFrame(self, fg_color="#0d1f12", corner_radius=0)
        self._area_grid.pack(fill="both", expand=True, padx=16, pady=16)

        self._lbl_sin_datos = ctk.CTkLabel(
            self._area_grid,
            text="Selecciona un alumno con matrícula para ver sus calificaciones.",
            text_color="#4ade80", font=ctk.CTkFont(size=13))
        self._lbl_sin_datos.pack(pady=40)

    # ── Carga de datos ────────────────────────────────────────────────────────

    def _cargar_alumnos(self) -> None:
        """Carga la lista de alumnos y muestra el primero."""
        self._alumnos = bd.obtener_alumnos()
        self._convocatorias = self._ctrl.obtener_convocatorias()
        self._indice_alumno = 0
        if self._alumnos:
            self._mostrar_alumno()

    def _mostrar_alumno(self) -> None:
        """Actualiza la cabecera y los años disponibles para el alumno actual."""
        if not self._alumnos:
            self._lbl_alumno.configure(text="No hay alumnos registrados")
            return
        a = self._alumnos[self._indice_alumno]
        self._lbl_alumno.configure(
            text=f"{a['apellidos']}, {a['nombre']}  (Exp: {a['numero_expediente']})"
        )
        # Obtener años académicos de este alumno
        anios = self._ctrl.obtener_anios_alumno(a["id"])
        self._combo_anio.configure(values=anios)
        if anios:
            self._combo_anio.set(anios[0])
            self._refrescar_grid()
        else:
            self._combo_anio.set("")
            self._limpiar_grid()
            self._lbl_sin_datos.configure(
                text="Este alumno no tiene matrículas en ningún año académico.")
            self._lbl_sin_datos.pack(pady=40)

    def _refrescar_grid(self) -> None:
        """Redibuja la cuadrícula de calificaciones."""
        self._limpiar_grid()
        if not self._alumnos:
            return
        a = self._alumnos[self._indice_alumno]
        anio = self._combo_anio.get()
        if not anio:
            return

        filas = self._ctrl.obtener_grid(a["id"], anio)
        if not filas:
            self._lbl_sin_datos.configure(
                text=f"No hay asignaturas matriculadas en {anio}.")
            self._lbl_sin_datos.pack(pady=40)
            return

        self._entradas_notas = {}
        nombres_conv = [c["nombre"] for c in self._convocatorias]

        # Cabecera de la tabla
        cab = ctk.CTkFrame(self._area_grid, fg_color="#1a3324", corner_radius=8)
        cab.pack(fill="x", pady=(0, 4))
        ctk.CTkLabel(cab, text="Asignatura", width=220, anchor="w",
                     font=ctk.CTkFont(weight="bold"),
                     text_color="#86efac").pack(side="left", padx=12, pady=8)
        for conv in self._convocatorias:
            ctk.CTkLabel(cab, text=conv["nombre"], width=140, anchor="center",
                         font=ctk.CTkFont(weight="bold"),
                         text_color="#86efac").pack(side="left", padx=4)

        # Filas de asignaturas
        for i, fila in enumerate(filas):
            color = "#1a2e1f" if i % 2 == 0 else "#203828"
            fila_frame = ctk.CTkFrame(self._area_grid, fg_color=color, corner_radius=6)
            fila_frame.pack(fill="x", pady=1)

            ctk.CTkLabel(fila_frame, text=fila["asignatura"], width=220, anchor="w",
                         text_color="#e2e8f0").pack(side="left", padx=12, pady=6)

            for conv in self._convocatorias:
                nota_val = fila.get(conv["nombre"], "")
                entry = ctk.CTkEntry(fila_frame, width=130, height=32,
                                     corner_radius=6,
                                     placeholder_text="0-10")
                if nota_val != "":
                    entry.insert(0, str(nota_val))
                entry.pack(side="left", padx=4, pady=4)
                self._entradas_notas[(fila["id_clase"], fila["id_matricula"], conv["id"])] = entry

    def _limpiar_grid(self) -> None:
        """Destruye todos los widgets del área de la cuadrícula."""
        for widget in self._area_grid.winfo_children():
            if widget is not self._lbl_sin_datos:
                widget.destroy()
        self._lbl_sin_datos.pack_forget()
        self._entradas_notas = {}

    # ── Acciones ──────────────────────────────────────────────────────────────

    def _anterior(self) -> None:
        if not self._alumnos:
            return
        self._indice_alumno = (self._indice_alumno - 1) % len(self._alumnos)
        self._mostrar_alumno()

    def _siguiente(self) -> None:
        if not self._alumnos:
            return
        self._indice_alumno = (self._indice_alumno + 1) % len(self._alumnos)
        self._mostrar_alumno()

    def _al_cambiar_anio(self, valor: str) -> None:
        self._refrescar_grid()

    def _guardar_notas(self) -> None:
        """Guarda todas las notas editadas en la cuadrícula."""
        errores = []
        for (id_clase, id_matricula, id_conv), entry in self._entradas_notas.items():
            nota_txt = entry.get().strip()
            if not nota_txt:
                continue
            try:
                self._ctrl.guardar_nota(id_matricula, id_clase, id_conv, nota_txt)
            except ValueError as e:
                errores.append(str(e))

        if errores:
            messagebox.showerror("Errores al guardar",
                                  "\n".join(errores), parent=self)
        else:
            messagebox.showinfo("Guardado", "Notas guardadas correctamente.", parent=self)
        self._refrescar_grid()

    def _exportar(self) -> None:
        """Exporta las calificaciones de una asignatura a CSV."""
        asigs = bd.obtener_asignaturas()
        if not asigs:
            messagebox.showinfo("Sin datos", "No hay asignaturas registradas.", parent=self)
            return

        # Diálogo de selección de asignatura y año
        ExportarDialog(self, asigs, self._ctrl)

    def _actualizar(self) -> None:
        self._refrescar_grid()


# ─────────────────────────────────────────────────────────────────────────────
#  Diálogo de exportación
# ─────────────────────────────────────────────────────────────────────────────

class ExportarDialog(ctk.CTkToplevel):
    """Diálogo para seleccionar asignatura, año y ruta de exportación."""

    def __init__(self, parent, asigs: list, ctrl: ControladorCalificaciones):
        super().__init__(parent)
        self.title("Exportar Calificaciones")
        self.geometry("460x320")
        self.resizable(False, False)
        self.grab_set()
        self.configure(fg_color="#0d1f12")
        self._asigs = asigs
        self._ctrl = ctrl
        self._construir_ui()
        self._centrar(parent)

    def _construir_ui(self) -> None:
        ctk.CTkLabel(self, text="Exportar Calificaciones a CSV",
                     font=ctk.CTkFont(size=15, weight="bold"),
                     text_color="#e2e8f0").pack(pady=(20, 8))

        scroll = ctk.CTkScrollableFrame(self, fg_color="#122218", corner_radius=12)
        scroll.pack(fill="both", expand=True, padx=20, pady=8)

        # Asignatura
        ctk.CTkLabel(scroll, text="Asignatura *", anchor="w",
                     text_color="#86efac").pack(anchor="w", padx=8, pady=(8, 2))
        opciones = [f"[{a['id']}] {a['nombre']}" for a in self._asigs]
        self._combo_asig = ctk.CTkComboBox(scroll, values=opciones, height=36)
        self._combo_asig.pack(fill="x", padx=8, pady=(0, 8))

        # Año académico
        ctk.CTkLabel(scroll, text="Año académico *", anchor="w",
                     text_color="#86efac").pack(anchor="w", padx=8, pady=(4, 2))
        self._entry_anio = ctk.CTkEntry(scroll, placeholder_text="2025-2026", height=36)
        self._entry_anio.pack(fill="x", padx=8, pady=(0, 8))

        # Botones
        frame_btns = ctk.CTkFrame(self, fg_color="transparent")
        frame_btns.pack(pady=(0, 16))
        ctk.CTkButton(frame_btns, text="Cancelar", width=120, height=38,
                      fg_color="#1e4d2e", hover_color="#2d6a3f",
                      command=self.destroy).pack(side="left", padx=8)
        ctk.CTkButton(frame_btns, text="Exportar", width=120, height=38,
                      fg_color="#15803d", hover_color="#16a34a",
                      command=self._exportar).pack(side="left", padx=8)

    def _exportar(self) -> None:
        asig_txt = self._combo_asig.get()
        anio = self._entry_anio.get().strip()
        if not asig_txt or not anio:
            messagebox.showwarning("Campos vacíos",
                                    "Selecciona asignatura e introduce el año.", parent=self)
            return
        try:
            id_asig = int(asig_txt.split("]")[0].replace("[", "").strip())
        except Exception:
            messagebox.showerror("Error", "Asignatura no reconocida.", parent=self)
            return

        ruta = filedialog.asksaveasfilename(
            title="Guardar calificaciones",
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv"), ("Todos", "*.*")],
            initialfile=f"calificaciones_{anio}.csv",
            parent=self,
        )
        if not ruta:
            return
        try:
            n = self._ctrl.exportar_a_csv(id_asig, anio, ruta)
            messagebox.showinfo("Exportación completada",
                                 f"Se exportaron {n} registros a:\n{ruta}", parent=self)
            self.destroy()
        except (ValueError, Exception) as e:
            messagebox.showerror("Error al exportar", str(e), parent=self)

    def _centrar(self, parent) -> None:
        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() - 460) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - 320) // 2
        self.geometry(f"460x320+{x}+{y}")
