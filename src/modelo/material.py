class Material:
    """Representa un material del instituto, asociado a un aula."""

    def __init__(self, id_material: int = None, nombre: str = "",
                 descripcion: str = "", cantidad: int = 1,
                 id_aula: int = None, numero_aula: str = "Sin aula"):
        self._id_material = id_material
        self._nombre = nombre
        self._descripcion = descripcion
        self._cantidad = cantidad
        self._id_aula = id_aula
        self._numero_aula = numero_aula

    # ── id_material ───────────────────────────────────────────────────────────
    @property
    def id_material(self) -> int:
        return self._id_material

    @id_material.setter
    def id_material(self, valor: int):
        self._id_material = valor

    # ── nombre ────────────────────────────────────────────────────────────────
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("El nombre del material no puede estar vacío")
        self._nombre = valor.strip()

    # ── descripcion ───────────────────────────────────────────────────────────
    @property
    def descripcion(self) -> str:
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor: str):
        self._descripcion = valor.strip() if valor else ""

    # ── cantidad ──────────────────────────────────────────────────────────────
    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor: int):
        if int(valor) < 0:
            raise ValueError("La cantidad no puede ser negativa")
        self._cantidad = int(valor)

    # ── id_aula ───────────────────────────────────────────────────────────────
    @property
    def id_aula(self) -> int:
        return self._id_aula

    @id_aula.setter
    def id_aula(self, valor: int):
        self._id_aula = valor

    # ── numero_aula (solo lectura, cargado por JOIN) ──────────────────────────
    @property
    def numero_aula(self) -> str:
        return self._numero_aula

    def __str__(self) -> str:
        return f"{self._nombre} (x{self._cantidad}) – Aula {self._numero_aula}"
