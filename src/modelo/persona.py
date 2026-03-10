from abc import ABC


class Persona(ABC):
    def __init__(self, *, id_persona:int , nombre:str , apellido:str, tipo):
        self.id_persona = id_persona
        self.nombre = nombre
        self.apellido = apellido
        self.tipo = tipo

    def get_id_persona(self):
        return self

    @property
    def id_persona(self):
        return self.id_persona