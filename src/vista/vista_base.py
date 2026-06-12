"""
Módulo con componentes reutilizables para las vistas de gestión.
Proporciona:
  - VistaGestion: frame estándar con tabla + barra de herramientas
  - crear_treeview: crea un ttk.Treeview con scroll y estilos oscuros
  - DialogFormulario: ventana emergente genérica para formularios de alta/edición
"""

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk


# ─────────────────────────────────────────────────────────────────────────────
#  Estilos para el Treeview oscuro
# ─────────────────────────────────────────────────────────────────────────────

def _aplicar_estilo_treeview() -> None:
    """Configura el estilo oscuro del Treeview una sola vez."""
    estilo = ttk.Style()
    estilo.theme_use("clam")
    estilo.configure("Instituto.Treeview",
                     background="#1a2e1f",
                     foreground="#e2e8f0",
                     fieldbackground="#1a2e1f",
                     rowheight=28,
                     font=("Segoe UI", 11))
    estilo.configure("Instituto.Treeview.Heading",
                     background="#16a34a",
                     foreground="white",
                     font=("Segoe UI", 11, "bold"),
                     relief="flat")
    estilo.map("Instituto.Treeview",
               background=[("selected", "#16a34a")],
               foreground=[("selected", "white")])


_aplicar_estilo_treeview()


# ─────────────────────────────────────────────────────────────────────────────
#  Función auxiliar para crear Treeview con scroll
# ─────────────────────────────────────────────────────────────────────────────

def crear_treeview(parent, columnas: list) -> ttk.Treeview:
    """
    Crea un ttk.Treeview con scroll vertical y horizontal.
    columnas: lista de (id_columna, texto_cabecera, ancho)
    """
    marco = tk.Frame(parent, bg="#0d1f12")
    marco.pack(fill="both", expand=True)

    scroll_v = ttk.Scrollbar(marco, orient="vertical")
    scroll_h = ttk.Scrollbar(marco, orient="horizontal")

    ids_col = [c[0] for c in columnas]
    tree = ttk.Treeview(marco,
                        columns=ids_col,
                        show="headings",
                        style="Instituto.Treeview",
                        yscrollcommand=scroll_v.set,
                        xscrollcommand=scroll_h.set,
                        selectmode="browse")

    scroll_v.configure(command=tree.yview)
    scroll_h.configure(command=tree.xview)

    for col_id, col_texto, col_ancho in columnas:
        tree.heading(col_id, text=col_texto)
        tree.column(col_id, width=col_ancho, minwidth=60, anchor="w")

    scroll_v.pack(side="right", fill="y")
    scroll_h.pack(side="bottom", fill="x")
    tree.pack(fill="both", expand=True)

    # Colores alternos de filas
    tree.tag_configure("par",   background="#1a2e1f")
    tree.tag_configure("impar", background="#203828")

    return tree


def rellenar_treeview(tree: ttk.Treeview, filas: list) -> None:
    """Limpia y vuelve a rellenar el Treeview con las filas dadas."""
    tree.delete(*tree.get_children())
    for i, fila in enumerate(filas):
        tag = "par" if i % 2 == 0 else "impar"
        tree.insert("", "end", values=fila, tags=(tag,))


# ─────────────────────────────────────────────────────────────────────────────
#  VistaGestion – frame base con cabecera, toolbar y tabla
# ─────────────────────────────────────────────────────────────────────────────

class VistaGestion(ctk.CTkFrame):
    """
    Frame reutilizable para módulos de gestión (CRUD).
    Las subclases deben implementar:
      - _columnas()   → list[(id, texto, ancho)]
      - _cargar_datos()
      - _nuevo()
      - _editar()
      - _eliminar()
    """

    def __init__(self, parent, titulo: str):
        super().__init__(parent, fg_color="#0d1f12", corner_radius=0)
        self._titulo = titulo
        self._tree: ttk.Treeview | None = None
        self._construir_base()
        self._cargar_datos()

    # ── Estructura base ───────────────────────────────────────────────────────

    def _construir_base(self) -> None:
        # Cabecera
        cab = ctk.CTkFrame(self, fg_color="#132a1a", height=64, corner_radius=0)
        cab.pack(fill="x")
        cab.pack_propagate(False)

        ctk.CTkLabel(cab, text=self._titulo,
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="#e2e8f0").pack(side="left", padx=24, pady=16)

        # Toolbar
        toolbar = ctk.CTkFrame(cab, fg_color="transparent")
        toolbar.pack(side="right", padx=16)

        self._btn_nuevo = ctk.CTkButton(toolbar, text="Nuevo", width=100, height=36,
                                         corner_radius=8, command=self._nuevo)
        self._btn_nuevo.pack(side="left", padx=4)

        self._btn_editar = ctk.CTkButton(toolbar, text="Editar", width=100, height=36,
                                          corner_radius=8, fg_color="#1e4d2e",
                                          hover_color="#2d6a3f", command=self._editar)
        self._btn_editar.pack(side="left", padx=4)

        self._btn_eliminar = ctk.CTkButton(toolbar, text="Eliminar", width=100, height=36,
                                            corner_radius=8, fg_color="#7f1d1d",
                                            hover_color="#991b1b", command=self._eliminar)
        self._btn_eliminar.pack(side="left", padx=4)

        # Área de la tabla
        self._frame_tabla = ctk.CTkFrame(self, fg_color="#0d1f12", corner_radius=0)
        self._frame_tabla.pack(fill="both", expand=True, padx=16, pady=16)

        self._tree = crear_treeview(self._frame_tabla, self._columnas())

    # ── Métodos a sobreescribir ────────────────────────────────────────────────

    def _columnas(self) -> list:
        raise NotImplementedError

    def _cargar_datos(self) -> None:
        raise NotImplementedError

    def _nuevo(self) -> None:
        raise NotImplementedError

    def _editar(self) -> None:
        raise NotImplementedError

    def _eliminar(self) -> None:
        raise NotImplementedError

    # ── Utilidades compartidas ────────────────────────────────────────────────

    def _obtener_id_seleccionado(self):
        """Devuelve el primer valor de la fila seleccionada (habitualmente el id)."""
        sel = self._tree.selection()
        if not sel:
            return None
        return self._tree.item(sel[0])["values"][0]

    def _confirmar_eliminacion(self, nombre: str) -> bool:
        return messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Deseas eliminar '{nombre}'?\nEsta acción no se puede deshacer.",
            parent=self
        )


# ─────────────────────────────────────────────────────────────────────────────
#  DialogFormulario – ventana emergente genérica para formularios
# ─────────────────────────────────────────────────────────────────────────────

class DialogFormulario(ctk.CTkToplevel):
    """Ventana de diálogo para formularios de alta y edición."""

    def __init__(self, parent, titulo: str, ancho: int = 500, alto: int = 480):
        super().__init__(parent)
        self.title(titulo)
        self.geometry(f"{ancho}x{alto}")
        self.resizable(False, False)
        self.grab_set()              # Modal
        self.configure(fg_color="#0d1f12")
        self._campos: dict = {}

        # Cabecera
        ctk.CTkLabel(self, text=titulo,
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="#e2e8f0").pack(pady=(20, 0))

        # Área scrollable para el formulario
        self._scroll = ctk.CTkScrollableFrame(self, fg_color="#122218", corner_radius=12)
        self._scroll.pack(fill="both", expand=True, padx=20, pady=16)

        # Botones al fondo
        frame_btns = ctk.CTkFrame(self, fg_color="transparent")
        frame_btns.pack(pady=(0, 16))

        ctk.CTkButton(frame_btns, text="Cancelar", width=120, height=38,
                      corner_radius=8, fg_color="#1e4d2e", hover_color="#2d6a3f",
                      command=self.destroy).pack(side="left", padx=8)

        self._btn_guardar = ctk.CTkButton(frame_btns, text="Guardar", width=120, height=38,
                                          corner_radius=8, command=self._al_guardar)
        self._btn_guardar.pack(side="left", padx=8)

        # Centrar ventana
        self.update_idletasks()
        if parent is not None:
            px = parent.winfo_rootx() + (parent.winfo_width() - ancho) // 2
            py = parent.winfo_rooty() + (parent.winfo_height() - alto) // 2
        else:
            sw = self.winfo_screenwidth()
            sh = self.winfo_screenheight()
            px = (sw - ancho) // 2
            py = (sh - alto) // 2
        self.geometry(f"{ancho}x{alto}+{px}+{py}")

    def agregar_campo(self, clave: str, etiqueta: str,
                      valor_inicial: str = "",
                      tipo: str = "texto",
                      opciones: list = None) -> None:
        """
        Agrega un campo al formulario.
        tipo: 'texto' | 'password' | 'combobox' | 'check'
        """
        ctk.CTkLabel(self._scroll, text=etiqueta, anchor="w",
                     text_color="#94a3b8", font=ctk.CTkFont(size=12)).pack(
            anchor="w", padx=8, pady=(8, 2))

        if tipo == "password":
            widget = ctk.CTkEntry(self._scroll, show="•", height=36, corner_radius=6)
        elif tipo == "combobox":
            widget = ctk.CTkComboBox(self._scroll, values=opciones or [],
                                      height=36, corner_radius=6)
            widget.set(valor_inicial)
        elif tipo == "check":
            var = ctk.BooleanVar(value=bool(valor_inicial))
            widget = ctk.CTkCheckBox(self._scroll, text="", variable=var)
            self._campos[clave] = var
            widget.pack(anchor="w", padx=8, pady=(0, 4))
            return
        else:
            widget = ctk.CTkEntry(self._scroll, height=36, corner_radius=6)

        if tipo not in ("combobox", "check"):
            widget.insert(0, str(valor_inicial) if valor_inicial else "")

        widget.pack(fill="x", padx=8, pady=(0, 4))
        self._campos[clave] = widget

    def obtener_valor(self, clave: str) -> str:
        """Devuelve el valor actual de un campo del formulario."""
        campo = self._campos.get(clave)
        if campo is None:
            return ""
        if isinstance(campo, ctk.BooleanVar):
            return campo.get()
        if isinstance(campo, ctk.CTkComboBox):
            return campo.get()
        return campo.get().strip()

    def _al_guardar(self) -> None:
        """Sobreescribir en la subclase o conectar vía callback."""
        pass

    def conectar_guardar(self, callback) -> None:
        """Conecta la acción del botón Guardar a una función externa."""
        self._btn_guardar.configure(command=callback)
