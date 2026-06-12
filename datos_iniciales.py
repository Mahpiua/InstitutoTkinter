"""
Carga de datos de ejemplo para el sistema de gestión del instituto.
Se ejecuta automáticamente en el primer arranque si la BD está vacía.
También puede lanzarse manualmente: python datos_iniciales.py
"""

from src.modelo.gestor_bd import (
    crear_bd, iniciar_carga,
    insertar_alumno, insertar_profesor, insertar_miembro_direccion,
    insertar_aula, insertar_asignatura, insertar_material,
    insertar_clase, insertar_matricula, guardar_calificacion,
    obtener_alumnos, obtener_profesores, obtener_aulas,
    obtener_asignaturas, obtener_clases, obtener_matriculas_alumno,
    obtener_tipos_convocatoria
)


def cargar_datos_iniciales() -> None:
    print("Insertando aulas…")
    for numero, cap, desc in [
        ("A101", 30, "Aula principal planta 1"),
        ("A102", 25, "Aula informática"),
        ("B201", 28, "Aula laboratorio"),
        ("B202", 30, "Aula idiomas"),
        ("GIM",  40, "Gimnasio"),
    ]:
        try:
            insertar_aula(numero, cap, desc)
        except ValueError:
            pass

    print("Insertando asignaturas…")
    for nombre, depto in [
        ("Matemáticas",          "Ciencias"),
        ("Lengua Castellana",    "Humanidades"),
        ("Historia de España",   "Ciencias Sociales"),
        ("Física y Química",     "Ciencias"),
        ("Inglés",               "Idiomas"),
        ("Educación Física",     "Deportes"),
        ("Tecnología",           "Tecnología"),
        ("Biología y Geología",  "Ciencias"),
        ("Economía",             "Ciencias Sociales"),
        ("Filosofía",            "Humanidades"),
    ]:
        try:
            insertar_asignatura(nombre, depto)
        except Exception:
            pass

    print("Insertando profesores…")
    for nombre, apellidos, dni, fnac, email, tlf, depto, esp in [
        ("Carlos", "García López",   "12345678A", "1975-03-15", "cgarcia@instituto.es",    "600111001", "Ciencias",         "Matemáticas"),
        ("Lucía",  "Martínez Ruiz",  "23456789B", "1980-07-22", "lmartinez@instituto.es",  "600111002", "Humanidades",      "Literatura"),
        ("Pedro",  "Fernández Díaz", "34567890C", "1972-11-05", "pfernandez@instituto.es", "600111003", "Ciencias Sociales","Historia"),
        ("Ana",    "Sánchez Torres", "45678901D", "1985-04-30", "asanchez@instituto.es",   "600111004", "Idiomas",          "Inglés"),
        ("Miguel", "López García",   "56789012E", "1978-09-18", "mlopez@instituto.es",     "600111005", "Tecnología",       "Informática"),
    ]:
        try:
            insertar_profesor(nombre, apellidos, dni, fnac, email, tlf, depto, esp)
        except ValueError:
            pass

    print("Insertando miembros de dirección…")
    for kwargs in [
        dict(nombre="Carmen", apellidos="Romero Blanco", dni="67890123F",
             fecha_nacimiento="1968-06-10", email="cromero@instituto.es",
             telefono="600000001", rol="director", es_profesor=False),
        dict(nombre="Carlos", apellidos="García López", dni="12345678A",
             fecha_nacimiento="1975-03-15", email="cgarcia@instituto.es",
             telefono="600111001", rol="jefe_estudios", es_profesor=True,
             departamento="Ciencias", especialidad="Matemáticas"),
        dict(nombre="Rosa", apellidos="Navarro Cano", dni="78901234G",
             fecha_nacimiento="1972-02-14", email="rnavarro@instituto.es",
             telefono="600000002", rol="secretario", es_profesor=False),
    ]:
        try:
            insertar_miembro_direccion(**kwargs)
        except ValueError:
            pass

    print("Insertando alumnos…")
    for nombre, apellidos, dni, fnac, email, tlf, exp in [
        ("Alejandro", "Pérez Gómez",  "80001111H", "2006-01-12", "aperez@correo.es",  "611000001", "EXP001"),
        ("Beatriz",   "Jiménez Mora", "80002222I", "2006-04-25", "bjimenez@correo.es", "611000002", "EXP002"),
        ("Carlos",    "Muñoz Vera",   "80003333J", "2007-08-03", "cmunoz@correo.es",   "611000003", "EXP003"),
        ("Diana",     "Ortega Pino",  "80004444K", "2006-11-19", "dortega@correo.es",  "611000004", "EXP004"),
        ("Eduardo",   "Ramos Cruz",   "80005555L", "2007-02-28", "eramos@correo.es",   "611000005", "EXP005"),
    ]:
        try:
            insertar_alumno(nombre, apellidos, dni, fnac, email, tlf, exp)
        except ValueError:
            pass

    print("Insertando clases…")
    profs = {f"{p['nombre']} {p['apellidos']}": p['id'] for p in obtener_profesores()}
    aulas = {a['numero']: a['id'] for a in obtener_aulas()}
    asigs = {a['nombre']: a['id'] for a in obtener_asignaturas()}

    for prof_key, aula_key, asig_key, anio, grupo in [
        ("Carlos García López",  "A101", "Matemáticas",       "2025-2026", "A"),
        ("Lucía Martínez Ruiz",  "A102", "Lengua Castellana", "2025-2026", "A"),
        ("Pedro Fernández Díaz", "B201", "Historia de España","2025-2026", "A"),
        ("Ana Sánchez Torres",   "B202", "Inglés",            "2025-2026", "A"),
        ("Miguel López García",  "A102", "Tecnología",        "2025-2026", "A"),
        ("Carlos García López",  "A101", "Física y Química",  "2025-2026", "A"),
    ]:
        prof_id = profs.get(prof_key)
        aula_id = aulas.get(aula_key)
        asig_id = asigs.get(asig_key)
        if all([prof_id, aula_id, asig_id]):
            try:
                insertar_clase(prof_id, aula_id, asig_id, anio, grupo)
            except ValueError:
                pass

    print("Insertando materiales…")
    aulas = {a['numero']: a['id'] for a in obtener_aulas()}
    for nombre, desc, cantidad, aula_key in [
        ("Proyector",        "Proyector Full HD",              2,  "A101"),
        ("Ordenador",        "Ordenador sobremesa i5",        15,  "A102"),
        ("Microscopio",      "Microscopio óptico 400x",        6,  "B201"),
        ("Balón baloncesto", "Balón de baloncesto talla 7",   10,  "GIM"),
        ("Pizarra digital",  "Pizarra digital interactiva",    1,  "B202"),
    ]:
        try:
            insertar_material(nombre, desc, cantidad, aulas.get(aula_key))
        except Exception:
            pass

    print("Insertando matrículas y calificaciones de ejemplo…")
    clases_bd = obtener_clases()
    ids_clases_anio = [c["id"] for c in clases_bd if c["anio_academico"] == "2025-2026"]
    convocatorias = {c["nombre"]: c["id"] for c in obtener_tipos_convocatoria()}
    notas_muestra = [7.5, 6.0, 8.0, 5.5, 9.0]

    for i, alumno in enumerate(obtener_alumnos()):
        mats = obtener_matriculas_alumno(alumno["id"])
        if not mats:
            try:
                id_mat = insertar_matricula(alumno["id"], "2025-2026", "2024-09-10", ids_clases_anio)
            except ValueError:
                id_mat = None
        else:
            id_mat = mats[0]["id"]

        if id_mat and ids_clases_anio:
            id_conv_1ev = convocatorias.get("1ª Evaluación")
            if id_conv_1ev:
                for id_clase in ids_clases_anio[:3]:
                    try:
                        guardar_calificacion(
                            id_mat, id_clase, id_conv_1ev,
                            notas_muestra[i % len(notas_muestra)],
                            "2024-12-20"
                        )
                    except Exception:
                        pass

    print("[OK] Datos de ejemplo cargados correctamente.")


if __name__ == "__main__":
    crear_bd()
    iniciar_carga()
    cargar_datos_iniciales()
    print("Credenciales de acceso:  admin / admin123")
