from src.modelo.persona import Persona

# Roles válidos para los miembros de dirección
ROLES_VALIDOS = ("director", "jefe_estudios", "secretario")
ROLES_DISPLAY = {
    "director": "Director/a",
    "jefe_estudios": "Jefe/a de Estudios",
    "secretario": "Secretario/a",
}


class Direccion(Persona):
    """Representa a un miembro de la dirección del instituto.
    Puede ser simultáneamente profesor.
    """

    def __init__(self, id_persona: int = None, nombre: str = "", apellidos: str = "",
                 dni: str = "", email: str = "", telefono: str = "",
                 fecha_nacimiento: str = "", id_direccion: int = None,
                 rol: str = "", es_profesor: bool = False,
                 id_profesor: int = None, departamento: str = "",
                 especialidad: str = ""):
        super().__init__(id_persona=id_persona, nombre=nombre, apellidos=apellidos,
                         dni=dni, email=email, telefono=telefono,
                         fecha_nacimiento=fecha_nacimiento, tipo="direccion")
        self._id_direccion = id_direccion
        self._rol = rol
        self._es_profesor = es_profesor
        self._id_profesor = id_profesor
        self._departamento = departamento
        self._especialidad = especialidad

    # ── id_direccion ──────────────────────────────────────────────────────────
    @property
    def id_direccion(self) -> int:
        return self._id_direccion

    @id_direccion.setter
    def id_direccion(self, valor: int):
        self._id_direccion = valor

    # ── rol ───────────────────────────────────────────────────────────────────
    @property
    def rol(self) -> str:
        return self._rol

    @rol.setter
    def rol(self, valor: str):
        if valor not in ROLES_VALIDOS:
            raise ValueError(f"Rol inválido. Debe ser uno de: {ROLES_VALIDOS}")
        self._rol = valor

    @property
    def rol_display(self) -> str:
        return ROLES_DISPLAY.get(self._rol, self._rol)

    # ── es_profesor ───────────────────────────────────────────────────────────
    @property
    def es_profesor(self) -> bool:
        return self._es_profesor

    @es_profesor.setter
    def es_profesor(self, valor: bool):
        self._es_profesor = bool(valor)

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
        return f"{self.rol_display}: {self.nombre_completo()}"
