from src.modelo import gestor_bd as bd
from src.modelo.profesor import Profesor


class ControladorProfesores:
    """Intermediario entre la vista de profesores y la capa de datos."""

    def obtener_todos(self) -> list[Profesor]:
        filas = bd.obtener_profesores()
        return [self._fila_a_profesor(f) for f in filas]

    def obtener_por_id(self, id_profesor: int) -> Profesor:
        fila = bd.obtener_profesor_por_id(id_profesor)
        return self._fila_a_profesor(fila) if fila else None

    def crear(self, nombre: str, apellidos: str, dni: str, fecha_nacimiento: str,
              email: str, telefono: str, departamento: str, especialidad: str) -> Profesor:
        self._validar(nombre, apellidos, dni)
        id_prof = bd.insertar_profesor(
            nombre, apellidos, dni, fecha_nacimiento, email, telefono,
            departamento, especialidad
        )
        return self.obtener_por_id(id_prof)

    def actualizar(self, id_profesor: int, nombre: str, apellidos: str, dni: str,
                   fecha_nacimiento: str, email: str, telefono: str,
                   departamento: str, especialidad: str) -> None:
        self._validar(nombre, apellidos, dni)
        bd.actualizar_profesor(
            id_profesor, nombre, apellidos, dni, fecha_nacimiento,
            email, telefono, departamento, especialidad
        )

    def eliminar(self, id_profesor: int) -> None:
        bd.eliminar_profesor(id_profesor)

    @staticmethod
    def _validar(nombre: str, apellidos: str, dni: str) -> None:
        if not nombre.strip():
            raise ValueError("El nombre es obligatorio")
        if not apellidos.strip():
            raise ValueError("Los apellidos son obligatorios")
        if not dni.strip():
            raise ValueError("El DNI es obligatorio")

    @staticmethod
    def _fila_a_profesor(f: dict) -> Profesor:
        return Profesor(
            id_persona=f["id_persona"],
            nombre=f["nombre"],
            apellidos=f["apellidos"],
            dni=f["dni"],
            email=f.get("email", ""),
            telefono=f.get("telefono", ""),
            fecha_nacimiento=f.get("fecha_nacimiento", ""),
            id_profesor=f["id"],
            departamento=f.get("departamento", ""),
            especialidad=f.get("especialidad", ""),
        )
