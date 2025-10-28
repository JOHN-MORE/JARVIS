import abacusai
import json

# Conectar con Abacus.AI
client = abacusai.ApiClient()

print("🔍 Buscando el dataset 'JARVIS_DATA_1'...\n")

# Buscar feature groups que contengan "JARVIS_DATA_1"
try:
    # Listar todos los feature groups
    feature_groups = client.list_feature_groups()
    
    # Buscar el que coincida con el nombre
    jarvis_data = None
    for fg in feature_groups:
        if fg.table_name and "JARVIS_DATA_1" in fg.table_name.upper():
            jarvis_data = fg
            break
    
    if jarvis_data:
        print(f"✅ Dataset encontrado!")
        print(f"   Nombre: {jarvis_data.table_name}")
        print(f"   ID: {jarvis_data.feature_group_id}")
        print(f"   Estado: {jarvis_data.status if hasattr(jarvis_data, 'status') else 'N/A'}")
        
        # Obtener más detalles
        fg_details = client.describe_feature_group(jarvis_data.feature_group_id)
        print(f"   Versión: {fg_details.feature_group_version if hasattr(fg_details, 'feature_group_version') else 'N/A'}")
        
        # Verificar si está listo para usar
        if hasattr(fg_details, 'status') and fg_details.status == 'COMPLETE':
            print(f"\n✅ El dataset está listo (COMPLETE)")
            
            # Ahora vamos a crear el chatbot JARVIS
            print(f"\n🤖 Creando el chatbot JARVIS...")
            
            # Primero necesito sugerir APIs para crear un chatbot RAG
            apis = client.suggest_abacus_apis("create RAG chatbot with document retriever using a dataset")
            print(f"\n📚 APIs sugeridas para crear chatbot RAG:")
            for api in apis[:5]:
                print(f"   - {api}")
            
            # Guardar información del dataset
            with open('/home/ubuntu/jarvis_dataset_info.json', 'w') as f:
                json.dump({
                    'feature_group_id': jarvis_data.feature_group_id,
                    'table_name': jarvis_data.table_name,
                    'status': fg_details.status if hasattr(fg_details, 'status') else 'N/A'
                }, f, indent=2)
            
            print(f"\n✅ Información del dataset guardada en jarvis_dataset_info.json")
            
        else:
            print(f"\n⚠️ El dataset existe pero NO está listo todavía")
            print(f"   Estado actual: {fg_details.status if hasattr(fg_details, 'status') else 'N/A'}")
            print(f"   Por favor espera a que el estado sea 'COMPLETE'")
    else:
        print("❌ No se encontró ningún dataset llamado 'JARVIS_DATA_1'")
        print("\n📋 Datasets disponibles en tu cuenta:")
        for fg in feature_groups[:10]:  # Mostrar solo los primeros 10
            print(f"   - {fg.table_name if fg.table_name else 'Sin nombre'} (ID: {fg.feature_group_id})")
        
        if len(feature_groups) > 10:
            print(f"   ... y {len(feature_groups) - 10} más")
        
        print("\n💡 El enlace que proporcionaste (https://drive.google.com/drive/my-drive) es tu vista personal")
        print("   Para compartir archivos de Google Drive, necesitas:")
        print("   1. Hacer clic derecho en el archivo/carpeta")
        print("   2. Seleccionar 'Compartir' o 'Obtener enlace'")
        print("   3. Cambiar permisos a 'Cualquier persona con el enlace'")
        print("   4. Copiar el enlace compartido")

except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

