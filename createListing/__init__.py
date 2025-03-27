import azure.functions as func
import logging
import json
import requests

MONDAY_API_URL = "https://api.monday.com/v2"
MONDAY_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjQwNDQwNjI3MywiYWFpIjoxMSwidWlkIjo2NTMxMzU2MCwiaWFkIjoiMjAyNC0wOC0zMFQxODoyMzozMS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MjUxMzkxNDksInJnbiI6ImV1YzEifQ.qyU9j29vOkMrXdb2_ymf-7rbV7yIeL17tFuMUr0yteA"

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Procesando la petición HTTP.')

    try:
        req_body = req.get_json()
        logging.info("Cuerpo recibido: " + json.dumps(req_body))
    except Exception as e:
        logging.error("Error al obtener el body: " + str(e))
        return func.HttpResponse("Error en el body", status_code=400)

    # Responder a challenge (verificación inicial de webhook)
    if "challenge" in req_body:
        return func.HttpResponse(
            json.dumps(req_body),
            status_code=200,
            mimetype="application/json"
        )

    # Extraer el pulseId (itemId)
    try:
        pulse_id = req_body["event"]["pulseId"]
    except KeyError:
        logging.error("No se encontró pulseId en el payload.")
        return func.HttpResponse("pulseId no encontrado", status_code=400)

    # Consultar las columnas del item
    headers = {
        "Authorization": MONDAY_API_KEY,
        "Content-Type": "application/json"
    }
    query = {
        "query": f"""
        query {{
            items(ids: {pulse_id}) {{
                column_values {{
                    id
                    title
                    text
                }}
            }}
        }}
        """
    }

    try:
        response = requests.post(MONDAY_API_URL, json=query, headers=headers)
        response.raise_for_status()
        data = response.json()
        columns = data["data"]["items"][0]["column_values"]
        return func.HttpResponse(json.dumps(columns), mimetype="application/json", status_code=200)
    except Exception as e:
        logging.error("Error consultando a Monday: " + str(e))
        return func.HttpResponse("Error consultando Monday", status_code=500)