from tkinter import messagebox
from src.vista.vista_base import VistaGestion, DialogFormulario, rellenar_treeview
from src.controlador.controlador_clases import ControladorClases
from src.modelo import gestor_bd as bd


class ClasesVista(VistaGestion):
    """Vista CRUD para la gestión de las clases."""

    def __init__(self, parent):
        self._ctrl = ControladorClases()
        super().__init__(parent, "Clases")

    def _columnas(self) -> list:
        return [
            ("id",          "ID",           50),
            ("asignatura",  "Asignatura",  200),
            ("grupo",       "Grupo",        70),
            ("anio",        "Año Acad.",   110),
            ("profesor",    "Profesor",    200),
            ("aula",        "Aula",        100),
        ]

    def _cargar_datos(self) -> None:
        clases = self._ctrl.obtener_todas()
        filas = [
            (c.id_clase, c.nombre_asignatura, c.grupo, c.anio_academico,
             c.nombre_profesor, c.numero_aula)
            for c in clases
        ]
        rellenar_treeview(self._tree, filas)

    def _nuevo(self) -> None:
        dlg = self._crear_dialogo("Nueva clase")
        dlg.conectar_guardar(lambda: self._guardar_nuevo(dlg))

    def _editar(self) -> None:
        id_sel = self._obtener_id_seleccionado()
        if not id_sel:
            messagebox.showinfo("Sin selección", "Selecciona una clase para editar", parent=self)
            return
        clases = self._ctrl.obtener_todas()
        clase = next((c for c in clases if c.id_clase == int(id_sel)), None)
        if not clase:
            return
        dlg = self._crear_dialogo("Editar clase", clase)
        dlg.conectar_guardar(lambda: self._guardar_edicion(dlg, int(id_sel)))

    def _eliminar(self) -> None:
        id_sel = self._obtener_id_seleccionado()
        if not id_sel:
            messagebox.showinfo("Sin selección", "Selecciona una clase para eliminar", parent=self)
            return
        if not self._confirmar_eliminacion(f"clase ID {id_sel}"):
            return
        try:
            self._ctrl.eliminar(int(id_sel))
            self._cargar_datos()
        except Exception as e:
            messagebox.showerror("Error al eliminar", str(e), parent=self)

    def _guardar_nuevo(self, dlg: DialogFormulario) -> None:
        try:
            id_prof = self._extraer_id(dlg.obtener_valor("profesor"))
            id_aula = self._extraer_id(dlg.obtener_valor("aula"))
            id_asig = self._extraer_id(dlg.obtener_valor("asignatura"))
            self._ctrl.crear(
                id_profesor=id_prof,
                id_aula=id_aula,
                id_asignatura=id_asig,
                anio_academico=dlg.obtener_valor("anio"),
                grupo=dlg.obtener_valor("grupo"),
            )
            dlg.destroy()
            self._cargar_datos()
        except (ValueError, Exception) as e:
            messagebox.showerror("Error", str(e), parent=dlg)

    def _guardar_edicion(self, dlg: DialogFormulario, id_clase: int) -> None:
        try:
            id_prof = self._extraer_id(dlg.obtener_valor("profesor"))
            id_aula = self._extraer_id(dlg.obtener_valor("aula"))
            id_asig = self._extraer_id(dlg.obtener_valor("asignatura"))
            self._ctrl.actualizar(
                id_clase=id_clase,
                id_profesor=id_prof,
                id_aula=id_aula,
                id_asignatura=id_asig,
                anio_academico=dlg.obtener_valor("anio"),
                grupo=dlg.obtener_valor("grupo"),
            )
            dlg.destroy()
            self._cargar_datos()
        except (ValueError, Exception) as e:
            messagebox.showerror("Error", str(e), parent=dlg)

    @staticmethod
    def _extraer_id(texto: str) -> int:
        """Extrae el id del formato '[id] Nombre'."""
        try:
            return int(texto.split("]")[0].replace("[", "").strip())
        except Exception:
            raise ValueError(f"Valor no reconocido: '{texto}'")

    @staticmethod
    def _crear_dialogo(titulo: str, clase=None) -> DialogFormulario:
        # Obtener opciones de BD
        profs = bd.obtener_profesores()
        aulas = bd.obtener_aulas()
        asigs = bd.obtener_asignaturas()

        opciones_prof = [f"[{p['id']}] {p['nombre']} {p['apellidos']}" for p in profs]
        opciones_aula = [f"[{a['id']}] {a['numero']}" for a in aulas]
        opciones_asig = [f"[{a['id']}] {a['nombre']}" for a in asigs]

        val_prof = f"[{clase.id_profesor}] {clase.nombre_profesor}" if clase else (opciones_prof[0] if opciones_prof else "")
        val_aula = f"[{clase.id_aula}] {clase.numero_aula}"       if clase else (opciones_aula[0] if opciones_aula else "")
        val_asig = f"[{clase.id_asignatura}] {clase.nombre_asignatura}" if clase else (opciones_asig[0] if opciones_asig else "")

        dlg = DialogFormulario(None, titulo, ancho=500, alto=440)
        dlg.agregar_campo("asignatura", "Asignatura *", val_asig, tipo="combobox", opciones=opciones_asig)
        dlg.agregar_campo("profesor",   "Profesor *",   val_prof, tipo="combobox", opciones=opciones_prof)
        dlg.agregar_campo("aula",       "Aula *",       val_aula, tipo="combobox", opciones=opciones_aula)
        dlg.agregar_campo("anio",       "Año académico * (p.ej. 2025-2026)", clase.anio_academico if clase else "")
        dlg.agregar_campo("grupo",      "Grupo (p.ej. A, B…)", clase.grupo if clase else "A")
        return dlg
