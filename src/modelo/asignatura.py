class Asignatura:
    """Representa una asignatura del instituto."""

    def __init__(self, id_asignatura: int = None, nombre: str = "",
                 departamento: str = ""):
        self._id_asignatura = id_asignatura
        self._nombre = nombre
        self._departamento = departamento

    # ── id_asignatura ─────────────────────────────────────────────────────────
    @property
    def id_asignatura(self) -> int:
        return self._id_asignatura

    @id_asignatura.setter
    def id_asignatura(self, valor: int):
        self._id_asignatura = valor

    # ── nombre ────────────────────────────────────────────────────────────────
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("El nombre de la asignatura no puede estar vacío")
        self._nombre = valor.strip()

    # ── departamento ──────────────────────────────────────────────────────────
    @property
    def departamento(self) -> str:
        return self._departamento

    @departamento.setter
    def departamento(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("El departamento no puede estar vacío")
        self._departamento = valor.strip()

    def __str__(self) -> str:
        return f"{self._nombre} ({self._departamento})"
