import re

# Definir las rutas de los archivos
input_file_path = 'mysqlsampledatabase.sql'  # Cambia esto a la ruta de tu archivo de entrada
output_file_path = 'base_linda.sql'  # Cambia esto a la ruta de tu archivo de salida


with open(input_file_path, 'r', encoding='utf-8') as file:
    content = file.read()


corrected_content = re.sub(r"\\'", "''", content)

# Guardar el contenido corregido en un nuevo archivo
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(corrected_content)

print(f"Archivo corregido guardado en: {output_file_path}")
