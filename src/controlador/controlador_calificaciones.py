import csv
from datetime import date
from src.modelo import gestor_bd as bd


class ControladorCalificaciones:
    """Intermediario entre la vista de calificaciones y la capa de datos."""

    def obtener_grid(self, id_alumno: int, anio_academico: str) -> list:
        """Devuelve datos listos para mostrar en la cuadrícula de calificaciones."""
        return bd.obtener_calificaciones_para_grid(id_alumno, anio_academico)

    def obtener_anios_alumno(self, id_alumno: int) -> list:
        return bd.obtener_anios_alumno(id_alumno)

    def obtener_convocatorias(self) -> list:
        return bd.obtener_tipos_convocatoria()

    def guardar_nota(self, id_matricula: int, id_clase: int,
                     id_tipo_convocatoria: int, nota_str: str) -> None:
        """Valida y guarda (o actualiza) una calificación."""
        nota_str = nota_str.strip()
        if nota_str == "" or nota_str == "-":
            # Nota vacía: no guardamos nada
            return
        try:
            nota = float(nota_str.replace(",", "."))
        except ValueError:
            raise ValueError(f"Nota inválida: '{nota_str}'. Debe ser un número entre 0 y 10")
        if nota < 0 or nota > 10:
            raise ValueError("La nota debe estar entre 0 y 10")
        fecha = date.today().isoformat()
        bd.guardar_calificacion(id_matricula, id_clase, id_tipo_convocatoria, nota, fecha)

    def exportar_a_csv(self, id_asignatura: int, anio_academico: str,
                        ruta_salida: str) -> int:
        """
        Exporta las calificaciones de una asignatura a CSV.
        Devuelve el número de filas escritas.
        """
        filas = bd.exportar_calificaciones_asignatura(id_asignatura, anio_academico)
        if not filas:
            raise ValueError("No hay calificaciones para exportar con los filtros seleccionados")

        with open(ruta_salida, "w", newline="", encoding="utf-8-sig") as f:
            escritor = csv.writer(f)
            escritor.writerow(["Año académico", "Convocatoria", "Alumno",
                               "Asignatura", "Nota"])
            for fila in filas:
                escritor.writerow([
                    fila["anio_academico"],
                    fila["convocatoria"] or "",
                    fila["alumno"],
                    fila["asignatura"],
                    fila["nota"],
                ])
        return len(filas)
