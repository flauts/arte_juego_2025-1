#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# como correr:
# python script_txt.py --count 5

import os
import json
import base64
import random
import string
import argparse

def generar_contenido_base64(longitud=100) -> str:
    """Genera un string aleatorio y lo codifica en base64."""
    contenido = ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=longitud))
    contenido_bytes = contenido.encode('utf-8')
    base64_bytes = base64.b64encode(contenido_bytes)
    return base64_bytes.decode('utf-8')

def guardar_json_base64(index: int, output_dir: str):
    """Guarda un JSON con contenido base64 aleatorio."""
    os.makedirs(output_dir, exist_ok=True)
    filename = f"base64_{index}.txt"
    data = {
        "title": filename,
        "content": generar_contenido_base64()
    }
    ruta = os.path.join(output_dir, f"base64_{index}.json")
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Guardado: {ruta}")

def main():
    parser = argparse.ArgumentParser(description="Genera archivos JSON con contenido en base64.")
    parser.add_argument("--count", type=int, default=1, help="Número de archivos a generar.")
    parser.add_argument("--output", default="mensajes/base64_jsons", help="Directorio de salida.")
    args = parser.parse_args()

    for i in range(1, args.count + 1):
        guardar_json_base64(i, args.output)

if __name__ == "__main__":
    main()
