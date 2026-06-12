from datetime import date
from src.modelo import gestor_bd as bd
from src.modelo.matricula import Matricula


class ControladorMatriculas:
    """Intermediario entre la vista de matrículas y la capa de datos."""

    def obtener_todas(self) -> list[Matricula]:
        filas = bd.obtener_matriculas()
        return [self._fila_a_matricula(f) for f in filas]

    def obtener_por_alumno(self, id_alumno: int) -> list[Matricula]:
        filas = bd.obtener_matriculas_alumno(id_alumno)
        return [Matricula(id_matricula=f["id"],
                          anio_academico=f["anio_academico"],
                          fecha_matricula=f["fecha_matricula"],
                          id_alumno=id_alumno) for f in filas]

    def crear(self, id_alumno: int, anio_academico: str, ids_clases: list) -> Matricula:
        if not anio_academico.strip():
            raise ValueError("El año académico es obligatorio")
        if not ids_clases:
            raise ValueError("Debe seleccionar al menos una clase")
        fecha_hoy = date.today().isoformat()
        id_mat = bd.insertar_matricula(id_alumno, anio_academico, fecha_hoy, ids_clases)
        filas = bd.obtener_matriculas()
        for f in filas:
            if f["id"] == id_mat:
                return self._fila_a_matricula(f)
        return None

    def eliminar(self, id_matricula: int) -> None:
        bd.eliminar_matricula(id_matricula)

    def obtener_clases_matricula(self, id_matricula: int) -> list:
        return bd.obtener_clases_de_matricula(id_matricula)

    @staticmethod
    def _fila_a_matricula(f: dict) -> Matricula:
        return Matricula(
            id_matricula=f["id"],
            id_alumno=f["id_alumno"],
            anio_academico=f["anio_academico"],
            fecha_matricula=f["fecha_matricula"],
            nombre_alumno=f.get("nombre_alumno", ""),
            numero_expediente=f.get("numero_expediente", ""),
        )
