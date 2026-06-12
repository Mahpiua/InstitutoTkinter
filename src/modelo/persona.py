from abc import ABC


class Persona(ABC):
    """Clase base abstracta para todas las personas del sistema."""

    def __init__(self, id_persona: int = None, nombre: str = "", apellidos: str = "",
                 dni: str = "", email: str = "", telefono: str = "",
                 fecha_nacimiento: str = "", tipo: str = ""):
        self._id_persona = id_persona
        self._nombre = nombre
        self._apellidos = apellidos
        self._dni = dni
        self._email = email
        self._telefono = telefono
        self._fecha_nacimiento = fecha_nacimiento
        self._tipo = tipo

    # ── id_persona ──────────────────────────────────────────────────────────
    @property
    def id_persona(self) -> int:
        return self._id_persona

    @id_persona.setter
    def id_persona(self, valor: int):
        self._id_persona = valor

    # ── nombre ──────────────────────────────────────────────────────────────
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("El nombre no puede estar vacío")
        self._nombre = valor.strip()

    # ── apellidos ────────────────────────────────────────────────────────────
    @property
    def apellidos(self) -> str:
        return self._apellidos

    @apellidos.setter
    def apellidos(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("Los apellidos no pueden estar vacíos")
        self._apellidos = valor.strip()

    # ── dni ──────────────────────────────────────────────────────────────────
    @property
    def dni(self) -> str:
        return self._dni

    @dni.setter
    def dni(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("El DNI no puede estar vacío")
        self._dni = valor.strip().upper()

    # ── email ────────────────────────────────────────────────────────────────
    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str):
        self._email = valor.strip() if valor else ""

    # ── telefono ─────────────────────────────────────────────────────────────
    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        self._telefono = valor.strip() if valor else ""

    # ── fecha_nacimiento ──────────────────────────────────────────────────────
    @property
    def fecha_nacimiento(self) -> str:
        return self._fecha_nacimiento

    @fecha_nacimiento.setter
    def fecha_nacimiento(self, valor: str):
        self._fecha_nacimiento = valor if valor else ""

    # ── tipo ─────────────────────────────────────────────────────────────────
    @property
    def tipo(self) -> str:
        return self._tipo

    # ── métodos de utilidad ───────────────────────────────────────────────────
    def nombre_completo(self) -> str:
        """Devuelve nombre y apellidos concatenados."""
        return f"{self._nombre} {self._apellidos}"

    def __str__(self) -> str:
        return f"{self._tipo.capitalize()}: {self.nombre_completo()} (DNI: {self._dni})"
