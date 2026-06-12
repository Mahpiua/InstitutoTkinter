import sqlite3
import csv
from database import queries as q

# Ruta al fichero de base de datos
DB_PATH = "instituto.db"


# ─────────────────────────────────────────────────────────────────────────────
#  CONEXIÓN
# ─────────────────────────────────────────────────────────────────────────────

def iniciar_conexion() -> sqlite3.Connection:
    """Abre y devuelve una conexión a la BD con claves foráneas habilitadas."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row          # acceso por nombre de columna
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ─────────────────────────────────────────────────────────────────────────────
#  CREACIÓN DE TABLAS  (3ª Forma Normal)
# ─────────────────────────────────────────────────────────────────────────────

def crear_bd() -> None:
    """Crea todas las tablas del esquema si no existen."""
    conn = iniciar_conexion()
    cur = conn.cursor()
    cur.executescript("""
        -- Tabla base para todas las personas
        CREATE TABLE IF NOT EXISTS personas (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre           TEXT    NOT NULL,
            apellidos        TEXT    NOT NULL,
            dni              TEXT    UNIQUE NOT NULL,
            email            TEXT    DEFAULT '',
            telefono         TEXT    DEFAULT '',
            fecha_nacimiento TEXT    DEFAULT ''
        );

        -- Alumnos: extiende personas
        CREATE TABLE IF NOT EXISTS alumnos (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            id_persona        INTEGER UNIQUE NOT NULL,
            numero_expediente TEXT    UNIQUE NOT NULL,
            FOREIGN KEY (id_persona) REFERENCES personas(id) ON DELETE CASCADE
        );

        -- Profesores: extiende personas
        CREATE TABLE IF NOT EXISTS profesores (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            id_persona   INTEGER UNIQUE NOT NULL,
            departamento TEXT DEFAULT '',
            especialidad TEXT DEFAULT '',
            FOREIGN KEY (id_persona) REFERENCES personas(id) ON DELETE CASCADE
        );

        -- Miembros de dirección (pueden coincidir con un profesor)
        CREATE TABLE IF NOT EXISTS miembros_direccion (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            id_persona INTEGER UNIQUE NOT NULL,
            rol        TEXT NOT NULL CHECK(rol IN ('director','jefe_estudios','secretario')),
            FOREIGN KEY (id_persona) REFERENCES personas(id) ON DELETE CASCADE
        );

        -- Aulas
        CREATE TABLE IF NOT EXISTS aulas (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            numero      TEXT    UNIQUE NOT NULL,
            capacidad   INTEGER NOT NULL DEFAULT 30,
            descripcion TEXT    DEFAULT ''
        );

        -- Asignaturas
        CREATE TABLE IF NOT EXISTS asignaturas (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre       TEXT NOT NULL,
            departamento TEXT NOT NULL
        );

        -- Materiales asociados a un aula
        CREATE TABLE IF NOT EXISTS materiales (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre      TEXT    NOT NULL,
            descripcion TEXT    DEFAULT '',
            cantidad    INTEGER NOT NULL DEFAULT 1,
            id_aula     INTEGER,
            FOREIGN KEY (id_aula) REFERENCES aulas(id) ON DELETE SET NULL
        );

        -- Clases: profesor + aula + asignatura + año académico
        CREATE TABLE IF NOT EXISTS clases (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            id_profesor    INTEGER NOT NULL,
            id_aula        INTEGER NOT NULL,
            id_asignatura  INTEGER NOT NULL,
            anio_academico TEXT    NOT NULL,
            grupo          TEXT    NOT NULL DEFAULT 'A',
            FOREIGN KEY (id_profesor)   REFERENCES profesores(id),
            FOREIGN KEY (id_aula)       REFERENCES aulas(id),
            FOREIGN KEY (id_asignatura) REFERENCES asignaturas(id),
            UNIQUE(id_asignatura, anio_academico, grupo)
        );

        -- Matrículas: un alumno en un año académico
        CREATE TABLE IF NOT EXISTS matriculas (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            id_alumno      INTEGER NOT NULL,
            anio_academico TEXT    NOT NULL,
            fecha_matricula TEXT   NOT NULL,
            FOREIGN KEY (id_alumno) REFERENCES alumnos(id),
            UNIQUE(id_alumno, anio_academico)
        );

        -- Qué clases cursa cada matrícula (N:M)
        CREATE TABLE IF NOT EXISTS matricula_clase (
            id_matricula INTEGER NOT NULL,
            id_clase     INTEGER NOT NULL,
            PRIMARY KEY (id_matricula, id_clase),
            FOREIGN KEY (id_matricula) REFERENCES matriculas(id) ON DELETE CASCADE,
            FOREIGN KEY (id_clase)     REFERENCES clases(id)     ON DELETE CASCADE
        );

        -- Tipos de convocatoria fijos
        CREATE TABLE IF NOT EXISTS tipos_convocatoria (
            id     INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            orden  INTEGER NOT NULL
        );

        -- Calificaciones: alumno x clase x convocatoria → nota
        CREATE TABLE IF NOT EXISTS calificaciones (
            id                   INTEGER PRIMARY KEY AUTOINCREMENT,
            id_matricula         INTEGER NOT NULL,
            id_clase             INTEGER NOT NULL,
            id_tipo_convocatoria INTEGER NOT NULL,
            nota                 REAL,
            fecha_calificacion   TEXT DEFAULT '',
            FOREIGN KEY (id_matricula)         REFERENCES matriculas(id),
            FOREIGN KEY (id_clase)             REFERENCES clases(id),
            FOREIGN KEY (id_tipo_convocatoria) REFERENCES tipos_convocatoria(id),
            UNIQUE(id_matricula, id_clase, id_tipo_convocatoria)
        );

        -- Administrador del sistema
        CREATE TABLE IF NOT EXISTS admin (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario  TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()


def iniciar_carga() -> None:
    """Inserta datos iniciales si aún no existen."""
    conn = iniciar_conexion()
    cur = conn.cursor()

    cur.execute(q.INSERT_ADMIN, ("admin", "admin123"))

    for nombre, orden in [
        ("1ª Evaluación",    1),
        ("2ª Evaluación",    2),
        ("Evaluación Final", 3),
        ("Extraordinaria",   4),
    ]:
        cur.execute(q.INSERT_CONVOCATORIA, (nombre, orden))

    conn.commit()
    conn.close()


# ─────────────────────────────────────────────────────────────────────────────
#  ADMIN / LOGIN
# ─────────────────────────────────────────────────────────────────────────────

def verificar_login(usuario: str, password: str) -> bool:
    """Comprueba las credenciales del administrador."""
    try:
        conn = iniciar_conexion()
        cur = conn.cursor()
        cur.execute(q.SELECT_LOGIN, (usuario, password))
        resultado = cur.fetchone()
        conn.close()
        return resultado is not None
    except sqlite3.Error as e:
        raise Exception(f"Error al verificar login: {e}")


# ─────────────────────────────────────────────────────────────────────────────
#  ALUMNOS
# ─────────────────────────────────────────────────────────────────────────────

def insertar_alumno(nombre: str, apellidos: str, dni: str, fecha_nacimiento: str,
                    email: str, telefono: str, numero_expediente: str) -> int:
    """Inserta un alumno nuevo; devuelve su id_alumno."""
    conn = iniciar_conexion()
    try:
        cur = conn.cursor()
        cur.execute(q.INSERT_PERSONA,
                    (nombre, apellidos, dni, email, telefono, fecha_nacimiento))
        id_persona = cur.lastrowid
        cur.execute(q.INSERT_ALUMNO, (id_persona, numero_expediente))
        id_alumno = cur.lastrowid
        conn.commit()
        return id_alumno
    except sqlite3.IntegrityError as e:
        conn.rollback()
        msg = str(e).lower()
        if "dni" in msg:
            raise ValueError(f"Ya existe una persona con el DNI '{dni}'")
        if "numero_expediente" in msg:
            raise ValueError(f"Ya existe un alumno con el expediente '{numero_expediente}'")
        raise ValueError(f"Error de integridad: {e}")
    finally:
        conn.close()


def obtener_alumnos() -> list:
    """Devuelve todos los alumnos ordenados por apellidos."""
    try:
        conn = iniciar_conexion()
        cur = conn.cursor()
        cur.execute(q.SELECT_ALUMNOS)
        filas = [dict(f) for f in cur.fetchall()]
        conn.close()
        return filas
    except sqlite3.Error as e:
        raise Exception(f"Error al obtener alumnos: {e}")


def obtener_alumno_por_id(id_alumno: int) -> dict:
    """Devuelve los datos de un alumno concreto."""
    try:
        conn = iniciar_conexion()
        cur = conn.cursor()
        cur.execute(q.SELECT_ALUMNO_POR_ID, (id_alumno,))
        fila = cur.fetchone()
        conn.close()
        return dict(fila) if fila else None
    except sqlite3.Error as e:
        raise Exception(f"Error al obtener alumno: {e}")


def actualizar_alumno(id_alumno: int, nombre: str, apellidos: str, dni: str,
                      fecha_nacimiento: str, email: str, telefono: str,
                      numero_expediente: str) -> None:
    """Actualiza los datos de un alumno existente."""
    conn = iniciar_conexion()
    try:
        cur = conn.cursor()
        cur.execute(q.SELECT_ID_PERSONA_ALUMNO, (id_alumno,))
        row = cur.fetchone()
        if not row:
            raise ValueError(f"No existe alumno con id {id_alumno}")
        id_persona = row["id_persona"]
        cur.execute(q.UPDATE_PERSONA,
                    (nombre, apellidos, dni, email, telefono, fecha_nacimiento, id_persona))
        cur.execute(q.UPDATE_ALUMNO, (numero_expediente, id_alumno))
        conn.commit()
    except sqlite3.IntegrityError as e:
        conn.rollback()
        raise ValueError(f"Error de integridad al actualizar: {e}")
    finally:
        conn.close()


def eliminar_alumno(id_alumno: int) -> None:
    """Elimina un alumno (y en cascada su persona)."""
    conn = iniciar_conexion()
    try:
        cur = conn.cursor()
        cur.execute(q.SELECT_ID_PERSONA_ALUMNO, (id_alumno,))
        row = cur.fetchone()
        if not row:
            raise ValueError(f"No existe alumno con id {id_alumno}")
        # CASCADE borra alumnos cuando se borra la persona
        cur.execute(q.DELETE_PERSONA, (row["id_persona"],))
        conn.commit()
    except ValueError:
        raise
    except sqlite3.Error as e:
        conn.rollback()
        raise Exception(f"Error al eliminar alumno: {e}")
    finally:
        conn.close()


# ─────────────────────────────────────────────────────────────────────────────
#  PROFESORES
# ─────────────────────────────────────────────────────────────────────────────

def insertar_profesor(nombre: str, apellidos: str, dni: str, fecha_nacimiento: str,
                      email: str, telefono: str, departamento: str,
                      especialidad: str) -> int:
    """Inserta un profesor nuevo; devuelve su id_profesor."""
    conn = iniciar_conexion()
    try:
        cur = conn.cursor()
        cur.execute(q.INSERT_PERSONA,
                    (nombre, apellidos, dni, email, telefono, fecha_nacimiento))
        id_persona = cur.lastrowid
        cur.execute(q.INSERT_PROFESOR, (id_persona, departamento, especialidad))
        id_profesor = cur.lastrowid
        conn.commit()
        return id_profesor
    except sqlite3.IntegrityError as e:
        conn.rollback()
        if "dni" in str(e).lower():
            raise ValueError(f"Ya existe una persona con el DNI '{dni}'")
        raise ValueError(f"Error de integridad: {e}")
    finally:
        conn.close()


def obtener_profesores() -> list:
    """Devuelve todos los profesores ordenados por apellidos."""
    try:
        conn = iniciar_conexion()
        cur = conn.cursor()
        cur.execute(q.SELECT_PROFESORES)
        filas = [dict(f) for f in cur.fetchall()]
        conn.close()
        return filas
    except sqlite3.Error as e:
        raise Exception(f"Error al obtener profesores: {e}")


def obtener_profesor_por_id(id_profesor: int) -> dict:
    """Devuelve los datos de un profesor concreto."""
    try:
        conn = iniciar_conexion()
        cur = conn.cursor()
        cur.execute(q.SELECT_PROFESOR_POR_ID, (id_profesor,))
        fila = cur.fetchone()
        conn.close()
        return dict(fila) if fila else None
    except sqlite3.Error as e:
        raise Exception(f"Error al obtener profesor: {e}")


def actualizar_profesor(id_profesor: int, nombre: str, apellidos: str, dni: str,
                        fecha_nacimiento: str, email: str, telefono: str,
                        departamento: str, especialidad: str) -> None:
    """Actualiza los datos de un profesor."""
    conn = iniciar_conexion()
    try:
        cur = conn.cursor()
        cur.execute(q.SELECT_ID_PERSONA_PROFESOR, (id_profesor,))
        row = cur.fetchone()
        if not row:
            raise ValueError(f"No existe profesor con id {id_profesor}")
        id_persona = row["id_persona"]
        cur.execute(q.UPDATE_PERSONA,
                    (nombre, apellidos, dni, email, telefono, fecha_nacimiento, id_persona))
        cur.execute(q.UPDATE_PROFESOR, (departamento, especialidad, id_profesor))
        conn.commit()
    except sqlite3.IntegrityError as e:
        conn.rollback()
        raise ValueError(f"Error de integridad: {e}")
    finally:
        conn.close()


def eliminar_profesor(id_profesor: int) -> None:
    """Elimina un profesor (solo si no tiene clases ni rol de dirección)."""
    conn = iniciar_conexion()
    try:
        cur = conn.cursor()
        cur.execute(q.SELECT_ID_PERSONA_PROFESOR, (id_profesor,))
        row = cur.fetchone()
        if not row:
            raise ValueError(f"No existe profesor con id {id_profesor}")
        id_persona = row["id_persona"]

        cur.execute(q.SELECT_DIRECCION_POR_PERSONA, (id_persona,))
        if cur.fetchone():
            raise ValueError("No se puede eliminar: este profesor también es miembro de dirección")

        cur.execute(q.SELECT_CLASES_DE_PROFESOR, (id_profesor,))
        if cur.fetchone():
            raise ValueError("No se puede eliminar: el profesor tiene clases asignadas")

        cur.execute(q.DELETE_PERSONA, (id_persona,))
        conn.commit()
    except ValueError:
        raise
    except sqlite3.Error as e:
        conn.rollback()
        raise Exception(f"Error al eliminar profesor: {e}")
    finally:
        conn.close()


# ─────────────────────────────────────────────────────────────────────────────
#  DIRECCIÓN
# ─────────────────────────────────────────────────────────────────────────────

def insertar_miembro_direccion(nombre: str, apellidos: str, dni: str,
                               fecha_nacimiento: str, email: str, telefono: str,
                               rol: str, es_profesor: bool = False,
                               departamento: str = "", especialidad: str = "") -> int:
    """Inserta un miembro de dirección (puede también ser profesor)."""
    conn = iniciar_conexion()
    try:
        cur = conn.cursor()
        # Reutilizar persona existente por DNI si ya existe
        cur.execute(q.SELECT_PERSONA_POR_DNI, (dni,))
        persona_row = cur.fetchone()
        if persona_row:
            id_persona = persona_row["id"]
            cur.execute(q.UPDATE_PERSONA_SIN_DNI,
                        (nombre, apellidos, email, telefono, fecha_nacimiento, id_persona))
        else:
            cur.execute(q.INSERT_PERSONA,
                        (nombre, apellidos, dni, email, telefono, fecha_nacimiento))
            id_persona = cur.lastrowid

        if es_profesor:
            cur.execute(q.SELECT_PROFESOR_POR_PERSONA, (id_persona,))
            if not cur.fetchone():
                cur.execute(q.INSERT_PROFESOR, (id_persona, departamento, especialidad))
            else:
                cur.execute(q.UPDATE_PROFESOR_POR_PERSONA,
                            (departamento, especialidad, id_persona))

        cur.execute(q.INSERT_MIEMBRO_DIRECCION, (id_persona, rol))
        id_dir = cur.lastrowid
        conn.commit()
        return id_dir
    except sqlite3.IntegrityError as e:
        conn.rollback()
        if "miembros_direccion" in str(e).lower() or "unique" in str(e).lower():
            raise ValueError("Esta persona ya tiene un rol de dirección asignado")
        raise ValueError(f"Error de integridad: {e}")
    finally:
        conn.close()


def obtener_miembros_direccion() -> list:
    """Devuelve todos los miembros de dirección."""
    try:
        conn = iniciar_conexion()
        cur = conn.cursor()
        cur.execute(q.SELECT_MIEMBROS_DIRECCION)
        filas = [dict(f) for f in cur.fetchall()]
        conn.close()
        return filas
    except sqlite3.Error as e:
        raise Exception(f"Error al obtener miembros de dirección: {e}")


def obtener_miembro_direccion_por_id(id_dir: int) -> dict:
    """Devuelve los datos de un miembro de dirección concreto."""
    try:
        conn = iniciar_conexion()
        cur = conn.cursor()
        cur.execute(q.SELECT_MIEMBRO_DIRECCION_POR_ID, (id_dir,))
        fila = cur.fetchone()
        conn.close()
        return dict(fila) if fila else None
    except sqlite3.Error as e:
        raise Exception(f"Error al obtener miembro de dirección: {e}")


def actualizar_miembro_direccion(id_dir: int, nombre: str, apellidos: str, dni: str,
                                  fecha_nacimiento: str, email: str, telefono: str,
                                  rol: str, es_profesor: bool,
                                  departamento: str, especialidad: str) -> None:
    """Actualiza los datos de un miembro de dirección."""
    conn = iniciar_conexion()
    try:
        cur = conn.cursor()
        cur.execute(q.SELECT_ID_PERSONA_DIRECCION, (id_dir,))
        row = cur.fetchone()
        if not row:
            raise ValueError(f"No existe miembro de dirección con id {id_dir}")
        id_persona = row["id_persona"]

        cur.execute(q.UPDATE_PERSONA,
                    (nombre, apellidos, dni, email, telefono, fecha_nacimiento, id_persona))
        cur.execute(q.UPDATE_MIEMBRO_DIRECCION, (rol, id_dir))

        cur.execute(q.SELECT_PROFESOR_POR_PERSONA, (id_persona,))
        ya_es_prof = cur.fetchone() is not None
        if es_profesor and not ya_es_prof:
            cur.execute(q.INSERT_PROFESOR, (id_persona, departamento, especialidad))
        elif es_profesor and ya_es_prof:
            cur.execute(q.UPDATE_PROFESOR_POR_PERSONA,
                        (departamento, especialidad, id_persona))

        conn.commit()
    except sqlite3.IntegrityError as e:
        conn.rollback()
        raise ValueError(f"Error de integridad: {e}")
    finally:
        conn.close()


def eliminar_miembro_direccion(id_dir: int) -> None:
    """Elimina el rol de dirección (si la persona solo es directivo, también la borra)."""
    conn = iniciar_conexion()
    try:
        cur = conn.cursor()
        cur.execute(q.SELECT_ID_PERSONA_DIRECCION, (id_dir,))
        row = cur.fetchone()
        if not row:
            raise ValueError(f"No existe miembro de dirección con id {id_dir}")
        id_persona = row["id_persona"]

        cur.execute(q.DELETE_MIEMBRO_DIRECCION, (id_dir,))
        # Si ya no es profesor tampoco, eliminar la persona
        cur.execute(q.SELECT_PROFESOR_POR_PERSONA, (id_persona,))
        if not cur.fetchone():
            cur.execute(q.DELETE_PERSONA, (id_persona,))
        conn.commit()
    except ValueError:
        raise
    except sqlite3.Error as e:
        conn.rollback()
        raise Exception(f"Error al eliminar miembro de dirección: {e}")
    finally:
        conn.close()


# ─────────────────────────────────────────────────────────────────────────────
#  AULAS
# ─────────────────────────────────────────────────────────────────────────────

def insertar_aula(numero: str, capacidad: int, descripcion: str = "") -> int:
    """Inserta un aula nueva; devuelve su id."""
    conn = iniciar_conexion()
    try:
        cur = conn.cursor()
        cur.execute(q.INSERT_AULA, (numero, capacidad, descripcion))
        id_aula = cur.lastrowid
        conn.commit()
        return id_aula
    except sqlite3.IntegrityError:
        conn.rollback()
        raise ValueError(f"Ya existe un aula con el número '{numero}'")
    finally:
        conn.close()


def obtener_aulas() -> list:
    """Devuelve todas las aulas ordenadas por número."""
    try:
        conn = iniciar_conexion()
        cur = conn.cursor()
        cur.execute(q.SELECT_AULAS)
        filas = [dict(f) for f in cur.fetchall()]
        conn.close()
        return filas
    except sqlite3.Error as e:
        raise Exception(f"Error al obtener aulas: {e}")


def actualizar_aula(id_aula: int, numero: str, capacidad: int, descripcion: str) -> None:
    """Actualiza los datos de un aula."""
    conn = iniciar_conexion()
    try:
        cur = conn.cursor()
        cur.execute(q.UPDATE_AULA, (numero, capacidad, descripcion, id_aula))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.rollback()
        raise ValueError(f"Ya existe un aula con el número '{numero}'")
    finally:
        conn.close()


def eliminar_aula(id_aula: int) -> None:
    """Elimina un aula (solo si no tiene clases ni materiales asignados)."""
    conn = iniciar_conexion()
    try:
        cur = conn.cursor()
        cur.execute(q.SELECT_CLASES_DE_AULA, (id_aula,))
        if cur.fetchone():
            raise ValueError("No se puede eliminar: el aula tiene clases asignadas")
        cur.execute(q.DELETE_AULA, (id_aula,))
        conn.commit()
    except ValueError:
        raise
    except sqlite3.Error as e:
        conn.rollback()
        raise Exception(f"Error al eliminar aula: {e}")
    finally:
        conn.close()


# ─────────────────────────────────────────────────────────────────────────────
#  ASIGNATURAS
# ─────────────────────────────────────────────────────────────────────────────

def insertar_asignatura(nombre: str, departamento: str) -> int:
    """Inserta una asignatura nueva; devuelve su id."""
    conn = iniciar_conexion()
    try:
        cur = conn.cursor()
        cur.execute(q.INSERT_ASIGNATURA, (nombre, departamento))
        id_asig = cur.lastrowid
        conn.commit()
        return id_asig
    except sqlite3.Error as e:
        conn.rollback()
        raise Exception(f"Error al insertar asignatura: {e}")
    finally:
        conn.close()


def obtener_asignaturas() -> list:
    """Devuelve todas las asignaturas."""
    try:
        conn = iniciar_conexion()
        cur = conn.cursor()
        cur.execute(q.SELECT_ASIGNATURAS)
        filas = [dict(f) for f in cur.fetchall()]
        conn.close()
        return filas
    except sqlite3.Error as e:
        raise Exception(f"Error al obtener asignaturas: {e}")


def actualizar_asignatura(id_asig: int, nombre: str, departamento: str) -> None:
    """Actualiza una asignatura."""
    conn = iniciar_conexion()
    try:
        cur = conn.cursor()
        cur.execute(q.UPDATE_ASIGNATURA, (nombre, departamento, id_asig))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise Exception(f"Error al actualizar asignatura: {e}")
    finally:
        conn.close()


def eliminar_asignatura(id_asig: int) -> None:
    """Elimina una asignatura (solo si no tiene clases)."""
    conn = iniciar_conexion()
    try:
        cur = conn.cursor()
        cur.execute(q.SELECT_CLASES_DE_ASIGNATURA, (id_asig,))
        if cur.fetchone():
            raise ValueError("No se puede eliminar: la asignatura tiene clases asignadas")
        cur.execute(q.DELETE_ASIGNATURA, (id_asig,))
        conn.commit()
    except ValueError:
        raise
    except sqlite3.Error as e:
        conn.rollback()
        raise Exception(f"Error al eliminar asignatura: {e}")
    finally:
        conn.close()


# ─────────────────────────────────────────────────────────────────────────────
#  MATERIALES
# ─────────────────────────────────────────────────────────────────────────────

def insertar_material(nombre: str, descripcion: str, cantidad: int,
                      id_aula: int = None) -> int:
    """Inserta un material nuevo; devuelve su id."""
    conn = iniciar_conexion()
    try:
        cur = conn.cursor()
        cur.execute(q.INSERT_MATERIAL, (nombre, descripcion, cantidad, id_aula))
        id_mat = cur.lastrowid
        conn.commit()
        return id_mat
    except sqlite3.Error as e:
        conn.rollback()
        raise Exception(f"Error al insertar material: {e}")
    finally:
        conn.close()


def obtener_materiales() -> list:
    """Devuelve todos los materiales con el número de su aula."""
    try:
        conn = iniciar_conexion()
        cur = conn.cursor()
        cur.execute(q.SELECT_MATERIALES)
        filas = [dict(f) for f in cur.fetchall()]
        conn.close()
        return filas
    except sqlite3.Error as e:
        raise Exception(f"Error al obtener materiales: {e}")


def actualizar_material(id_mat: int, nombre: str, descripcion: str,
                        cantidad: int, id_aula: int = None) -> None:
    """Actualiza un material."""
    conn = iniciar_conexion()
    try:
        cur = conn.cursor()
        cur.execute(q.UPDATE_MATERIAL, (nombre, descripcion, cantidad, id_aula, id_mat))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise Exception(f"Error al actualizar material: {e}")
    finally:
        conn.close()


def eliminar_material(id_mat: int) -> None:
    """Elimina un material."""
    conn = iniciar_conexion()
    try:
        cur = conn.cursor()
        cur.execute(q.DELETE_MATERIAL, (id_mat,))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise Exception(f"Error al eliminar material: {e}")
    finally:
        conn.close()


def importar_materiales_csv(ruta: str) -> tuple:
    """
    Importa materiales desde un CSV (columnas: nombre,descripcion,cantidad,numero_aula).
    Devuelve (n_insertados, lista_errores).
    """
    insertados = 0
    errores = []
    try:
        with open(ruta, encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            conn = iniciar_conexion()
            cur = conn.cursor()
            for i, fila in enumerate(reader, start=2):
                try:
                    nombre = fila.get("nombre", "").strip()
                    if not nombre:
                        errores.append(f"Fila {i}: nombre vacío")
                        continue
                    descripcion = fila.get("descripcion", "").strip()
                    try:
                        cantidad = int(fila.get("cantidad", 1))
                    except ValueError:
                        errores.append(f"Fila {i}: cantidad no es un número")
                        continue
                    numero_aula = fila.get("numero_aula", "").strip()
                    id_aula = None
                    if numero_aula:
                        cur.execute(q.SELECT_AULA_POR_NUMERO, (numero_aula,))
                        row = cur.fetchone()
                        if row:
                            id_aula = row["id"]
                        else:
                            errores.append(
                                f"Fila {i}: aula '{numero_aula}' no encontrada "
                                f"(se insertará sin aula)"
                            )
                    cur.execute(q.INSERT_MATERIAL, (nombre, descripcion, cantidad, id_aula))
                    insertados += 1
                except Exception as e:
                    errores.append(f"Fila {i}: {e}")
            conn.commit()
            conn.close()
    except FileNotFoundError:
        raise ValueError(f"Archivo no encontrado: {ruta}")
    except Exception as e:
        raise Exception(f"Error al importar materiales: {e}")
    return insertados, errores


# ─────────────────────────────────────────────────────────────────────────────
#  CLASES
# ─────────────────────────────────────────────────────────────────────────────

def insertar_clase(id_profesor: int, id_aula: int, id_asignatura: int,
                   anio_academico: str, grupo: str = "A") -> int:
    """Inserta una clase nueva; devuelve su id."""
    conn = iniciar_conexion()
    try:
        cur = conn.cursor()
        cur.execute(q.INSERT_CLASE,
                    (id_profesor, id_aula, id_asignatura, anio_academico, grupo))
        id_clase = cur.lastrowid
        conn.commit()
        return id_clase
    except sqlite3.IntegrityError:
        conn.rollback()
        raise ValueError("Ya existe una clase con esa asignatura, año académico y grupo")
    finally:
        conn.close()


def obtener_clases() -> list:
    """Devuelve todas las clases con datos de profesor, aula y asignatura."""
    try:
        conn = iniciar_conexion()
        cur = conn.cursor()
        cur.execute(q.SELECT_CLASES)
        filas = [dict(f) for f in cur.fetchall()]
        conn.close()
        return filas
    except sqlite3.Error as e:
        raise Exception(f"Error al obtener clases: {e}")


def actualizar_clase(id_clase: int, id_profesor: int, id_aula: int,
                     id_asignatura: int, anio_academico: str, grupo: str) -> None:
    """Actualiza los datos de una clase."""
    conn = iniciar_conexion()
    try:
        cur = conn.cursor()
        cur.execute(q.UPDATE_CLASE,
                    (id_profesor, id_aula, id_asignatura, anio_academico, grupo, id_clase))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.rollback()
        raise ValueError("Ya existe una clase con esa asignatura, año académico y grupo")
    finally:
        conn.close()


def eliminar_clase(id_clase: int) -> None:
    """Elimina una clase."""
    conn = iniciar_conexion()
    try:
        cur = conn.cursor()
        cur.execute(q.DELETE_CLASE, (id_clase,))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise Exception(f"Error al eliminar clase: {e}")
    finally:
        conn.close()


# ─────────────────────────────────────────────────────────────────────────────
#  MATRÍCULAS
# ─────────────────────────────────────────────────────────────────────────────

def insertar_matricula(id_alumno: int, anio_academico: str,
                       fecha_matricula: str, ids_clases: list) -> int:
    """Inserta una matrícula con sus clases; devuelve id_matricula."""
    conn = iniciar_conexion()
    try:
        cur = conn.cursor()
        cur.execute(q.INSERT_MATRICULA, (id_alumno, anio_academico, fecha_matricula))
        id_mat = cur.lastrowid
        for id_clase in ids_clases:
            cur.execute(q.INSERT_MATRICULA_CLASE, (id_mat, id_clase))
        conn.commit()
        return id_mat
    except sqlite3.IntegrityError:
        conn.rollback()
        raise ValueError(f"Ya existe una matrícula para este alumno en el año {anio_academico}")
    finally:
        conn.close()


def obtener_matriculas() -> list:
    """Devuelve todas las matrículas con nombre del alumno."""
    try:
        conn = iniciar_conexion()
        cur = conn.cursor()
        cur.execute(q.SELECT_MATRICULAS)
        filas = [dict(f) for f in cur.fetchall()]
        conn.close()
        return filas
    except sqlite3.Error as e:
        raise Exception(f"Error al obtener matrículas: {e}")


def obtener_matriculas_alumno(id_alumno: int) -> list:
    """Devuelve las matrículas de un alumno concreto."""
    try:
        conn = iniciar_conexion()
        cur = conn.cursor()
        cur.execute(q.SELECT_MATRICULAS_ALUMNO, (id_alumno,))
        filas = [dict(f) for f in cur.fetchall()]
        conn.close()
        return filas
    except sqlite3.Error as e:
        raise Exception(f"Error al obtener matrículas del alumno: {e}")


def eliminar_matricula(id_mat: int) -> None:
    """Elimina una matrícula (y en cascada sus calificaciones)."""
    conn = iniciar_conexion()
    try:
        cur = conn.cursor()
        cur.execute(q.DELETE_MATRICULA, (id_mat,))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise Exception(f"Error al eliminar matrícula: {e}")
    finally:
        conn.close()


def obtener_clases_de_matricula(id_matricula: int) -> list:
    """Devuelve las clases asociadas a una matrícula."""
    try:
        conn = iniciar_conexion()
        cur = conn.cursor()
        cur.execute(q.SELECT_CLASES_DE_MATRICULA, (id_matricula,))
        filas = [dict(f) for f in cur.fetchall()]
        conn.close()
        return filas
    except sqlite3.Error as e:
        raise Exception(f"Error al obtener clases de la matrícula: {e}")


# ─────────────────────────────────────────────────────────────────────────────
#  CALIFICACIONES
# ─────────────────────────────────────────────────────────────────────────────

def guardar_calificacion(id_matricula: int, id_clase: int,
                         id_tipo_convocatoria: int, nota: float,
                         fecha_calificacion: str) -> None:
    """Inserta o actualiza una calificación (upsert)."""
    conn = iniciar_conexion()
    try:
        cur = conn.cursor()
        cur.execute(q.UPSERT_CALIFICACION,
                    (id_matricula, id_clase, id_tipo_convocatoria, nota, fecha_calificacion))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise Exception(f"Error al guardar calificación: {e}")
    finally:
        conn.close()


def obtener_calificaciones_para_grid(id_alumno: int, anio_academico: str) -> list:
    """
    Devuelve las calificaciones de un alumno organizadas para la cuadrícula.
    Cada elemento: {asignatura, id_clase, id_matricula, '1ª Evaluación': nota, ...}
    """
    try:
        conn = iniciar_conexion()
        cur = conn.cursor()

        cur.execute(q.SELECT_ASIGNATURAS_ALUMNO_ANIO, (id_alumno, anio_academico))
        asignaturas = [dict(f) for f in cur.fetchall()]

        cur.execute(q.SELECT_TIPOS_CONVOCATORIA_SIMPLE)
        convocatorias = [dict(f) for f in cur.fetchall()]

        resultado = []
        for asig in asignaturas:
            fila = {
                "id_asignatura": asig["id_asignatura"],
                "asignatura":    asig["asignatura"],
                "id_clase":      asig["id_clase"],
                "id_matricula":  asig["id_matricula"],
            }
            for conv in convocatorias:
                cur.execute(q.SELECT_NOTA,
                            (asig["id_matricula"], asig["id_clase"], conv["id"]))
                nota_row = cur.fetchone()
                fila[conv["nombre"]] = (
                    nota_row["nota"] if nota_row and nota_row["nota"] is not None else ""
                )
            resultado.append(fila)

        conn.close()
        return resultado
    except sqlite3.Error as e:
        raise Exception(f"Error al obtener calificaciones: {e}")


def obtener_anios_alumno(id_alumno: int) -> list:
    """Devuelve los años académicos en que el alumno tiene matrícula."""
    try:
        conn = iniciar_conexion()
        cur = conn.cursor()
        cur.execute(q.SELECT_ANIOS_ALUMNO, (id_alumno,))
        filas = [f["anio_academico"] for f in cur.fetchall()]
        conn.close()
        return filas
    except sqlite3.Error as e:
        raise Exception(f"Error al obtener años académicos: {e}")


def obtener_tipos_convocatoria() -> list:
    """Devuelve todos los tipos de convocatoria."""
    try:
        conn = iniciar_conexion()
        cur = conn.cursor()
        cur.execute(q.SELECT_TIPOS_CONVOCATORIA)
        filas = [dict(f) for f in cur.fetchall()]
        conn.close()
        return filas
    except sqlite3.Error as e:
        raise Exception(f"Error al obtener tipos de convocatoria: {e}")


def exportar_calificaciones_asignatura(id_asignatura: int, anio_academico: str) -> list:
    """
    Devuelve filas para exportar: año, convocatoria, alumno, asignatura, nota.
    Ordenado alfabéticamente por apellidos del alumno.
    """
    try:
        conn = iniciar_conexion()
        cur = conn.cursor()
        cur.execute(q.SELECT_EXPORTAR_CALIFICACIONES, (anio_academico, id_asignatura, anio_academico))
        filas = [dict(f) for f in cur.fetchall()]
        conn.close()
        return filas
    except sqlite3.Error as e:
        raise Exception(f"Error al exportar calificaciones: {e}")
