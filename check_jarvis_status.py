#!/usr/bin/env python3
"""
Script para verificar el estado del dataset JARVIS_DATA_1
"""

import abacusai
from datetime import datetime

def check_status():
    client = abacusai.ApiClient()
    fg_id = "355f6d6fc"
    
    print("=" * 80)
    print(f"🤖 VERIFICACIÓN DE ESTADO - JARVIS_DATA_1")
    print(f"⏰ Fecha y Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    try:
        # Obtener información del feature group
        fg = client.describe_feature_group(fg_id)
        
        print(f"\n📋 Información del Dataset:")
        print(f"   • Nombre: {fg.table_name}")
        print(f"   • ID: {fg.feature_group_id}")
        print(f"   • Creado: {fg.created_at}")
        
        # Verificar la versión más reciente
        if hasattr(fg, 'latest_feature_group_version') and fg.latest_feature_group_version:
            version = fg.latest_feature_group_version
            status = version.status if hasattr(version, 'status') else 'DESCONOCIDO'
            
            print(f"\n📊 Estado de la Versión:")
            print(f"   • Versión ID: {version.feature_group_version if hasattr(version, 'feature_group_version') else 'N/A'}")
            print(f"   • Estado: {status}")
            
            if status == 'COMPLETE':
                print(f"\n✅ ¡EXCELENTE! El dataset está COMPLETO y listo para usar.")
                print(f"\n🚀 Ahora puedes crear el chatbot JARVIS ejecutando:")
                print(f"   python /home/ubuntu/create_jarvis_chatbot.py")
                return True
                
            elif status == 'PENDING':
                print(f"\n⏳ El dataset todavía se está procesando...")
                print(f"   Por favor espera unos minutos más y vuelve a verificar.")
                return False
                
            elif status == 'FAILED':
                print(f"\n❌ ERROR: El procesamiento del dataset falló.")
                print(f"   Es posible que haya un problema con los documentos subidos.")
                print(f"   Por favor revisa los archivos o contacta al soporte.")
                return False
                
            else:
                print(f"\n⚠️ Estado inesperado: {status}")
                return False
        else:
            print(f"\n⚠️ No se pudo obtener información de la versión del dataset.")
            return False
            
    except Exception as e:
        print(f"\n❌ Error al verificar el estado:")
        print(f"   {str(e)}")
        return False
    
    finally:
        print("\n" + "=" * 80)

if __name__ == "__main__":
    is_ready = check_status()
    exit(0 if is_ready else 1)
