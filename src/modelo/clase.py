class Clase:
    """Representa una clase: un profesor imparte una asignatura en un aula durante un año."""

    def __init__(self, id_clase: int = None, id_profesor: int = None,
                 id_aula: int = None, id_asignatura: int = None,
                 anio_academico: str = "", grupo: str = "A",
                 nombre_profesor: str = "", numero_aula: str = "",
                 nombre_asignatura: str = ""):
        self._id_clase = id_clase
        self._id_profesor = id_profesor
        self._id_aula = id_aula
        self._id_asignatura = id_asignatura
        self._anio_academico = anio_academico
        self._grupo = grupo
        # Campos de presentación (cargados mediante JOIN)
        self._nombre_profesor = nombre_profesor
        self._numero_aula = numero_aula
        self._nombre_asignatura = nombre_asignatura

    # ── id_clase ──────────────────────────────────────────────────────────────
    @property
    def id_clase(self) -> int:
        return self._id_clase

    @id_clase.setter
    def id_clase(self, valor: int):
        self._id_clase = valor

    # ── id_profesor ───────────────────────────────────────────────────────────
    @property
    def id_profesor(self) -> int:
        return self._id_profesor

    @id_profesor.setter
    def id_profesor(self, valor: int):
        self._id_profesor = valor

    # ── id_aula ───────────────────────────────────────────────────────────────
    @property
    def id_aula(self) -> int:
        return self._id_aula

    @id_aula.setter
    def id_aula(self, valor: int):
        self._id_aula = valor

    # ── id_asignatura ─────────────────────────────────────────────────────────
    @property
    def id_asignatura(self) -> int:
        return self._id_asignatura

    @id_asignatura.setter
    def id_asignatura(self, valor: int):
        self._id_asignatura = valor

    # ── anio_academico ────────────────────────────────────────────────────────
    @property
    def anio_academico(self) -> str:
        return self._anio_academico

    @anio_academico.setter
    def anio_academico(self, valor: str):
        if not valor:
            raise ValueError("El año académico no puede estar vacío")
        self._anio_academico = valor

    # ── grupo ─────────────────────────────────────────────────────────────────
    @property
    def grupo(self) -> str:
        return self._grupo

    @grupo.setter
    def grupo(self, valor: str):
        self._grupo = valor if valor else "A"

    # ── campos de presentación (solo lectura) ─────────────────────────────────
    @property
    def nombre_profesor(self) -> str:
        return self._nombre_profesor

    @property
    def numero_aula(self) -> str:
        return self._numero_aula

    @property
    def nombre_asignatura(self) -> str:
        return self._nombre_asignatura

    def __str__(self) -> str:
        return f"{self._nombre_asignatura} - Grupo {self._grupo} ({self._anio_academico})"
