from src.modelo import gestor_bd as bd
from src.modelo.asignatura import Asignatura


class ControladorAsignaturas:
    """Intermediario entre la vista de asignaturas y la capa de datos."""

    def obtener_todas(self) -> list[Asignatura]:
        filas = bd.obtener_asignaturas()
        return [self._fila_a_asignatura(f) for f in filas]

    def crear(self, nombre: str, departamento: str) -> Asignatura:
        self._validar(nombre, departamento)
        id_asig = bd.insertar_asignatura(nombre, departamento)
        filas = bd.obtener_asignaturas()
        for f in filas:
            if f["id"] == id_asig:
                return self._fila_a_asignatura(f)
        return None

    def actualizar(self, id_asig: int, nombre: str, departamento: str) -> None:
        self._validar(nombre, departamento)
        bd.actualizar_asignatura(id_asig, nombre, departamento)

    def eliminar(self, id_asig: int) -> None:
        bd.eliminar_asignatura(id_asig)

    @staticmethod
    def _validar(nombre: str, departamento: str) -> None:
        if not nombre.strip():
            raise ValueError("El nombre de la asignatura es obligatorio")
        if not departamento.strip():
            raise ValueError("El departamento es obligatorio")

    @staticmethod
    def _fila_a_asignatura(f: dict) -> Asignatura:
        return Asignatura(
            id_asignatura=f["id"],
            nombre=f["nombre"],
            departamento=f["departamento"],
        )
