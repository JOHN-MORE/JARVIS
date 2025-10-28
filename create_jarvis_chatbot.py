#!/usr/bin/env python3
"""
Script para crear el chatbot JARVIS con RAG
"""

import abacusai
from datetime import datetime
import time

def create_jarvis_chatbot():
    client = abacusai.ApiClient()
    fg_id = "355f6d6fc"
    
    print("=" * 80)
    print(f"🤖 CREACIÓN DEL CHATBOT JARVIS")
    print(f"⏰ Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    try:
        # Paso 1: Verificar que el dataset esté listo
        print(f"\n📋 Paso 1: Verificando el estado del dataset...")
        fg = client.describe_feature_group(fg_id)
        
        if not hasattr(fg, 'latest_feature_group_version') or not fg.latest_feature_group_version:
            print(f"❌ Error: No se pudo obtener la versión del dataset.")
            return False
        
        version = fg.latest_feature_group_version
        status = version.status if hasattr(version, 'status') else 'DESCONOCIDO'
        
        if status != 'COMPLETE':
            print(f"❌ Error: El dataset NO está listo todavía (Estado: {status})")
            print(f"   Por favor ejecuta primero: python /home/ubuntu/check_jarvis_status.py")
            return False
        
        print(f"✅ Dataset verificado: {status}")
        
        # Paso 2: Buscar o crear un proyecto
        print(f"\n📁 Paso 2: Configurando el proyecto...")
        
        # Buscar proyectos existentes
        projects = client.list_projects()
        jarvis_project = None
        
        for project in projects:
            if hasattr(project, 'name') and 'JARVIS' in project.name.upper():
                jarvis_project = project
                print(f"✅ Proyecto encontrado: {project.name} (ID: {project.project_id})")
                break
        
        # Si no existe, crear uno nuevo
        if not jarvis_project:
            print(f"   Creando nuevo proyecto para JARVIS...")
            
            # Sugerir APIs para crear proyecto
            apis = client.suggest_abacus_apis("create a new project for chatbot")
            print(f"   APIs sugeridas: {[api.method for api in apis[:3]]}")
            
            # Crear proyecto
            jarvis_project = client.create_project(
                name="JARVIS Chatbot Project",
                use_case="CHAT_LLM"
            )
            print(f"✅ Proyecto creado: {jarvis_project.name} (ID: {jarvis_project.project_id})")
        
        project_id = jarvis_project.project_id
        
        # Paso 3: Crear Document Retriever
        print(f"\n📚 Paso 3: Creando Document Retriever...")
        
        # Verificar si ya existe un document retriever para este feature group
        doc_retrievers = client.list_document_retrievers()
        existing_retriever = None
        
        for dr in doc_retrievers:
            if hasattr(dr, 'feature_group_id') and dr.feature_group_id == fg_id:
                existing_retriever = dr
                print(f"✅ Document Retriever existente encontrado: {dr.document_retriever_id}")
                break
        
        if existing_retriever:
            doc_retriever_id = existing_retriever.document_retriever_id
        else:
            # Crear nuevo document retriever
            print(f"   Creando nuevo Document Retriever para JARVIS_DATA_1...")
            
            doc_retriever = client.create_document_retriever(
                project_id=project_id,
                name="JARVIS Document Retriever",
                feature_group_id=fg_id
            )
            doc_retriever_id = doc_retriever.document_retriever_id
            print(f"✅ Document Retriever creado: {doc_retriever_id}")
            
            # Esperar a que se entrene
            print(f"   Esperando a que el Document Retriever termine de indexarse...")
            max_wait = 300  # 5 minutos máximo
            wait_time = 0
            
            while wait_time < max_wait:
                dr_info = client.describe_document_retriever(doc_retriever_id)
                if hasattr(dr_info, 'latest_document_retriever_version'):
                    version_info = dr_info.latest_document_retriever_version
                    if hasattr(version_info, 'status'):
                        dr_status = version_info.status
                        if dr_status == 'COMPLETE':
                            print(f"✅ Document Retriever indexado correctamente")
                            break
                        elif dr_status == 'FAILED':
                            print(f"❌ Error: El Document Retriever falló")
                            return False
                
                print(f"   ⏳ Indexando... ({wait_time}s transcurridos)")
                time.sleep(10)
                wait_time += 10
            
            if wait_time >= max_wait:
                print(f"⚠️ Advertencia: Tiempo de espera agotado, pero continuando...")
        
        # Paso 4: Crear Agent
        print(f"\n🤖 Paso 4: Configurando el agente JARVIS...")
        
        # Sugerir APIs para crear agent
        apis = client.suggest_abacus_apis("create AI agent with custom instructions and document retriever")
        print(f"   APIs sugeridas: {[api.method for api in apis[:3]]}")
        
        # Configurar el system message de JARVIS
        system_message = """Eres JARVIS, un asistente inteligente experto en cuatro áreas principales:

💰 FINANZAS: Análisis financiero, inversiones, economía, mercados, criptomonedas
🏥 SALUD: Información médica, bienestar, nutrición, fitness, salud mental
💻 TECNOLOGÍA: Software, hardware, programación, inteligencia artificial, tendencias tecnológicas
🎵 MÚSICA: Teoría musical, géneros, historia, artistas, producción musical

PERSONALIDAD Y TONO:
- Eres formal y profesional, pero con un toque sutil de humor cuando es apropiado
- Tus respuestas son precisas, bien estructuradas y fáciles de entender
- Siempre incluyes referencias y citas de los documentos que consultas
- Eres proactivo y ofreces información adicional relevante

IDIOMA:
- Tu idioma principal es el ESPAÑOL
- Puedes traducir a otros idiomas si el usuario lo solicita explícitamente
- Mantienes la formalidad incluso en español

METODOLOGÍA:
1. Analiza cuidadosamente la pregunta del usuario
2. Busca información relevante en los documentos disponibles
3. Proporciona respuestas basadas en evidencia
4. Cita siempre las fuentes de los documentos
5. Ofrece contexto adicional cuando sea útil
6. Si no tienes información sobre algo, admítelo con honestidad

FORMATO DE RESPUESTAS:
- Usa encabezados (###) para organizar información compleja
- Utiliza listas con bullets (•) para enumerar puntos
- Incluye emojis relevantes para mejorar la legibilidad
- Al citar documentos, usa el formato: [Fuente: nombre_del_documento]

RESTRICCIONES:
- NO inventes información que no esté en los documentos
- NO proporciones consejos médicos o financieros definitivos sin advertencias
- NO uses un tono demasiado casual o informal
- SÍ admite cuando no tienes información suficiente

Recuerda: Tu objetivo es ser un asistente confiable, preciso y útil en estas cuatro áreas de expertise."""

        # Crear el agent
        try:
            agent = client.create_agent(
                project_id=project_id,
                name="JARVIS",
                memory="Conversacional con contexto de múltiples mensajes",
                system_message=system_message,
                agent_config={
                    "model": "gpt-4",
                    "temperature": 0.7,
                    "max_tokens": 2000,
                    "enable_document_retrieval": True
                }
            )
            agent_id = agent.agent_id
            print(f"✅ Agente JARVIS creado: {agent_id}")
        except Exception as e:
            print(f"⚠️ Error al crear agente (probando método alternativo): {str(e)}")
            
            # Método alternativo: crear usando chatbot/conversational agent
            apis = client.suggest_abacus_apis("create conversational agent or chatbot")
            print(f"   APIs alternativas: {[api.method for api in apis[:3]]}")
            agent_id = None
        
        # Paso 5: Crear Deployment
        print(f"\n🚀 Paso 5: Desplegando el chatbot JARVIS...")
        
        # Sugerir APIs para deployment
        apis = client.suggest_abacus_apis("create deployment for agent or chatbot")
        print(f"   APIs sugeridas: {[api.method for api in apis[:5]]}")
        
        # Intentar crear el deployment
        try:
            if agent_id:
                deployment = client.create_deployment(
                    project_id=project_id,
                    name="JARVIS Chatbot Deployment",
                    description="Asistente experto en Finanzas, Salud, Tecnología y Música",
                    agent_id=agent_id
                )
            else:
                # Deployment directo con document retriever
                deployment = client.create_deployment(
                    project_id=project_id,
                    name="JARVIS Chatbot Deployment",
                    description="Asistente experto en Finanzas, Salud, Tecnología y Música"
                )
            
            deployment_id = deployment.deployment_id
            print(f"✅ Deployment creado: {deployment_id}")
            
            # Obtener el token del deployment
            deployment_token = deployment.deployment_token if hasattr(deployment, 'deployment_token') else None
            
            print(f"\n" + "=" * 80)
            print(f"✅ ¡CHATBOT JARVIS CREADO EXITOSAMENTE!")
            print(f"=" * 80)
            print(f"\n📋 Información del Chatbot:")
            print(f"   • Nombre: JARVIS")
            print(f"   • Proyecto ID: {project_id}")
            print(f"   • Document Retriever ID: {doc_retriever_id}")
            if agent_id:
                print(f"   • Agent ID: {agent_id}")
            print(f"   • Deployment ID: {deployment_id}")
            if deployment_token:
                print(f"   • Deployment Token: {deployment_token}")
            
            print(f"\n🎯 Áreas de Expertise:")
            print(f"   • 💰 Finanzas")
            print(f"   • 🏥 Salud")
            print(f"   • 💻 Tecnología")
            print(f"   • 🎵 Música")
            
            print(f"\n🌐 Acceso al Chatbot:")
            print(f"   Puedes acceder a JARVIS desde la plataforma de Abacus.AI")
            print(f"   en la sección de Deployments o Agents")
            
            # Guardar información
            with open('/home/ubuntu/jarvis_deployment_info.txt', 'w') as f:
                f.write(f"JARVIS Chatbot - Información de Deployment\n")
                f.write(f"=" * 50 + "\n\n")
                f.write(f"Proyecto ID: {project_id}\n")
                f.write(f"Document Retriever ID: {doc_retriever_id}\n")
                if agent_id:
                    f.write(f"Agent ID: {agent_id}\n")
                f.write(f"Deployment ID: {deployment_id}\n")
                if deployment_token:
                    f.write(f"Deployment Token: {deployment_token}\n")
                f.write(f"\nFecha de creación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            print(f"\n💾 Información guardada en: /home/ubuntu/jarvis_deployment_info.txt")
            
            return True
            
        except Exception as e:
            print(f"❌ Error al crear deployment: {str(e)}")
            print(f"\n📝 Información para creación manual:")
            print(f"   • Proyecto ID: {project_id}")
            print(f"   • Document Retriever ID: {doc_retriever_id}")
            if agent_id:
                print(f"   • Agent ID: {agent_id}")
            
            import traceback
            print(f"\n🔍 Detalles del error:")
            traceback.print_exc()
            
            return False
        
    except Exception as e:
        print(f"\n❌ Error general: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        print(f"\n⏰ Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)

if __name__ == "__main__":
    success = create_jarvis_chatbot()
    exit(0 if success else 1)
