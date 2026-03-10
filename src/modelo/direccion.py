from src.modelo.persona import Persona


class Direccion(Persona):
    def __init__(self, id_persona, nombre, apellido, tipo, rol_direccion):
        super().__init__(id_persona, nombre, apellido, tipo)
        self.rol_direccion = rol_direccion

