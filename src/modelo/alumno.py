from src.modelo.persona import Persona
from datetime import datetime, date

class Alumno(Persona):

    def __init__(self, id_persona: int, nombre: str, apellido: str,
                 id_alumno: int = None, numero_expediente: str = "",
                 fecha_nacimiento: date = None, email: str = "", telefono: str = ""):
        super().__init__(id_persona, nombre, apellido, "alumno", email, telefono)
        self._id_alumno = id_alumno
        self._numero_expediente = numero_expediente
        self._fecha_nacimiento = fecha_nacimiento
        self._matriculas = []
        self._clases = []
        self._calificaciones = []

