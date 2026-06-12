class TipoConvocatoria:
    """Tipo de convocatoria: 1ª Evaluación, 2ª Evaluación, Evaluación Final, Extraordinaria."""

    def __init__(self, id_tipo: int = None, nombre: str = "", orden: int = 0):
        self._id_tipo = id_tipo
        self._nombre = nombre
        self._orden = orden

    @property
    def id_tipo(self) -> int:
        return self._id_tipo

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def orden(self) -> int:
        return self._orden

    def __str__(self) -> str:
        return self._nombre
