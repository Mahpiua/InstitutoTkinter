from tkinter import messagebox
from src.vista.vista_base import VistaGestion, DialogFormulario, rellenar_treeview
from src.controlador.controlador_aulas import ControladorAulas


class AulasVista(VistaGestion):
    """Vista CRUD para la gestión de las aulas."""

    def __init__(self, parent):
        self._ctrl = ControladorAulas()
        super().__init__(parent, "Aulas")

    def _columnas(self) -> list:
        return [
            ("id",          "ID",          50),
            ("numero",      "Número",     120),
            ("capacidad",   "Capacidad",  100),
            ("descripcion", "Descripción", 340),
        ]

    def _cargar_datos(self) -> None:
        aulas = self._ctrl.obtener_todas()
        filas = [(a.id_aula, a.numero, a.capacidad, a.descripcion) for a in aulas]
        rellenar_treeview(self._tree, filas)

    def _nuevo(self) -> None:
        dlg = self._crear_dialogo("Nueva aula")
        dlg.conectar_guardar(lambda: self._guardar_nuevo(dlg))

    def _editar(self) -> None:
        id_sel = self._obtener_id_seleccionado()
        if not id_sel:
            messagebox.showinfo("Sin selección", "Selecciona un aula para editar", parent=self)
            return
        aulas = self._ctrl.obtener_todas()
        aula = next((a for a in aulas if a.id_aula == int(id_sel)), None)
        if not aula:
            return
        dlg = self._crear_dialogo("Editar aula", aula)
        dlg.conectar_guardar(lambda: self._guardar_edicion(dlg, int(id_sel)))

    def _eliminar(self) -> None:
        id_sel = self._obtener_id_seleccionado()
        if not id_sel:
            messagebox.showinfo("Sin selección", "Selecciona un aula para eliminar", parent=self)
            return
        aulas = self._ctrl.obtener_todas()
        aula = next((a for a in aulas if a.id_aula == int(id_sel)), None)
        nombre = aula.numero if aula else str(id_sel)
        if not self._confirmar_eliminacion(f"Aula {nombre}"):
            return
        try:
            self._ctrl.eliminar(int(id_sel))
            self._cargar_datos()
        except Exception as e:
            messagebox.showerror("Error al eliminar", str(e), parent=self)

    def _guardar_nuevo(self, dlg: DialogFormulario) -> None:
        try:
            self._ctrl.crear(
                numero=dlg.obtener_valor("numero"),
                capacidad=dlg.obtener_valor("capacidad"),
                descripcion=dlg.obtener_valor("descripcion"),
            )
            dlg.destroy()
            self._cargar_datos()
        except (ValueError, Exception) as e:
            messagebox.showerror("Error", str(e), parent=dlg)

    def _guardar_edicion(self, dlg: DialogFormulario, id_aula: int) -> None:
        try:
            self._ctrl.actualizar(
                id_aula=id_aula,
                numero=dlg.obtener_valor("numero"),
                capacidad=dlg.obtener_valor("capacidad"),
                descripcion=dlg.obtener_valor("descripcion"),
            )
            dlg.destroy()
            self._cargar_datos()
        except (ValueError, Exception) as e:
            messagebox.showerror("Error", str(e), parent=dlg)

    @staticmethod
    def _crear_dialogo(titulo: str, aula=None) -> DialogFormulario:
        dlg = DialogFormulario(None, titulo, ancho=420, alto=360)
        dlg.agregar_campo("numero",      "Número de aula *",   aula.numero if aula else "")
        dlg.agregar_campo("capacidad",   "Capacidad *",        aula.capacidad if aula else "30")
        dlg.agregar_campo("descripcion", "Descripción",        aula.descripcion if aula else "")
        return dlg
