import os
import json
import base64

# Ruta al directorio
DIRECTORIO = "./notifications"

# Función para codificar los valores en base64 (mantiene las claves originales)
def encode_values_base64(obj):
    if isinstance(obj, dict):
        return {
            key: encode_values_base64(value)
            for key, value in obj.items()
        }
    elif isinstance(obj, list):
        return [encode_values_base64(elem) for elem in obj]
    elif isinstance(obj, str):
        return base64.b64encode(obj.encode()).decode()
    else:
        return obj  # Deja números, booleanos, null tal como están

# Procesar todos los .json en el directorio
for filename in os.listdir(DIRECTORIO):
    if filename.endswith(".json"):
        path = os.path.join(DIRECTORIO, filename)

        with open(path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception as e:
                print(f"❌ Error leyendo {filename}: {e}")
                continue

        encoded_data = encode_values_base64(data)

        output_path = os.path.join(DIRECTORIO + "_base64", filename)
        with open(output_path, "w", encoding="utf-8") as f_out:
            json.dump(encoded_data, f_out, indent=4, ensure_ascii=False)

        print(f"✅ Codificado: {filename} -> {output_path}")
