from src.modelo.persona import Persona


class Alumno(Persona):
    """Representa a un alumno del instituto."""

    def __init__(self, id_persona: int = None, nombre: str = "", apellidos: str = "",
                 dni: str = "", email: str = "", telefono: str = "",
                 fecha_nacimiento: str = "", id_alumno: int = None,
                 numero_expediente: str = ""):
        super().__init__(id_persona=id_persona, nombre=nombre, apellidos=apellidos,
                         dni=dni, email=email, telefono=telefono,
                         fecha_nacimiento=fecha_nacimiento, tipo="alumno")
        self._id_alumno = id_alumno
        self._numero_expediente = numero_expediente

    # ── id_alumno ────────────────────────────────────────────────────────────
    @property
    def id_alumno(self) -> int:
        return self._id_alumno

    @id_alumno.setter
    def id_alumno(self, valor: int):
        self._id_alumno = valor

    # ── numero_expediente ─────────────────────────────────────────────────────
    @property
    def numero_expediente(self) -> str:
        return self._numero_expediente

    @numero_expediente.setter
    def numero_expediente(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("El número de expediente no puede estar vacío")
        self._numero_expediente = valor.strip()

    def __str__(self) -> str:
        return f"Alumno: {self.nombre_completo()} | Exp: {self._numero_expediente}"
