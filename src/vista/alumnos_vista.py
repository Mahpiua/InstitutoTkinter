from tkinter import messagebox
from src.vista.vista_base import VistaGestion, DialogFormulario, rellenar_treeview
from src.controlador.controlador_alumnos import ControladorAlumnos


class AlumnosVista(VistaGestion):
    """Vista CRUD para la gestión del alumnado."""

    def __init__(self, parent):
        self._ctrl = ControladorAlumnos()
        super().__init__(parent, "Alumnos")

    # ── Definición de columnas ─────────────────────────────────────────────────

    def _columnas(self) -> list:
        return [
            ("id",          "ID",           50),
            ("expediente",  "Expediente",  120),
            ("nombre",      "Nombre",      140),
            ("apellidos",   "Apellidos",   180),
            ("dni",         "DNI",         110),
            ("fnac",        "F. Nacimiento", 120),
            ("email",       "Email",       180),
            ("telefono",    "Teléfono",    110),
        ]

    # ── Carga de datos ────────────────────────────────────────────────────────

    def _cargar_datos(self) -> None:
        alumnos = self._ctrl.obtener_todos()
        filas = [
            (a.id_alumno, a.numero_expediente, a.nombre, a.apellidos,
             a.dni, a.fecha_nacimiento, a.email, a.telefono)
            for a in alumnos
        ]
        rellenar_treeview(self._tree, filas)

    # ── Acciones CRUD ─────────────────────────────────────────────────────────

    def _nuevo(self) -> None:
        dlg = self._crear_dialogo("Nuevo alumno")
        dlg.conectar_guardar(lambda: self._guardar_nuevo(dlg))

    def _editar(self) -> None:
        id_sel = self._obtener_id_seleccionado()
        if not id_sel:
            messagebox.showinfo("Sin selección", "Selecciona un alumno para editar", parent=self)
            return
        alumno = self._ctrl.obtener_por_id(int(id_sel))
        if not alumno:
            return
        dlg = self._crear_dialogo("Editar alumno", alumno)
        dlg.conectar_guardar(lambda: self._guardar_edicion(dlg, int(id_sel)))

    def _eliminar(self) -> None:
        id_sel = self._obtener_id_seleccionado()
        if not id_sel:
            messagebox.showinfo("Sin selección", "Selecciona un alumno para eliminar", parent=self)
            return
        alumno = self._ctrl.obtener_por_id(int(id_sel))
        if not alumno:
            return
        if not self._confirmar_eliminacion(alumno.nombre_completo()):
            return
        try:
            self._ctrl.eliminar(int(id_sel))
            self._cargar_datos()
        except Exception as e:
            messagebox.showerror("Error al eliminar", str(e), parent=self)

    # ── Lógica de guardado ────────────────────────────────────────────────────

    def _guardar_nuevo(self, dlg: DialogFormulario) -> None:
        try:
            self._ctrl.crear(
                nombre=dlg.obtener_valor("nombre"),
                apellidos=dlg.obtener_valor("apellidos"),
                dni=dlg.obtener_valor("dni"),
                fecha_nacimiento=dlg.obtener_valor("fnac"),
                email=dlg.obtener_valor("email"),
                telefono=dlg.obtener_valor("telefono"),
                numero_expediente=dlg.obtener_valor("expediente"),
            )
            dlg.destroy()
            self._cargar_datos()
        except (ValueError, Exception) as e:
            messagebox.showerror("Error", str(e), parent=dlg)

    def _guardar_edicion(self, dlg: DialogFormulario, id_alumno: int) -> None:
        try:
            self._ctrl.actualizar(
                id_alumno=id_alumno,
                nombre=dlg.obtener_valor("nombre"),
                apellidos=dlg.obtener_valor("apellidos"),
                dni=dlg.obtener_valor("dni"),
                fecha_nacimiento=dlg.obtener_valor("fnac"),
                email=dlg.obtener_valor("email"),
                telefono=dlg.obtener_valor("telefono"),
                numero_expediente=dlg.obtener_valor("expediente"),
            )
            dlg.destroy()
            self._cargar_datos()
        except (ValueError, Exception) as e:
            messagebox.showerror("Error", str(e), parent=dlg)

    # ── Construcción del diálogo ──────────────────────────────────────────────

    @staticmethod
    def _crear_dialogo(titulo: str, alumno=None) -> DialogFormulario:
        dlg = DialogFormulario(None, titulo, ancho=460, alto=540)
        dlg.agregar_campo("nombre",     "Nombre *",             alumno.nombre if alumno else "")
        dlg.agregar_campo("apellidos",  "Apellidos *",          alumno.apellidos if alumno else "")
        dlg.agregar_campo("dni",        "DNI *",                alumno.dni if alumno else "")
        dlg.agregar_campo("expediente", "Nº Expediente *",      alumno.numero_expediente if alumno else "")
        dlg.agregar_campo("fnac",       "Fecha nacimiento (AAAA-MM-DD)", alumno.fecha_nacimiento if alumno else "")
        dlg.agregar_campo("email",      "Email",                alumno.email if alumno else "")
        dlg.agregar_campo("telefono",   "Teléfono",             alumno.telefono if alumno else "")
        return dlg
