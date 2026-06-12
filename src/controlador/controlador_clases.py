from src.modelo import gestor_bd as bd
from src.modelo.clase import Clase


class ControladorClases:
    """Intermediario entre la vista de clases y la capa de datos."""

    def obtener_todas(self) -> list[Clase]:
        filas = bd.obtener_clases()
        return [self._fila_a_clase(f) for f in filas]

    def crear(self, id_profesor: int, id_aula: int, id_asignatura: int,
              anio_academico: str, grupo: str) -> Clase:
        self._validar(id_profesor, id_aula, id_asignatura, anio_academico, grupo)
        id_clase = bd.insertar_clase(id_profesor, id_aula, id_asignatura, anio_academico, grupo)
        filas = bd.obtener_clases()
        for f in filas:
            if f["id"] == id_clase:
                return self._fila_a_clase(f)
        return None

    def actualizar(self, id_clase: int, id_profesor: int, id_aula: int,
                   id_asignatura: int, anio_academico: str, grupo: str) -> None:
        self._validar(id_profesor, id_aula, id_asignatura, anio_academico, grupo)
        bd.actualizar_clase(id_clase, id_profesor, id_aula, id_asignatura, anio_academico, grupo)

    def eliminar(self, id_clase: int) -> None:
        bd.eliminar_clase(id_clase)

    @staticmethod
    def _validar(id_profesor, id_aula, id_asignatura, anio_academico: str, grupo: str) -> None:
        if not id_profesor:
            raise ValueError("Debe seleccionar un profesor")
        if not id_aula:
            raise ValueError("Debe seleccionar un aula")
        if not id_asignatura:
            raise ValueError("Debe seleccionar una asignatura")
        if not anio_academico.strip():
            raise ValueError("El año académico es obligatorio (p. ej. 2025-2026)")
        if not grupo.strip():
            raise ValueError("El grupo es obligatorio")

    @staticmethod
    def _fila_a_clase(f: dict) -> Clase:
        return Clase(
            id_clase=f["id"],
            id_profesor=f["id_profesor"],
            id_aula=f["id_aula"],
            id_asignatura=f["id_asignatura"],
            anio_academico=f["anio_academico"],
            grupo=f["grupo"],
            nombre_profesor=f.get("nombre_profesor", ""),
            numero_aula=f.get("numero_aula", ""),
            nombre_asignatura=f.get("nombre_asignatura", ""),
        )
