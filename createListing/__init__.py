import azure.functions as func
import logging
import json
import requests

def obtener_acceso_hostaway():
    try:
        payload = {
            "grant_type": "client_credentials",
            "client_id": "81585",
            "client_secret": "0e3c059dceb6ec1e9ec6d5c6cf4030d9c9b6e5b83d3a70d177cf66838694db5f",
            "scope": "general"
        }
        headers = {'Content-type': "application/x-www-form-urlencoded", 'Cache-control': "no-cache"}
        response = requests.post(URL_HOSTAWAY_TOKEN, data=payload, headers=headers)
        response.raise_for_status()
        return response.json()["access_token"]
    except requests.RequestException as e:
        logging.error(f"Error al obtener el token de acceso: {str(e)}")
        raise

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Procesando la petición HTTP.')

    # Intenta obtener el parámetro 'id' de la query string
    id_param = req.params.get('id')

    
    req_body = {}
    try:
        req_body = req.get_json()
        logging.info("Cuerpo recibido: " + json.dumps(req_body))
    except Exception as e:
        logging.error("Error al obtener el body: " + str(e))

    # Si 'id' no viene en la query, se extrae del body
    if not id_param:
        id_param = req_body.get('id')

    if id_param:
        response = {"message": f"ID recibido: {id_param}"}
        return func.HttpResponse(json.dumps(response), status_code=200, mimetype="application/json")
    else:
        response = {"error": "Por favor, proporciona un 'id' en la query string o en el body."}
        return func.HttpResponse(json.dumps(response), status_code=400, mimetype="application/json")