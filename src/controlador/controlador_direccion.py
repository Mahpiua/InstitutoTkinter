from src.modelo import gestor_bd as bd
from src.modelo.direccion import Direccion


class ControladorDireccion:
    """Intermediario entre la vista de dirección y la capa de datos."""

    def obtener_todos(self) -> list[Direccion]:
        filas = bd.obtener_miembros_direccion()
        return [self._fila_a_direccion(f) for f in filas]

    def obtener_por_id(self, id_dir: int) -> Direccion:
        fila = bd.obtener_miembro_direccion_por_id(id_dir)
        return self._fila_a_direccion(fila) if fila else None

    def crear(self, nombre: str, apellidos: str, dni: str, fecha_nacimiento: str,
              email: str, telefono: str, rol: str, es_profesor: bool,
              departamento: str, especialidad: str) -> Direccion:
        self._validar(nombre, apellidos, dni, rol)
        id_dir = bd.insertar_miembro_direccion(
            nombre, apellidos, dni, fecha_nacimiento, email, telefono,
            rol, es_profesor, departamento, especialidad
        )
        return self.obtener_por_id(id_dir)

    def actualizar(self, id_dir: int, nombre: str, apellidos: str, dni: str,
                   fecha_nacimiento: str, email: str, telefono: str,
                   rol: str, es_profesor: bool, departamento: str, especialidad: str) -> None:
        self._validar(nombre, apellidos, dni, rol)
        bd.actualizar_miembro_direccion(
            id_dir, nombre, apellidos, dni, fecha_nacimiento,
            email, telefono, rol, es_profesor, departamento, especialidad
        )

    def eliminar(self, id_dir: int) -> None:
        bd.eliminar_miembro_direccion(id_dir)

    @staticmethod
    def _validar(nombre: str, apellidos: str, dni: str, rol: str) -> None:
        if not nombre.strip():
            raise ValueError("El nombre es obligatorio")
        if not apellidos.strip():
            raise ValueError("Los apellidos son obligatorios")
        if not dni.strip():
            raise ValueError("El DNI es obligatorio")
        if not rol:
            raise ValueError("El rol es obligatorio")

    @staticmethod
    def _fila_a_direccion(f: dict) -> Direccion:
        return Direccion(
            id_persona=f["id_persona"],
            nombre=f["nombre"],
            apellidos=f["apellidos"],
            dni=f["dni"],
            email=f.get("email", ""),
            telefono=f.get("telefono", ""),
            fecha_nacimiento=f.get("fecha_nacimiento", ""),
            id_direccion=f["id"],
            rol=f["rol"],
            es_profesor=bool(f.get("es_profesor", 0)),
            id_profesor=f.get("id_profesor"),
            departamento=f.get("departamento", ""),
            especialidad=f.get("especialidad", ""),
        )
