from tkinter import messagebox
from src.vista.vista_base import VistaGestion, DialogFormulario, rellenar_treeview
from src.controlador.controlador_profesores import ControladorProfesores


class ProfesoresVista(VistaGestion):
    """Vista CRUD para la gestión del profesorado."""

    def __init__(self, parent):
        self._ctrl = ControladorProfesores()
        super().__init__(parent, "Profesores")

    def _columnas(self) -> list:
        return [
            ("id",           "ID",          50),
            ("nombre",       "Nombre",     140),
            ("apellidos",    "Apellidos",  180),
            ("dni",          "DNI",        110),
            ("departamento", "Departamento", 160),
            ("especialidad", "Especialidad", 160),
            ("email",        "Email",      180),
            ("telefono",     "Teléfono",   110),
        ]

    def _cargar_datos(self) -> None:
        profs = self._ctrl.obtener_todos()
        filas = [
            (p.id_profesor, p.nombre, p.apellidos, p.dni,
             p.departamento, p.especialidad, p.email, p.telefono)
            for p in profs
        ]
        rellenar_treeview(self._tree, filas)

    def _nuevo(self) -> None:
        dlg = self._crear_dialogo("Nuevo profesor")
        dlg.conectar_guardar(lambda: self._guardar_nuevo(dlg))

    def _editar(self) -> None:
        id_sel = self._obtener_id_seleccionado()
        if not id_sel:
            messagebox.showinfo("Sin selección", "Selecciona un profesor para editar", parent=self)
            return
        prof = self._ctrl.obtener_por_id(int(id_sel))
        if not prof:
            return
        dlg = self._crear_dialogo("Editar profesor", prof)
        dlg.conectar_guardar(lambda: self._guardar_edicion(dlg, int(id_sel)))

    def _eliminar(self) -> None:
        id_sel = self._obtener_id_seleccionado()
        if not id_sel:
            messagebox.showinfo("Sin selección", "Selecciona un profesor para eliminar", parent=self)
            return
        prof = self._ctrl.obtener_por_id(int(id_sel))
        if not prof:
            return
        if not self._confirmar_eliminacion(prof.nombre_completo()):
            return
        try:
            self._ctrl.eliminar(int(id_sel))
            self._cargar_datos()
        except Exception as e:
            messagebox.showerror("Error al eliminar", str(e), parent=self)

    def _guardar_nuevo(self, dlg: DialogFormulario) -> None:
        try:
            self._ctrl.crear(
                nombre=dlg.obtener_valor("nombre"),
                apellidos=dlg.obtener_valor("apellidos"),
                dni=dlg.obtener_valor("dni"),
                fecha_nacimiento=dlg.obtener_valor("fnac"),
                email=dlg.obtener_valor("email"),
                telefono=dlg.obtener_valor("telefono"),
                departamento=dlg.obtener_valor("departamento"),
                especialidad=dlg.obtener_valor("especialidad"),
            )
            dlg.destroy()
            self._cargar_datos()
        except (ValueError, Exception) as e:
            messagebox.showerror("Error", str(e), parent=dlg)

    def _guardar_edicion(self, dlg: DialogFormulario, id_prof: int) -> None:
        try:
            self._ctrl.actualizar(
                id_profesor=id_prof,
                nombre=dlg.obtener_valor("nombre"),
                apellidos=dlg.obtener_valor("apellidos"),
                dni=dlg.obtener_valor("dni"),
                fecha_nacimiento=dlg.obtener_valor("fnac"),
                email=dlg.obtener_valor("email"),
                telefono=dlg.obtener_valor("telefono"),
                departamento=dlg.obtener_valor("departamento"),
                especialidad=dlg.obtener_valor("especialidad"),
            )
            dlg.destroy()
            self._cargar_datos()
        except (ValueError, Exception) as e:
            messagebox.showerror("Error", str(e), parent=dlg)

    @staticmethod
    def _crear_dialogo(titulo: str, prof=None) -> DialogFormulario:
        dlg = DialogFormulario(None, titulo, ancho=460, alto=560)
        dlg.agregar_campo("nombre",       "Nombre *",         prof.nombre if prof else "")
        dlg.agregar_campo("apellidos",    "Apellidos *",      prof.apellidos if prof else "")
        dlg.agregar_campo("dni",          "DNI *",            prof.dni if prof else "")
        dlg.agregar_campo("departamento", "Departamento",     prof.departamento if prof else "")
        dlg.agregar_campo("especialidad", "Especialidad",     prof.especialidad if prof else "")
        dlg.agregar_campo("fnac",         "Fecha nacimiento (AAAA-MM-DD)", prof.fecha_nacimiento if prof else "")
        dlg.agregar_campo("email",        "Email",            prof.email if prof else "")
        dlg.agregar_campo("telefono",     "Teléfono",         prof.telefono if prof else "")
        return dlg
