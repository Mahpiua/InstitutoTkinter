from src.modelo import gestor_bd as bd
from src.modelo.aula import Aula


class ControladorAulas:
    """Intermediario entre la vista de aulas y la capa de datos."""

    def obtener_todas(self) -> list[Aula]:
        filas = bd.obtener_aulas()
        return [self._fila_a_aula(f) for f in filas]

    def crear(self, numero: str, capacidad: int, descripcion: str) -> Aula:
        self._validar(numero, capacidad)
        id_aula = bd.insertar_aula(numero, capacidad, descripcion)
        filas = bd.obtener_aulas()
        for f in filas:
            if f["id"] == id_aula:
                return self._fila_a_aula(f)
        return None

    def actualizar(self, id_aula: int, numero: str, capacidad: int, descripcion: str) -> None:
        self._validar(numero, capacidad)
        bd.actualizar_aula(id_aula, numero, capacidad, descripcion)

    def eliminar(self, id_aula: int) -> None:
        bd.eliminar_aula(id_aula)

    @staticmethod
    def _validar(numero: str, capacidad) -> None:
        if not numero.strip():
            raise ValueError("El número del aula es obligatorio")
        try:
            if int(capacidad) <= 0:
                raise ValueError("La capacidad debe ser mayor que 0")
        except (TypeError, ValueError):
            raise ValueError("La capacidad debe ser un número entero positivo")

    @staticmethod
    def _fila_a_aula(f: dict) -> Aula:
        return Aula(
            id_aula=f["id"],
            numero=f["numero"],
            capacidad=f["capacidad"],
            descripcion=f.get("descripcion", ""),
        )
