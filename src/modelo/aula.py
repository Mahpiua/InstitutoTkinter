class Aula:
    """Representa un aula del instituto."""

    def __init__(self, id_aula: int = None, numero: str = "",
                 capacidad: int = 30, descripcion: str = ""):
        self._id_aula = id_aula
        self._numero = numero
        self._capacidad = capacidad
        self._descripcion = descripcion

    # ── id_aula ───────────────────────────────────────────────────────────────
    @property
    def id_aula(self) -> int:
        return self._id_aula

    @id_aula.setter
    def id_aula(self, valor: int):
        self._id_aula = valor

    # ── numero ────────────────────────────────────────────────────────────────
    @property
    def numero(self) -> str:
        return self._numero

    @numero.setter
    def numero(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("El número del aula no puede estar vacío")
        self._numero = valor.strip()

    # ── capacidad ─────────────────────────────────────────────────────────────
    @property
    def capacidad(self) -> int:
        return self._capacidad

    @capacidad.setter
    def capacidad(self, valor: int):
        if int(valor) <= 0:
            raise ValueError("La capacidad debe ser mayor que 0")
        self._capacidad = int(valor)

    # ── descripcion ───────────────────────────────────────────────────────────
    @property
    def descripcion(self) -> str:
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor: str):
        self._descripcion = valor.strip() if valor else ""

    def __str__(self) -> str:
        return f"Aula {self._numero} (Cap: {self._capacidad})"
