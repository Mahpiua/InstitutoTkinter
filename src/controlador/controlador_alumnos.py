from src.modelo import gestor_bd as bd
from src.modelo.alumno import Alumno


class ControladorAlumnos:
    """Intermediario entre la vista de alumnos y la capa de datos."""

    # ── Consultas ─────────────────────────────────────────────────────────────

    def obtener_todos(self) -> list[Alumno]:
        """Devuelve todos los alumnos como objetos Alumno."""
        filas = bd.obtener_alumnos()
        return [self._fila_a_alumno(f) for f in filas]

    def obtener_por_id(self, id_alumno: int) -> Alumno:
        """Devuelve un Alumno concreto o None si no existe."""
        fila = bd.obtener_alumno_por_id(id_alumno)
        return self._fila_a_alumno(fila) if fila else None

    # ── Operaciones CRUD ──────────────────────────────────────────────────────

    def crear(self, nombre: str, apellidos: str, dni: str, fecha_nacimiento: str,
              email: str, telefono: str, numero_expediente: str) -> Alumno:
        """Valida los datos y crea un alumno nuevo."""
        self._validar(nombre, apellidos, dni, numero_expediente)
        id_alumno = bd.insertar_alumno(
            nombre, apellidos, dni, fecha_nacimiento, email, telefono, numero_expediente
        )
        return self.obtener_por_id(id_alumno)

    def actualizar(self, id_alumno: int, nombre: str, apellidos: str, dni: str,
                   fecha_nacimiento: str, email: str, telefono: str,
                   numero_expediente: str) -> None:
        """Valida y actualiza los datos de un alumno."""
        self._validar(nombre, apellidos, dni, numero_expediente)
        bd.actualizar_alumno(
            id_alumno, nombre, apellidos, dni, fecha_nacimiento,
            email, telefono, numero_expediente
        )

    def eliminar(self, id_alumno: int) -> None:
        """Elimina un alumno por su id."""
        bd.eliminar_alumno(id_alumno)

    # ── Utilidades privadas ───────────────────────────────────────────────────

    @staticmethod
    def _validar(nombre: str, apellidos: str, dni: str, expediente: str) -> None:
        """Lanza ValueError si algún campo obligatorio está vacío."""
        if not nombre.strip():
            raise ValueError("El nombre es obligatorio")
        if not apellidos.strip():
            raise ValueError("Los apellidos son obligatorios")
        if not dni.strip():
            raise ValueError("El DNI es obligatorio")
        if not expediente.strip():
            raise ValueError("El número de expediente es obligatorio")

    @staticmethod
    def _fila_a_alumno(f: dict) -> Alumno:
        return Alumno(
            id_persona=f["id_persona"],
            nombre=f["nombre"],
            apellidos=f["apellidos"],
            dni=f["dni"],
            email=f.get("email", ""),
            telefono=f.get("telefono", ""),
            fecha_nacimiento=f.get("fecha_nacimiento", ""),
            id_alumno=f["id"],
            numero_expediente=f["numero_expediente"],
        )
