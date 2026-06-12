"""
Cadenas SQL (SELECT, INSERT, UPDATE, DELETE) del sistema.
gestor_bd.py importa estas constantes y las pasa a cursor.execute().
"""

# ─── ADMIN ────────────────────────────────────────────────────────────────────

INSERT_ADMIN = (
    "INSERT OR IGNORE INTO admin (usuario, password) VALUES (?, ?)"
)

SELECT_LOGIN = (
    "SELECT id FROM admin WHERE usuario = ? AND password = ?"
)

# ─── CONVOCATORIAS ────────────────────────────────────────────────────────────

INSERT_CONVOCATORIA = (
    "INSERT OR IGNORE INTO tipos_convocatoria (nombre, orden) VALUES (?, ?)"
)

SELECT_TIPOS_CONVOCATORIA = (
    "SELECT id, nombre, orden FROM tipos_convocatoria ORDER BY orden"
)

SELECT_TIPOS_CONVOCATORIA_SIMPLE = (
    "SELECT id, nombre FROM tipos_convocatoria ORDER BY orden"
)

# ─── PERSONAS ─────────────────────────────────────────────────────────────────

INSERT_PERSONA = (
    "INSERT INTO personas "
    "(nombre, apellidos, dni, email, telefono, fecha_nacimiento) "
    "VALUES (?, ?, ?, ?, ?, ?)"
)

SELECT_PERSONA_POR_DNI = (
    "SELECT id FROM personas WHERE dni = ?"
)

UPDATE_PERSONA = (
    "UPDATE personas SET nombre=?, apellidos=?, dni=?, email=?, telefono=?, "
    "fecha_nacimiento=? WHERE id=?"
)

# Versión sin DNI: se usa al reutilizar una persona ya existente por DNI
UPDATE_PERSONA_SIN_DNI = (
    "UPDATE personas SET nombre=?, apellidos=?, email=?, telefono=?, "
    "fecha_nacimiento=? WHERE id=?"
)

DELETE_PERSONA = (
    "DELETE FROM personas WHERE id = ?"
)

# ─── ALUMNOS ──────────────────────────────────────────────────────────────────

INSERT_ALUMNO = (
    "INSERT INTO alumnos (id_persona, numero_expediente) VALUES (?, ?)"
)

SELECT_ALUMNOS = """
    SELECT a.id, p.id AS id_persona, p.nombre, p.apellidos, p.dni,
           p.email, p.telefono, p.fecha_nacimiento, a.numero_expediente
    FROM alumnos a
    JOIN personas p ON p.id = a.id_persona
    ORDER BY p.apellidos, p.nombre
"""

SELECT_ALUMNO_POR_ID = """
    SELECT a.id, p.id AS id_persona, p.nombre, p.apellidos, p.dni,
           p.email, p.telefono, p.fecha_nacimiento, a.numero_expediente
    FROM alumnos a
    JOIN personas p ON p.id = a.id_persona
    WHERE a.id = ?
"""

SELECT_ID_PERSONA_ALUMNO = (
    "SELECT id_persona FROM alumnos WHERE id = ?"
)

UPDATE_ALUMNO = (
    "UPDATE alumnos SET numero_expediente=? WHERE id=?"
)

# ─── PROFESORES ───────────────────────────────────────────────────────────────

INSERT_PROFESOR = (
    "INSERT INTO profesores (id_persona, departamento, especialidad) VALUES (?, ?, ?)"
)

SELECT_PROFESORES = """
    SELECT pr.id, p.id AS id_persona, p.nombre, p.apellidos, p.dni,
           p.email, p.telefono, p.fecha_nacimiento,
           pr.departamento, pr.especialidad
    FROM profesores pr
    JOIN personas p ON p.id = pr.id_persona
    ORDER BY p.apellidos, p.nombre
"""

SELECT_PROFESOR_POR_ID = """
    SELECT pr.id, p.id AS id_persona, p.nombre, p.apellidos, p.dni,
           p.email, p.telefono, p.fecha_nacimiento,
           pr.departamento, pr.especialidad
    FROM profesores pr
    JOIN personas p ON p.id = pr.id_persona
    WHERE pr.id = ?
"""

SELECT_ID_PERSONA_PROFESOR = (
    "SELECT id_persona FROM profesores WHERE id = ?"
)

SELECT_PROFESOR_POR_PERSONA = (
    "SELECT id FROM profesores WHERE id_persona = ?"
)

UPDATE_PROFESOR = (
    "UPDATE profesores SET departamento=?, especialidad=? WHERE id=?"
)

UPDATE_PROFESOR_POR_PERSONA = (
    "UPDATE profesores SET departamento=?, especialidad=? WHERE id_persona=?"
)

SELECT_CLASES_DE_PROFESOR = (
    "SELECT id FROM clases WHERE id_profesor = ?"
)

# ─── DIRECCIÓN ────────────────────────────────────────────────────────────────

INSERT_MIEMBRO_DIRECCION = (
    "INSERT INTO miembros_direccion (id_persona, rol) VALUES (?, ?)"
)

SELECT_MIEMBROS_DIRECCION = """
    SELECT md.id, p.id AS id_persona, p.nombre, p.apellidos, p.dni,
           p.email, p.telefono, p.fecha_nacimiento, md.rol,
           CASE WHEN pr.id IS NOT NULL THEN 1 ELSE 0 END AS es_profesor,
           pr.id AS id_profesor, pr.departamento, pr.especialidad
    FROM miembros_direccion md
    JOIN personas p ON p.id = md.id_persona
    LEFT JOIN profesores pr ON pr.id_persona = md.id_persona
    ORDER BY md.rol, p.apellidos
"""

SELECT_MIEMBRO_DIRECCION_POR_ID = """
    SELECT md.id, p.id AS id_persona, p.nombre, p.apellidos, p.dni,
           p.email, p.telefono, p.fecha_nacimiento, md.rol,
           CASE WHEN pr.id IS NOT NULL THEN 1 ELSE 0 END AS es_profesor,
           pr.id AS id_profesor, pr.departamento, pr.especialidad
    FROM miembros_direccion md
    JOIN personas p ON p.id = md.id_persona
    LEFT JOIN profesores pr ON pr.id_persona = md.id_persona
    WHERE md.id = ?
"""

SELECT_ID_PERSONA_DIRECCION = (
    "SELECT id_persona FROM miembros_direccion WHERE id = ?"
)

SELECT_DIRECCION_POR_PERSONA = (
    "SELECT id FROM miembros_direccion WHERE id_persona = ?"
)

UPDATE_MIEMBRO_DIRECCION = (
    "UPDATE miembros_direccion SET rol=? WHERE id=?"
)

DELETE_MIEMBRO_DIRECCION = (
    "DELETE FROM miembros_direccion WHERE id = ?"
)

# ─── AULAS ────────────────────────────────────────────────────────────────────

INSERT_AULA = (
    "INSERT INTO aulas (numero, capacidad, descripcion) VALUES (?, ?, ?)"
)

SELECT_AULAS = (
    "SELECT id, numero, capacidad, descripcion FROM aulas ORDER BY numero"
)

UPDATE_AULA = (
    "UPDATE aulas SET numero=?, capacidad=?, descripcion=? WHERE id=?"
)

DELETE_AULA = (
    "DELETE FROM aulas WHERE id = ?"
)

SELECT_CLASES_DE_AULA = (
    "SELECT id FROM clases WHERE id_aula = ?"
)

SELECT_AULA_POR_NUMERO = (
    "SELECT id FROM aulas WHERE numero = ?"
)

# ─── ASIGNATURAS ──────────────────────────────────────────────────────────────

INSERT_ASIGNATURA = (
    "INSERT INTO asignaturas (nombre, departamento) VALUES (?, ?)"
)

SELECT_ASIGNATURAS = (
    "SELECT id, nombre, departamento FROM asignaturas ORDER BY nombre"
)

UPDATE_ASIGNATURA = (
    "UPDATE asignaturas SET nombre=?, departamento=? WHERE id=?"
)

DELETE_ASIGNATURA = (
    "DELETE FROM asignaturas WHERE id = ?"
)

SELECT_CLASES_DE_ASIGNATURA = (
    "SELECT id FROM clases WHERE id_asignatura = ?"
)

# ─── MATERIALES ───────────────────────────────────────────────────────────────

INSERT_MATERIAL = (
    "INSERT INTO materiales (nombre, descripcion, cantidad, id_aula) VALUES (?, ?, ?, ?)"
)

SELECT_MATERIALES = """
    SELECT m.id, m.nombre, m.descripcion, m.cantidad,
           m.id_aula, COALESCE(a.numero, 'Sin aula') AS numero_aula
    FROM materiales m
    LEFT JOIN aulas a ON a.id = m.id_aula
    ORDER BY m.nombre
"""

UPDATE_MATERIAL = (
    "UPDATE materiales SET nombre=?, descripcion=?, cantidad=?, id_aula=? WHERE id=?"
)

DELETE_MATERIAL = (
    "DELETE FROM materiales WHERE id = ?"
)

# ─── CLASES ───────────────────────────────────────────────────────────────────

INSERT_CLASE = (
    "INSERT INTO clases "
    "(id_profesor, id_aula, id_asignatura, anio_academico, grupo) "
    "VALUES (?, ?, ?, ?, ?)"
)

SELECT_CLASES = """
    SELECT c.id, c.anio_academico, c.grupo,
           c.id_profesor, p.nombre || ' ' || p.apellidos AS nombre_profesor,
           c.id_aula, a.numero AS numero_aula,
           c.id_asignatura, asig.nombre AS nombre_asignatura
    FROM clases c
    JOIN profesores pr ON pr.id = c.id_profesor
    JOIN personas p   ON p.id  = pr.id_persona
    JOIN aulas a      ON a.id  = c.id_aula
    JOIN asignaturas asig ON asig.id = c.id_asignatura
    ORDER BY c.anio_academico DESC, asig.nombre, c.grupo
"""

UPDATE_CLASE = (
    "UPDATE clases SET id_profesor=?, id_aula=?, id_asignatura=?, "
    "anio_academico=?, grupo=? WHERE id=?"
)

DELETE_CLASE = (
    "DELETE FROM clases WHERE id = ?"
)

# ─── MATRÍCULAS ───────────────────────────────────────────────────────────────

INSERT_MATRICULA = (
    "INSERT INTO matriculas (id_alumno, anio_academico, fecha_matricula) VALUES (?, ?, ?)"
)

INSERT_MATRICULA_CLASE = (
    "INSERT INTO matricula_clase (id_matricula, id_clase) VALUES (?, ?)"
)

SELECT_MATRICULAS = """
    SELECT m.id, m.anio_academico, m.fecha_matricula,
           m.id_alumno, p.nombre || ' ' || p.apellidos AS nombre_alumno,
           al.numero_expediente
    FROM matriculas m
    JOIN alumnos al ON al.id = m.id_alumno
    JOIN personas p ON p.id  = al.id_persona
    ORDER BY m.anio_academico DESC, p.apellidos
"""

SELECT_MATRICULAS_ALUMNO = (
    "SELECT id, anio_academico, fecha_matricula FROM matriculas "
    "WHERE id_alumno = ? ORDER BY anio_academico DESC"
)

DELETE_MATRICULA = (
    "DELETE FROM matriculas WHERE id = ?"
)

SELECT_CLASES_DE_MATRICULA = """
    SELECT c.id, asig.nombre AS nombre_asignatura, c.grupo, c.anio_academico
    FROM matricula_clase mc
    JOIN clases c ON c.id = mc.id_clase
    JOIN asignaturas asig ON asig.id = c.id_asignatura
    WHERE mc.id_matricula = ?
    ORDER BY asig.nombre
"""

# ─── CALIFICACIONES ───────────────────────────────────────────────────────────

UPSERT_CALIFICACION = """
    INSERT INTO calificaciones
        (id_matricula, id_clase, id_tipo_convocatoria, nota, fecha_calificacion)
    VALUES (?, ?, ?, ?, ?)
    ON CONFLICT(id_matricula, id_clase, id_tipo_convocatoria)
    DO UPDATE SET nota=excluded.nota, fecha_calificacion=excluded.fecha_calificacion
"""

SELECT_ASIGNATURAS_ALUMNO_ANIO = """
    SELECT DISTINCT asig.id AS id_asignatura, asig.nombre AS asignatura,
           c.id AS id_clase, m.id AS id_matricula
    FROM matriculas m
    JOIN matricula_clase mc ON mc.id_matricula = m.id
    JOIN clases c           ON c.id  = mc.id_clase
    JOIN asignaturas asig   ON asig.id = c.id_asignatura
    WHERE m.id_alumno = ? AND m.anio_academico = ?
    ORDER BY asig.nombre
"""

SELECT_NOTA = """
    SELECT nota FROM calificaciones
    WHERE id_matricula=? AND id_clase=? AND id_tipo_convocatoria=?
"""

SELECT_ANIOS_ALUMNO = (
    "SELECT anio_academico FROM matriculas "
    "WHERE id_alumno=? ORDER BY anio_academico DESC"
)

SELECT_EXPORTAR_CALIFICACIONES = """
    SELECT p.apellidos || ', ' || p.nombre AS alumno,
           asig.nombre  AS asignatura,
           ? AS anio_academico,
           tc.nombre    AS convocatoria,
           tc.orden,
           COALESCE(CAST(cal.nota AS TEXT), 'S/C') AS nota
    FROM clases c
    JOIN asignaturas asig   ON asig.id = c.id_asignatura
    JOIN matricula_clase mc ON mc.id_clase = c.id
    JOIN matriculas m       ON m.id = mc.id_matricula
    JOIN alumnos al         ON al.id = m.id_alumno
    JOIN personas p         ON p.id  = al.id_persona
    CROSS JOIN tipos_convocatoria tc
    LEFT JOIN calificaciones cal
        ON cal.id_matricula=m.id AND cal.id_clase=c.id
        AND cal.id_tipo_convocatoria=tc.id
    WHERE c.id_asignatura = ? AND c.anio_academico = ?
    ORDER BY p.apellidos, p.nombre, tc.orden
"""
