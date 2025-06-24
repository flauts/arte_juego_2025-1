# content_generator.py

import random
from datetime import datetime, timedelta

PROFESORES = [
    "Julio Yarasca", "Jorge Gonzalez Reaño", "Carlos Williams",
    "Geraldo Colchado", "Violeta Reaño", "Angel Napa"
]

CURSOS = [
    "Compiladores", "Arquitectura de Computadoras", "Sistemas Operativos",
    "Cloud Computing", "Base de Datos 1", "Programación 3", "DBP",
    "ADA", "Teoría de la Computación", "Estadística 1"
]

# Plantillas de contenido según tema del archivo
TEMPLATES = {
    "algoritmos": [
        "Algoritmo de búsqueda binaria:\n\n1. Definir el arreglo ordenado.\n2. Calcular el punto medio.\n3. Comparar el valor buscado.\n4. Repetir hasta encontrarlo o terminar.",
        "Complejidad del algoritmo:\n- Mejor caso: O(1)\n- Promedio: O(log n)\n- Peor caso: O(log n)"
    ],
    "bd": [
        "Modelo entidad-relación:\n- Entidades: Alumno, Curso\n- Relaciones: Matricula (muchos a muchos)\n- Atributos: Nombre, Código, Nota",
        "Consulta SQL ejemplo:\n```sql\nSELECT nombre FROM alumnos WHERE nota > 14;\n```"
    ],
    "logica": [
        "Conectores lógicos:\n- AND: p ∧ q\n- OR: p ∨ q\n- NOT: ¬p\n\nTabla de verdad:\n\n| p | q | p ∧ q |\n|---|---|--------|\n| V | V |   V    |\n| V | F |   F    |",
        "Proposición compuesta: ¬(p ∧ q) ≡ ¬p ∨ ¬q (ley de De Morgan)"
    ],
    "historia": [
        "Resumen de la Revolución Francesa:\n- Inicio: 1789\n- Causas: crisis económica, desigualdad social\n- Eventos clave: Toma de la Bastilla, Declaración de Derechos",
        "Consecuencias:\n- Fin de la monarquía absoluta\n- Inicio del pensamiento liberal moderno"
    ],
    "default": [
        "Este es un apunte generado automáticamente.\nPuedes editarlo para agregar tus ideas principales.",
        "Profesor: {profesor}\nCurso: {curso}\nFecha: {fecha}\n\nNotas:\n- Punto importante 1\n- Punto importante 2"
    ]
}


def generate_note_content(filename: str) -> str:
    """Genera contenido extenso para una nota basado en el nombre del archivo."""

    base = filename.lower()
    fecha = datetime.now().strftime("%d/%m/%Y")
    profesor = random.choice(PROFESORES)
    curso = random.choice(CURSOS)

    # Elegir categoría
    if "algoritmo" in base:
        categoria = "algoritmos"
    elif "bd" in base or "base" in base or "sql" in base:
        categoria = "bd"
    elif "logica" in base:
        categoria = "logica"
    elif "historia" in base:
        categoria = "historia"
    else:
        categoria = "default"

    # Generar múltiples secciones
    bloques = []

    # Introducción
    bloques.append(f"Resumen del curso de {curso}.\nEste documento contiene apuntes desarrollados en clase por el profesor {profesor} el día {fecha}.\n")

    # Contenido repetido + mezclado
    for _ in range(20):  # Genera 20 párrafos extensos
        plantilla = random.choice(TEMPLATES.get(categoria, TEMPLATES["default"]))
        texto = plantilla
        if "{curso}" in texto or "{profesor}" in texto or "{fecha}" in texto:
            texto = texto.format(curso=curso, profesor=profesor, fecha=fecha)
        bloques.append(texto + "\n")

    # Conclusiones largas
    bloques.append("Conclusiones:\n" + "\n".join([
        "- Se comprendió a profundidad el tema expuesto.",
        "- Se identificaron patrones y estructuras comunes.",
        "- La participación del docente fue clave en aclarar dudas.",
        "- Se recomendó realizar prácticas adicionales para reforzar el aprendizaje.",
        "- El conocimiento adquirido será aplicado en evaluaciones futuras.\n"
    ]))

    # Glosario simulado
    bloques.append("Glosario de términos:\n" + "\n".join([
        "• Algoritmo: Conjunto ordenado de instrucciones para resolver un problema.",
        "• SQL: Lenguaje estructurado de consultas utilizado en bases de datos.",
        "• Inferencia lógica: Proceso de razonamiento que permite llegar a conclusiones.",
        "• Variable: Espacio en memoria para almacenar un dato identificable por nombre.",
        "• Entidad: Objeto distinguible del entorno sobre el cual se almacena información.\n"
    ]))

    # Fecha, profe y curso
    header = f"Apuntes: {filename.replace('_', ' ').title()}\nCurso: {curso}\nProfesor: {profesor}\nFecha: {fecha}\n\n"

    return header + "\n".join(bloques)
