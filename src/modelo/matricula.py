class Matricula:
    """Matrícula de un alumno en un año académico (incluye las clases en las que se inscribe)."""

    def __init__(self, id_matricula: int = None, id_alumno: int = None,
                 anio_academico: str = "", fecha_matricula: str = "",
                 nombre_alumno: str = "", numero_expediente: str = ""):
        self._id_matricula = id_matricula
        self._id_alumno = id_alumno
        self._anio_academico = anio_academico
        self._fecha_matricula = fecha_matricula
        self._nombre_alumno = nombre_alumno
        self._numero_expediente = numero_expediente

    # ── id_matricula ──────────────────────────────────────────────────────────
    @property
    def id_matricula(self) -> int:
        return self._id_matricula

    @id_matricula.setter
    def id_matricula(self, valor: int):
        self._id_matricula = valor

    # ── id_alumno ─────────────────────────────────────────────────────────────
    @property
    def id_alumno(self) -> int:
        return self._id_alumno

    @id_alumno.setter
    def id_alumno(self, valor: int):
        self._id_alumno = valor

    # ── anio_academico ────────────────────────────────────────────────────────
    @property
    def anio_academico(self) -> str:
        return self._anio_academico

    @anio_academico.setter
    def anio_academico(self, valor: str):
        if not valor:
            raise ValueError("El año académico no puede estar vacío")
        self._anio_academico = valor

    # ── fecha_matricula ───────────────────────────────────────────────────────
    @property
    def fecha_matricula(self) -> str:
        return self._fecha_matricula

    @fecha_matricula.setter
    def fecha_matricula(self, valor: str):
        self._fecha_matricula = valor if valor else ""

    # ── nombre_alumno (solo lectura) ──────────────────────────────────────────
    @property
    def nombre_alumno(self) -> str:
        return self._nombre_alumno

    @property
    def numero_expediente(self) -> str:
        return self._numero_expediente

    def __str__(self) -> str:
        return f"Matrícula de {self._nombre_alumno} – {self._anio_academico}"
