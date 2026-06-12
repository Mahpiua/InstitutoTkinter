from tkinter import messagebox
from src.vista.vista_base import VistaGestion, DialogFormulario, rellenar_treeview
from src.controlador.controlador_asignaturas import ControladorAsignaturas


class AsignaturasVista(VistaGestion):
    """Vista CRUD para la gestión de las asignaturas."""

    def __init__(self, parent):
        self._ctrl = ControladorAsignaturas()
        super().__init__(parent, "Asignaturas")

    def _columnas(self) -> list:
        return [
            ("id",           "ID",           50),
            ("nombre",       "Nombre",      240),
            ("departamento", "Departamento", 280),
        ]

    def _cargar_datos(self) -> None:
        asigs = self._ctrl.obtener_todas()
        filas = [(a.id_asignatura, a.nombre, a.departamento) for a in asigs]
        rellenar_treeview(self._tree, filas)

    def _nuevo(self) -> None:
        dlg = self._crear_dialogo("Nueva asignatura")
        dlg.conectar_guardar(lambda: self._guardar_nuevo(dlg))

    def _editar(self) -> None:
        id_sel = self._obtener_id_seleccionado()
        if not id_sel:
            messagebox.showinfo("Sin selección", "Selecciona una asignatura para editar", parent=self)
            return
        asigs = self._ctrl.obtener_todas()
        asig = next((a for a in asigs if a.id_asignatura == int(id_sel)), None)
        if not asig:
            return
        dlg = self._crear_dialogo("Editar asignatura", asig)
        dlg.conectar_guardar(lambda: self._guardar_edicion(dlg, int(id_sel)))

    def _eliminar(self) -> None:
        id_sel = self._obtener_id_seleccionado()
        if not id_sel:
            messagebox.showinfo("Sin selección", "Selecciona una asignatura para eliminar", parent=self)
            return
        asigs = self._ctrl.obtener_todas()
        asig = next((a for a in asigs if a.id_asignatura == int(id_sel)), None)
        nombre = asig.nombre if asig else str(id_sel)
        if not self._confirmar_eliminacion(nombre):
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
                departamento=dlg.obtener_valor("departamento"),
            )
            dlg.destroy()
            self._cargar_datos()
        except (ValueError, Exception) as e:
            messagebox.showerror("Error", str(e), parent=dlg)

    def _guardar_edicion(self, dlg: DialogFormulario, id_asig: int) -> None:
        try:
            self._ctrl.actualizar(
                id_asig=id_asig,
                nombre=dlg.obtener_valor("nombre"),
                departamento=dlg.obtener_valor("departamento"),
            )
            dlg.destroy()
            self._cargar_datos()
        except (ValueError, Exception) as e:
            messagebox.showerror("Error", str(e), parent=dlg)

    @staticmethod
    def _crear_dialogo(titulo: str, asig=None) -> DialogFormulario:
        dlg = DialogFormulario(None, titulo, ancho=420, alto=300)
        dlg.agregar_campo("nombre",       "Nombre de la asignatura *", asig.nombre if asig else "")
        dlg.agregar_campo("departamento", "Departamento *",            asig.departamento if asig else "")
        return dlg
