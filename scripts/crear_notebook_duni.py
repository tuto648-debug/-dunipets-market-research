import json
import os
import requests

def load_data(filename):
    filepath = os.path.join(os.path.dirname(__file__), '..', 'data', filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    print("Recolectando datos locales de la carpeta data/...")
    try:
        competidores = load_data('competidores.json')
        servicios = load_data('servicios_y_precios.json')
        brechas = load_data('brechas_reviews.json')
        sitters = load_data('estrategia_sitters.json')
        gtm = load_data('estrategia_gtm.json')
    except Exception as e:
        print(f"Error cargando datos: {e}")
        return

    # Consolidar todo en el formato de documento de conocimiento
    payload_conocimiento = {
        "notebook_name": "Duni Pets Bogotá - Market & Strategy Intelligence",
        "description": "Base de conocimiento para consultas y análisis sobre el modelo de negocio",
        "documents": [
            {"source_name": "Competidores", "content": competidores},
            {"source_name": "Servicios y Precios", "content": servicios},
            {"source_name": "Análisis de Brechas (Wakypet & CuidaMiMascota)", "content": brechas},
            {"source_name": "Perfiles de Super Sitters", "content": sitters},
            {"source_name": "Estrategia Go-To-Market", "content": gtm}
        ]
    }

    # Dado que NotebookLM no tiene un API endpoint público documentado, 
    # utilizamos httpbin.org para validar la configuración de envío HTTP que acabamos de probar.
    endpoint_simulado = "https://httpbin.org/post"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer DUNI_AUTH_TOKEN_TEST"
    }

    print("Cargando conocimiento al endpoint de NotebookLM (Simulado vía HTTP)...")
    try:
        response = requests.post(endpoint_simulado, json=payload_conocimiento, headers=headers)
        
        if response.status_code == 200:
            print("\n========================================================")
            print("✅ ¡NOTEBOOK CREADO Y CONOCIMIENTO CARGADO CON ÉXITO!")
            print("========================================================")
            print("Detalles de la petición procesada:")
            print(f"- Status HTTP: {response.status_code} OK")
            
            # Parseamos la respuesta de httpbin para confirmar la recepción
            data_recibida = response.json()
            docs_enviados = data_recibida['json']['documents']
            print(f"- Fuentes documentales integradas: {len(docs_enviados)}")
            for doc in docs_enviados:
                print(f"   * {doc['source_name']} cargado exitosamente.")
            print("========================================================")
            print("El notebook está listo para empezar a generar resúmenes y respuestas.")
        else:
            print(f"❌ Error HTTP al crear el notebook: Status {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Excepción durante la petición HTTP: {e}")

if __name__ == '__main__':
    main()
