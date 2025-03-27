import azure.functions as func
import logging
import json
import requests

URL_HOSTAWAY_TOKEN = "https://api.hostaway.com/v1/accessTokens"

""" def obtener_acceso_hostaway():
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
 """
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Procesando la petición HTTP.')

    try:
        req_body = req.get_json()
        logging.info("Cuerpo recibido: " + json.dumps(req_body))
    except Exception as e:
        logging.error("Error al obtener el body: " + str(e))
        return func.HttpResponse("Error en el body", status_code=400)

    return func.HttpResponse("Funciona OK", status_code=200)