from src.modelo import gestor_bd as bd
from src.modelo.material import Material


class ControladorMateriales:
    """Intermediario entre la vista de materiales y la capa de datos."""

    def obtener_todos(self) -> list[Material]:
        filas = bd.obtener_materiales()
        return [self._fila_a_material(f) for f in filas]

    def crear(self, nombre: str, descripcion: str, cantidad: int,
              id_aula: int = None) -> Material:
        self._validar(nombre, cantidad)
        id_mat = bd.insertar_material(nombre, descripcion, cantidad, id_aula)
        filas = bd.obtener_materiales()
        for f in filas:
            if f["id"] == id_mat:
                return self._fila_a_material(f)
        return None

    def actualizar(self, id_mat: int, nombre: str, descripcion: str,
                   cantidad: int, id_aula: int = None) -> None:
        self._validar(nombre, cantidad)
        bd.actualizar_material(id_mat, nombre, descripcion, cantidad, id_aula)

    def eliminar(self, id_mat: int) -> None:
        bd.eliminar_material(id_mat)

    def importar_csv(self, ruta: str) -> tuple:
        """Importa materiales desde CSV; devuelve (insertados, errores)."""
        return bd.importar_materiales_csv(ruta)

    @staticmethod
    def _validar(nombre: str, cantidad) -> None:
        if not nombre.strip():
            raise ValueError("El nombre del material es obligatorio")
        try:
            if int(cantidad) < 0:
                raise ValueError("La cantidad no puede ser negativa")
        except (TypeError, ValueError):
            raise ValueError("La cantidad debe ser un número entero no negativo")

    @staticmethod
    def _fila_a_material(f: dict) -> Material:
        return Material(
            id_material=f["id"],
            nombre=f["nombre"],
            descripcion=f.get("descripcion", ""),
            cantidad=f["cantidad"],
            id_aula=f.get("id_aula"),
            numero_aula=f.get("numero_aula", "Sin aula"),
        )
