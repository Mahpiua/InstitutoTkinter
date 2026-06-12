class Calificacion:
    """Calificación de un alumno en una asignatura para una convocatoria concreta."""

    def __init__(self, id_calificacion: int = None, id_matricula: int = None,
                 id_clase: int = None, id_tipo_convocatoria: int = None,
                 nota: float = None, fecha_calificacion: str = "",
                 nombre_alumno: str = "", nombre_asignatura: str = "",
                 nombre_convocatoria: str = "", anio_academico: str = ""):
        self._id_calificacion = id_calificacion
        self._id_matricula = id_matricula
        self._id_clase = id_clase
        self._id_tipo_convocatoria = id_tipo_convocatoria
        self._nota = nota
        self._fecha_calificacion = fecha_calificacion
        self._nombre_alumno = nombre_alumno
        self._nombre_asignatura = nombre_asignatura
        self._nombre_convocatoria = nombre_convocatoria
        self._anio_academico = anio_academico

    # ── id_calificacion ───────────────────────────────────────────────────────
    @property
    def id_calificacion(self) -> int:
        return self._id_calificacion

    # ── nota ──────────────────────────────────────────────────────────────────
    @property
    def nota(self) -> float:
        return self._nota

    @nota.setter
    def nota(self, valor):
        if valor is not None and (float(valor) < 0 or float(valor) > 10):
            raise ValueError("La nota debe estar entre 0 y 10")
        self._nota = float(valor) if valor is not None else None

    @property
    def nota_str(self) -> str:
        return str(self._nota) if self._nota is not None else "-"

    # ── campos de solo lectura ────────────────────────────────────────────────
    @property
    def id_matricula(self) -> int:
        return self._id_matricula

    @property
    def id_clase(self) -> int:
        return self._id_clase

    @property
    def id_tipo_convocatoria(self) -> int:
        return self._id_tipo_convocatoria

    @property
    def fecha_calificacion(self) -> str:
        return self._fecha_calificacion

    @property
    def nombre_alumno(self) -> str:
        return self._nombre_alumno

    @property
    def nombre_asignatura(self) -> str:
        return self._nombre_asignatura

    @property
    def nombre_convocatoria(self) -> str:
        return self._nombre_convocatoria

    @property
    def anio_academico(self) -> str:
        return self._anio_academico

    def __str__(self) -> str:
        return f"{self._nombre_asignatura} – {self._nombre_convocatoria}: {self.nota_str}"
