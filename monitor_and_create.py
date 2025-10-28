#!/usr/bin/env python3
"""
Script de monitoreo automático que verifica el estado del dataset
y crea el chatbot JARVIS automáticamente cuando esté listo.
"""

import abacusai
import time
import subprocess
from datetime import datetime

def monitor_and_create():
    client = abacusai.ApiClient()
    fg_id = "355f6d6fc"
    check_interval = 30  # segundos
    max_wait = 1800  # 30 minutos máximo
    
    print("=" * 80)
    print(f"🤖 MONITOR AUTOMÁTICO - JARVIS")
    print(f"=" * 80)
    print(f"⏰ Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⚙️ Configuración:")
    print(f"   • Intervalo de verificación: {check_interval} segundos")
    print(f"   • Tiempo máximo de espera: {max_wait} segundos ({max_wait//60} minutos)")
    print(f"   • Dataset ID: {fg_id}")
    print("=" * 80)
    
    total_wait = 0
    check_count = 0
    
    try:
        while total_wait < max_wait:
            check_count += 1
            print(f"\n🔍 Verificación #{check_count} - {datetime.now().strftime('%H:%M:%S')}")
            print(f"   Tiempo transcurrido: {total_wait} segundos ({total_wait//60} minutos)")
            
            try:
                # Verificar el estado del feature group
                fg = client.describe_feature_group(fg_id)
                
                if hasattr(fg, 'latest_feature_group_version') and fg.latest_feature_group_version:
                    version = fg.latest_feature_group_version
                    status = version.status if hasattr(version, 'status') else 'DESCONOCIDO'
                    
                    print(f"   Estado actual: {status}")
                    
                    if status == 'COMPLETE':
                        print(f"\n✅ ¡EL DATASET ESTÁ LISTO!")
                        print(f"\n🚀 Iniciando creación automática del chatbot JARVIS...")
                        print("=" * 80)
                        
                        # Ejecutar el script de creación
                        result = subprocess.run(
                            ['python3', '/home/ubuntu/create_jarvis_chatbot.py'],
                            capture_output=False,
                            text=True
                        )
                        
                        if result.returncode == 0:
                            print("\n" + "=" * 80)
                            print("✅ ¡ÉXITO! JARVIS ha sido creado correctamente.")
                            print("=" * 80)
                            return True
                        else:
                            print("\n" + "=" * 80)
                            print("⚠️ Hubo un problema durante la creación del chatbot.")
                            print("   Por favor revisa los mensajes anteriores.")
                            print("=" * 80)
                            return False
                    
                    elif status == 'PENDING':
                        print(f"   ⏳ Todavía procesando... esperando {check_interval} segundos")
                        
                    elif status == 'FAILED':
                        print(f"\n❌ ERROR: El procesamiento del dataset falló.")
                        print(f"   Por favor revisa los archivos o contacta al soporte.")
                        return False
                    
                    else:
                        print(f"   ⚠️ Estado inesperado: {status}")
                
                else:
                    print(f"   ⚠️ No se pudo obtener información de la versión")
                
            except Exception as e:
                print(f"   ⚠️ Error al verificar estado: {str(e)}")
            
            # Esperar antes de la próxima verificación
            if total_wait + check_interval < max_wait:
                time.sleep(check_interval)
                total_wait += check_interval
            else:
                break
        
        # Si llegamos aquí, se acabó el tiempo de espera
        print(f"\n" + "=" * 80)
        print(f"⏰ TIEMPO DE ESPERA AGOTADO")
        print("=" * 80)
        print(f"\nEl dataset todavía no está listo después de {max_wait//60} minutos.")
        print(f"\nPosibles razones:")
        print(f"   1. Los documentos son muy grandes y requieren más tiempo")
        print(f"   2. Hay muchos archivos para procesar")
        print(f"   3. Puede haber un problema con el procesamiento")
        print(f"\nRecomendaciones:")
        print(f"   1. Espera un poco más y ejecuta: python /home/ubuntu/check_jarvis_status.py")
        print(f"   2. Si después de 1 hora sigue PENDING, contacta al soporte de Abacus.AI")
        print(f"   3. Verifica que los archivos se subieron correctamente")
        
        return False
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️ Monitoreo interrumpido por el usuario (Ctrl+C)")
        print(f"   Tiempo transcurrido: {total_wait} segundos")
        print(f"   Verificaciones realizadas: {check_count}")
        print(f"\n   Puedes reanudar el monitoreo ejecutando este script nuevamente:")
        print(f"   python /home/ubuntu/monitor_and_create.py")
        return False
    
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        print(f"\n⏰ Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)

if __name__ == "__main__":
    print("\n💡 CONSEJO: Puedes detener este script en cualquier momento con Ctrl+C")
    print("           y reanudar más tarde sin perder progreso.\n")
    
    time.sleep(2)  # Pausa breve para que el usuario lea el mensaje
    
    success = monitor_and_create()
    exit(0 if success else 1)
