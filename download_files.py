import json
import os

# Read all the Google Drive outputs
output_dir = "/home/ubuntu/.external_service_outputs"
medicina_file = f"{output_dir}/google_drive_tool_output_1761560801.json"
produccion_file = f"{output_dir}/google_drive_tool_output_1761560816.json"

file_ids = []

# Read medicina alternativa files
with open(medicina_file, 'r') as f:
    data = json.load(f)
    for file in data.get('files', []):
        if file['mimeType'] == 'application/pdf':
            file_ids.append(file['id'])

# Read producción musical files
with open(produccion_file, 'r') as f:
    data = json.load(f)
    for file in data.get('files', []):
        if file['mimeType'] == 'application/pdf':
            file_ids.append(file['id'])

print(json.dumps(file_ids))
