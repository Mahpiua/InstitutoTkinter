from src.modelo.persona import Persona


class Profesor(Persona):
    """Representa a un profesor del instituto."""

    def __init__(self, id_persona: int = None, nombre: str = "", apellidos: str = "",
                 dni: str = "", email: str = "", telefono: str = "",
                 fecha_nacimiento: str = "", id_profesor: int = None,
                 departamento: str = "", especialidad: str = ""):
        super().__init__(id_persona=id_persona, nombre=nombre, apellidos=apellidos,
                         dni=dni, email=email, telefono=telefono,
                         fecha_nacimiento=fecha_nacimiento, tipo="profesor")
        self._id_profesor = id_profesor
        self._departamento = departamento
        self._especialidad = especialidad

    # ── id_profesor ───────────────────────────────────────────────────────────
    @property
    def id_profesor(self) -> int:
        return self._id_profesor

    @id_profesor.setter
    def id_profesor(self, valor: int):
        self._id_profesor = valor

    # ── departamento ──────────────────────────────────────────────────────────
    @property
    def departamento(self) -> str:
        return self._departamento

    @departamento.setter
    def departamento(self, valor: str):
        self._departamento = valor.strip() if valor else ""

    # ── especialidad ──────────────────────────────────────────────────────────
    @property
    def especialidad(self) -> str:
        return self._especialidad

    @especialidad.setter
    def especialidad(self, valor: str):
        self._especialidad = valor.strip() if valor else ""

    def __str__(self) -> str:
        return f"Profesor: {self.nombre_completo()} | Dpto: {self._departamento}"
