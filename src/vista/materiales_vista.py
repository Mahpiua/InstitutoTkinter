import customtkinter as ctk
from tkinter import messagebox, filedialog
from src.vista.vista_base import VistaGestion, DialogFormulario, rellenar_treeview
from src.controlador.controlador_materiales import ControladorMateriales
from src.modelo import gestor_bd as bd


class MaterialesVista(VistaGestion):
    """Vista CRUD para la gestión de materiales, con importación desde CSV."""

    def __init__(self, parent):
        self._ctrl = ControladorMateriales()
        super().__init__(parent, "Materiales")
        self._agregar_boton_importar()

    def _agregar_boton_importar(self) -> None:
        """Añade el botón de importar CSV junto al resto de la toolbar."""
        # Buscar la cabecera (primer hijo del frame) y añadir el botón
        for widget in self.winfo_children():
            for inner in widget.winfo_children():
                if isinstance(inner, ctk.CTkFrame):
                    ctk.CTkButton(
                        inner,
                        text="📂 Importar CSV",
                        width=130,
                        height=36,
                        corner_radius=8,
                        fg_color="#15803d",
                        hover_color="#16a34a",
                        command=self._importar_csv,
                    ).pack(side="left", padx=4)
                    return

    def _columnas(self) -> list:
        return [
            ("id",          "ID",         50),
            ("nombre",      "Nombre",    200),
            ("descripcion", "Descripción", 240),
            ("cantidad",    "Cantidad",   90),
            ("aula",        "Aula",       100),
        ]

    def _cargar_datos(self) -> None:
        materiales = self._ctrl.obtener_todos()
        filas = [
            (m.id_material, m.nombre, m.descripcion, m.cantidad, m.numero_aula)
            for m in materiales
        ]
        rellenar_treeview(self._tree, filas)

    def _nuevo(self) -> None:
        dlg = self._crear_dialogo("Nuevo material")
        dlg.conectar_guardar(lambda: self._guardar_nuevo(dlg))

    def _editar(self) -> None:
        id_sel = self._obtener_id_seleccionado()
        if not id_sel:
            messagebox.showinfo("Sin selección", "Selecciona un material para editar", parent=self)
            return
        mats = self._ctrl.obtener_todos()
        mat = next((m for m in mats if m.id_material == int(id_sel)), None)
        if not mat:
            return
        dlg = self._crear_dialogo("Editar material", mat)
        dlg.conectar_guardar(lambda: self._guardar_edicion(dlg, int(id_sel)))

    def _eliminar(self) -> None:
        id_sel = self._obtener_id_seleccionado()
        if not id_sel:
            messagebox.showinfo("Sin selección", "Selecciona un material para eliminar", parent=self)
            return
        mats = self._ctrl.obtener_todos()
        mat = next((m for m in mats if m.id_material == int(id_sel)), None)
        nombre = mat.nombre if mat else str(id_sel)
        if not self._confirmar_eliminacion(nombre):
            return
        try:
            self._ctrl.eliminar(int(id_sel))
            self._cargar_datos()
        except Exception as e:
            messagebox.showerror("Error al eliminar", str(e), parent=self)

    def _guardar_nuevo(self, dlg: DialogFormulario) -> None:
        try:
            id_aula = self._extraer_id_aula(dlg.obtener_valor("aula"))
            self._ctrl.crear(
                nombre=dlg.obtener_valor("nombre"),
                descripcion=dlg.obtener_valor("descripcion"),
                cantidad=dlg.obtener_valor("cantidad"),
                id_aula=id_aula,
            )
            dlg.destroy()
            self._cargar_datos()
        except (ValueError, Exception) as e:
            messagebox.showerror("Error", str(e), parent=dlg)

    def _guardar_edicion(self, dlg: DialogFormulario, id_mat: int) -> None:
        try:
            id_aula = self._extraer_id_aula(dlg.obtener_valor("aula"))
            self._ctrl.actualizar(
                id_mat=id_mat,
                nombre=dlg.obtener_valor("nombre"),
                descripcion=dlg.obtener_valor("descripcion"),
                cantidad=dlg.obtener_valor("cantidad"),
                id_aula=id_aula,
            )
            dlg.destroy()
            self._cargar_datos()
        except (ValueError, Exception) as e:
            messagebox.showerror("Error", str(e), parent=dlg)

    def _importar_csv(self) -> None:
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo CSV de materiales",
            filetypes=[("CSV", "*.csv"), ("Todos", "*.*")],
            parent=self,
        )
        if not ruta:
            return
        try:
            insertados, errores = self._ctrl.importar_csv(ruta)
            msg = f"Se importaron {insertados} material(es) correctamente."
            if errores:
                msg += f"\n\nAdvertencias ({len(errores)}):\n" + "\n".join(errores[:10])
                if len(errores) > 10:
                    msg += f"\n... y {len(errores) - 10} más."
            messagebox.showinfo("Importación completada", msg, parent=self)
            self._cargar_datos()
        except Exception as e:
            messagebox.showerror("Error al importar", str(e), parent=self)

    @staticmethod
    def _extraer_id_aula(texto: str):
        if not texto or texto == "Sin aula":
            return None
        try:
            return int(texto.split("]")[0].replace("[", "").strip())
        except Exception:
            return None

    @staticmethod
    def _crear_dialogo(titulo: str, mat=None) -> DialogFormulario:
        aulas = bd.obtener_aulas()
        opciones_aula = ["Sin aula"] + [f"[{a['id']}] {a['numero']}" for a in aulas]
        val_aula = "Sin aula"
        if mat and mat.id_aula:
            val_aula = f"[{mat.id_aula}] {mat.numero_aula}"

        dlg = DialogFormulario(None, titulo, ancho=460, alto=400)
        dlg.agregar_campo("nombre",      "Nombre del material *", mat.nombre if mat else "")
        dlg.agregar_campo("descripcion", "Descripción",           mat.descripcion if mat else "")
        dlg.agregar_campo("cantidad",    "Cantidad *",            mat.cantidad if mat else "1")
        dlg.agregar_campo("aula",        "Aula",                  val_aula,
                          tipo="combobox", opciones=opciones_aula)
        return dlg
