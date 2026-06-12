import customtkinter as ctk
from tkinter import messagebox
from src.vista.vista_base import VistaGestion, DialogFormulario, rellenar_treeview
from src.controlador.controlador_direccion import ControladorDireccion
from src.modelo.direccion import ROLES_VALIDOS, ROLES_DISPLAY


class DireccionVista(VistaGestion):
    """Vista CRUD para la gestión de los miembros de dirección."""

    def __init__(self, parent):
        self._ctrl = ControladorDireccion()
        super().__init__(parent, "Dirección")

    def _columnas(self) -> list:
        return [
            ("id",        "ID",          50),
            ("rol",       "Rol",        160),
            ("nombre",    "Nombre",     140),
            ("apellidos", "Apellidos",  180),
            ("dni",       "DNI",        110),
            ("profesor",  "Es Profesor", 100),
            ("depto",     "Departamento", 160),
            ("email",     "Email",      180),
        ]

    def _cargar_datos(self) -> None:
        miembros = self._ctrl.obtener_todos()
        filas = [
            (m.id_direccion, m.rol_display, m.nombre, m.apellidos,
             m.dni, "Sí" if m.es_profesor else "No",
             m.departamento, m.email)
            for m in miembros
        ]
        rellenar_treeview(self._tree, filas)

    def _nuevo(self) -> None:
        dlg = self._crear_dialogo("Nuevo miembro de dirección")
        dlg.conectar_guardar(lambda: self._guardar_nuevo(dlg))

    def _editar(self) -> None:
        id_sel = self._obtener_id_seleccionado()
        if not id_sel:
            messagebox.showinfo("Sin selección", "Selecciona un miembro para editar", parent=self)
            return
        miembro = self._ctrl.obtener_por_id(int(id_sel))
        if not miembro:
            return
        dlg = self._crear_dialogo("Editar miembro de dirección", miembro)
        dlg.conectar_guardar(lambda: self._guardar_edicion(dlg, int(id_sel)))

    def _eliminar(self) -> None:
        id_sel = self._obtener_id_seleccionado()
        if not id_sel:
            messagebox.showinfo("Sin selección", "Selecciona un miembro para eliminar", parent=self)
            return
        miembro = self._ctrl.obtener_por_id(int(id_sel))
        if not miembro:
            return
        if not self._confirmar_eliminacion(miembro.nombre_completo()):
            return
        try:
            self._ctrl.eliminar(int(id_sel))
            self._cargar_datos()
        except Exception as e:
            messagebox.showerror("Error al eliminar", str(e), parent=self)

    def _guardar_nuevo(self, dlg: DialogFormulario) -> None:
        try:
            rol_display = dlg.obtener_valor("rol")
            # Convertir display → clave
            rol = next((k for k, v in ROLES_DISPLAY.items() if v == rol_display), rol_display)
            self._ctrl.crear(
                nombre=dlg.obtener_valor("nombre"),
                apellidos=dlg.obtener_valor("apellidos"),
                dni=dlg.obtener_valor("dni"),
                fecha_nacimiento=dlg.obtener_valor("fnac"),
                email=dlg.obtener_valor("email"),
                telefono=dlg.obtener_valor("telefono"),
                rol=rol,
                es_profesor=bool(dlg.obtener_valor("es_profesor")),
                departamento=dlg.obtener_valor("departamento"),
                especialidad=dlg.obtener_valor("especialidad"),
            )
            dlg.destroy()
            self._cargar_datos()
        except (ValueError, Exception) as e:
            messagebox.showerror("Error", str(e), parent=dlg)

    def _guardar_edicion(self, dlg: DialogFormulario, id_dir: int) -> None:
        try:
            rol_display = dlg.obtener_valor("rol")
            rol = next((k for k, v in ROLES_DISPLAY.items() if v == rol_display), rol_display)
            self._ctrl.actualizar(
                id_dir=id_dir,
                nombre=dlg.obtener_valor("nombre"),
                apellidos=dlg.obtener_valor("apellidos"),
                dni=dlg.obtener_valor("dni"),
                fecha_nacimiento=dlg.obtener_valor("fnac"),
                email=dlg.obtener_valor("email"),
                telefono=dlg.obtener_valor("telefono"),
                rol=rol,
                es_profesor=bool(dlg.obtener_valor("es_profesor")),
                departamento=dlg.obtener_valor("departamento"),
                especialidad=dlg.obtener_valor("especialidad"),
            )
            dlg.destroy()
            self._cargar_datos()
        except (ValueError, Exception) as e:
            messagebox.showerror("Error", str(e), parent=dlg)

    @staticmethod
    def _crear_dialogo(titulo: str, m=None) -> DialogFormulario:
        roles_display = list(ROLES_DISPLAY.values())
        rol_inicial = ROLES_DISPLAY.get(m.rol, roles_display[0]) if m else roles_display[0]

        dlg = DialogFormulario(None, titulo, ancho=460, alto=600)
        dlg.agregar_campo("nombre",       "Nombre *",          m.nombre if m else "")
        dlg.agregar_campo("apellidos",    "Apellidos *",       m.apellidos if m else "")
        dlg.agregar_campo("dni",          "DNI *",             m.dni if m else "")
        dlg.agregar_campo("rol",          "Rol *",             rol_inicial,
                          tipo="combobox", opciones=roles_display)
        dlg.agregar_campo("es_profesor",  "También es profesor", m.es_profesor if m else False, tipo="check")
        dlg.agregar_campo("departamento", "Departamento (si es profesor)", m.departamento if m else "")
        dlg.agregar_campo("especialidad", "Especialidad",      m.especialidad if m else "")
        dlg.agregar_campo("fnac",         "Fecha nacimiento (AAAA-MM-DD)", m.fecha_nacimiento if m else "")
        dlg.agregar_campo("email",        "Email",             m.email if m else "")
        dlg.agregar_campo("telefono",     "Teléfono",          m.telefono if m else "")
        return dlg
