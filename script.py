#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import random
import os
import argparse
from datetime import datetime, timedelta

# Listas de ejemplo de profesores y cursos
PROFESORES = [
    "Julio Yarasca",
    "Jorge Gonzalez Reaño",
    "Carlos Williams",
    "Geraldo Colchado",
    "Violeta Reaño"
]

CURSOS = [
    "Compiladores",
    "Arquitectura de Computadoras",
    "Sistemas Operativos",
    "Cloud Computing",
    "Base de Datos 1",
    "Programación 3",
    "DBP"
]

# Plantillas de mensajes para cada tipo
TEMPLATES = {
    "whatsapp": [
        "¿Viste el grupo de WhatsApp de {curso}?",
        "Recordatorio: tenemos clase de {curso} en 10 minutos.",
        "Te mando el material de {curso} por WhatsApp."
    ],
    "correo": [
        "Adjunto el informe de {curso}.",
        "Buenas tardes, tengo dudas sobre la práctica de {curso}.",
        "Por favor, revisa el correo con la calificación de {curso}."
    ],
    "zoom": [
        "Invitación Zoom para la sesión de {curso} a las {hora}.",
        "Reunión de Zoom de {curso} programada mañana.",
        "Aquí está el link de Zoom para {curso}."
    ],
    "tarea": [
        "Tarea pendiente de {curso}: ejercicios 1 al 5.",
        "No olvides entregar la tarea de {curso} antes del viernes.",
        "La práctica de {curso} está pendiente en la plataforma."
    ],
    "deadline": [
        "Deadline del proyecto de {curso} para MAÑANA.",
        "Recuerda que el proyecto de {curso} vence el {fecha}.",
        "Último aviso: entrega del proyecto de {curso} pasado mañana."
    ]
}

def generar_mensaje(tipo: str) -> dict:
    """Genera un diccionario con profesor, curso y mensaje según el tipo."""
    profesor = random.choice(PROFESORES)
    curso = random.choice(CURSOS)
    plantilla = random.choice(TEMPLATES[tipo])
    
    # Generar valores dinámicos para hora o fecha si la plantilla los requiere
    hora = f"{random.randint(8,18)}:{random.choice(['00','30'])}"
    # Fecha aleatoria en formato D/M
    fecha_dt = datetime.now() + timedelta(days=random.randint(1,7))
    fecha = fecha_dt.strftime("%d/%m")
    
    mensaje = plantilla.format(curso=curso, hora=hora, fecha=fecha)
    return {
        "tipo": tipo,
        "profesor": profesor,
        "curso": curso,
        "mensaje": mensaje
    }

def guardar_json(data: dict, output_dir: str):
    """Guarda un diccionario en un archivo JSON dentro de output_dir."""
    os.makedirs(output_dir, exist_ok=True)
    # Contador basado en archivos existentes
    existentes = [f for f in os.listdir(output_dir) if f.startswith(data["tipo"])]
    indice = len(existentes) + 1
    filename = f"{data['tipo']}_{indice}.json"
    ruta = os.path.join(output_dir, filename)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Guardado: {ruta}")

def main():
    parser = argparse.ArgumentParser(
        description="Genera archivos JSON de distintos tipos de mensajes académicos."
    )
    parser.add_argument(
        "--tipo",
        choices=list(TEMPLATES.keys()) + ["aleatorio"],
        default="aleatorio",
        help="Tipo de mensaje a generar (o 'aleatorio')."
    )
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Número de mensajes a generar."
    )
    parser.add_argument(
        "--output",
        default="mensajes",
        help="Directorio donde se guardarán los archivos JSON."
    )
    args = parser.parse_args()

    for _ in range(args.count):
        tipo_elegido = random.choice(list(TEMPLATES.keys())) if args.tipo == "aleatorio" else args.tipo
        mensaje = generar_mensaje(tipo_elegido)
        guardar_json(mensaje, args.output)

if __name__ == "__main__":
    main()
