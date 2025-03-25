import azure.functions as func
import logging
import json

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