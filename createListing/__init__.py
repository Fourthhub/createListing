import azure.functions as func
import logging
import json
import requests

MONDAY_API_URL = "https://api.monday.com/v2"
MONDAY_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjQwNDQwNjI3MywiYWFpIjoxMSwidWlkIjo2NTMxMzU2MCwiaWFkIjoiMjAyNC0wOC0zMFQxODoyMzozMS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MjUxMzkxNDksInJnbiI6ImV1YzEifQ.qyU9j29vOkMrXdb2_ymf-7rbV7yIeL17tFuMUr0yteA"
URL = "https://api.breezeway.io/"
URL_HOSTAWAY_TOKEN = "https://api.hostaway.com/v1/accessTokens"  # Define la URL para obtener el token de Hostaway
COMPANY_ID = 8172
fecha_hoy = ""
hostaway_token = "" 

def obtener_acceso_hostaway():
    global hostaway_token
    try:
        logging.info("Obteniendo token de Hostaway...")
        payload = {
            "grant_type": "client_credentials",
            "client_id": "81585",
            "client_secret": "0e3c059dceb6ec1e9ec6d5c6cf4030d9c9b6e5b83d3a70d177cf66838694db5f",
            "scope": "general"
        }
        headers = {'Content-type': "application/x-www-form-urlencoded", 'Cache-control': "no-cache"}
        response = requests.post(URL_HOSTAWAY_TOKEN, data=payload, headers=headers)
        response.raise_for_status()
        hostaway_token = response.json()["access_token"]
        logging.info("Token de Hostaway obtenido con éxito.")
    except requests.RequestException as e:
        logging.error(f"Error al obtener token de Hostaway: {str(e)}")
        raise

def crear_listing(nombreApartamento, direccion):
    logging.info(f"Creando listing con nombre: {nombreApartamento} y dirección: {direccion}")
    obtener_acceso_hostaway()
    endpoint = "https://api.hostaway.com/v1/listings"
    headers = {
        "Authorization": f"Bearer {hostaway_token}",
        "Content-Type": "application/json"
    }

    data = {
        "propertyTypeId": 1,
        "name": nombreApartamento,
        "externalListingName": nombreApartamento,
        "internalListingName": nombreApartamento,
        "description": "In a classic Bremerhaven house we rent out our apartment which has a living room, bed room and is close to all the restaurants and nightlife.",
        "houseRules": "Additional rules",
        "keyPickup": "Key pickup",
        "specialInstruction": "Any special instruction",
        "doorSecurityCode": "ddff8",
        "country": "Germany",
        "countryCode": "DE",
        "state": "Bremen",
        "city": "Bremerhaven",
        "street": "Schulstraße 7",
        "address": direccion,
        "publicAddress": "Bremerhaven, Bremen 27570, Germany",
        "zipcode": "27570",
        "price": 211.62,
        "starRating": 5,
        "weeklyDiscount": 0.71,
        "monthlyDiscount": 0.82,
        "propertyRentTax": 12,
        "guestPerPersonPerNightTax": 10,
        "guestStayTax": 12,
        "guestNightlyTax": 13,
        "guestBathroomsNumber": 2,
        "refundableDamageDeposit": 12.34,
        "personCapacity": 6,
        "maxChildrenAllowed": None,
        "maxInfantsAllowed": None,
        "maxPetsAllowed": None,
        "lat": 53.5403,
        "lng": 8.58936,
        "checkInTimeStart": 12,
        "checkInTimeEnd": 21,
        "checkOutTime": 11,
        "cancellationPolicy": "strict",
        "squareMeters": 10,
        "roomType": "entire_home",
        "bathroomType": "shared",
        "bedroomsNumber": 1,
        "bedsNumber": 1,
        "bedType": "real_bed",
        "bathroomsNumber": 1,
        "minNights": 1,
        "maxNights": 1125,
        "guestsIncluded": 3,
        "cleaningFee": 40.32,
        "priceForExtraPerson": 54.01,
        "instantBookable": 0,
        "instantBookableLeadTime": 1,
        "allowSameDayBooking": 2,
        "sameDayBookingLeadTime": 12,
        "contactName": "contactName",
        "contactSurName": "contactSurName",
        "contactPhone1": "contactPhone1",
        "contactPhone2": "contactPhone2",
        "contactLanguage": "contactLanguage",
        "contactEmail": "contactEmail@mail.com",
        "contactAddress": "contactAddress",
        "language": "en",
        "currencyCode": "USD",
        "timeZoneName": "Europe/Berlin",
        "wifiUsername": "un",
        "wifiPassword": "pass",
        "cleannessStatus": None,
        "cleaningInstruction": None,
        "cleannessStatusUpdatedOn": None,
        "homeawayPropertyName": "Beautiful and cozy apartment close to city center",
        "homeawayPropertyHeadline": "Beautiful and cozy apartment close to city center with a living room and bed room",
        "homeawayPropertyDescription": "In a classic Bremerhaven house we rent out our apartment which has a living room, bed room and is close to all the restaurants and nightlife.",
        "bookingcomPropertyName": "Beautiful and cozy apartment close to city center",
        "bookingcomPropertyRoomName": "Apartment",
        "bookingcomPropertyDescription": "In a classic Bremerhaven house we rent out our apartment which has a living room, bed room and is close to all the restaurants and nightlife.",
        "airbnbName": "Beautiful and cozy apartment close to city center",
        "airbnbSummary": "In a classic Bremerhaven house we rent out our apartment which has a living room, bed room and is close to all the restaurants and nightlife.",
        "invoicingContactName": "Name",
        "invoicingContactSurName": "Surname",
        "invoicingContactPhone1": "+11122334456",
        "invoicingContactPhone2": "+11122334456",
        "invoicingContactLanguage": "en",
        "invoicingContactEmail": "invoice@company.com",
        "invoicingContactAddress": "221B Baker Street",
        "invoicingContactCity": "London",
        "invoicingContactZipcode": "110011",
        "invoicingContactCountry": "UK"
    }

    try:
        response = requests.post(endpoint, headers=headers, data=json.dumps(data))
        logging.info(f"Respuesta Hostaway status: {response.status_code}")
        if response.status_code == 201:
            logging.info("Listing creado exitosamente.")
            return response.json()
        else:
            logging.error(f"Error al crear listing: {response.status_code} - {response.text}")
            return {"error": response.text}
    except Exception as e:
        logging.error(f"Excepción al llamar a Hostaway: {str(e)}")
        return {"error": "Fallo en la llamada a Hostaway"}

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Inicio de ejecución de función HTTP.')

    try:
        req_body = req.get_json()
        logging.info("JSON recibido correctamente.")
    except Exception as e:
        logging.error("Error al parsear JSON de entrada.")
        return func.HttpResponse("Body inválido", status_code=400)

    if "challenge" in req_body:
        logging.info("Challenge recibido desde webhook, devolviendo challenge.")
        return func.HttpResponse(json.dumps(req_body), mimetype="application/json")

    try:
        pulse_id = int(req_body["event"]["pulseId"])
        logging.info(f"pulseId recibido: {pulse_id}")
    except (KeyError, ValueError):
        logging.error("pulseId inválido o ausente.")
        return func.HttpResponse("pulseId inválido", status_code=400)

    headers = {
        "Authorization": MONDAY_API_KEY,
        "Content-Type": "application/json"
    }

    query = {
        "query": """
            query ($itemId: [ID!]) {
                items(ids: $itemId) {
                    name
                    column_values {
                        id
                        text
                        column {
                            id
                            title
                        }
                        value
                    }
                }
            }
        """,
        "variables": {
            "itemId": pulse_id
        }
    }

    try:
        logging.info("Lanzando query a Monday...")
        response = requests.post(MONDAY_API_URL, json=query, headers=headers)
        response.raise_for_status()
        data = response.json()
        logging.info("Respuesta de Monday recibida correctamente.")

        column_values = data["data"]["items"][0]["column_values"]

        nombre = None
        direccion = None

        for col in column_values:
            title = col.get("column", {}).get("title", "").strip().lower()
            if title == "nombre del apartamento":
                nombre = col.get("text", "").strip()
            elif title == "direccion exacta":
                direccion = col.get("text", "").strip()

        logging.info(f"Nombre: {nombre}, Dirección: {direccion}")

        if not nombre or not direccion:
            logging.warning("Faltan nombre o dirección en el item.")
            return func.HttpResponse("Faltan nombre o dirección", status_code=400)

        resultado = crear_listing(nombre, direccion)
        logging.info("Proceso completo, devolviendo resultado.")
        return func.HttpResponse(json.dumps(resultado), mimetype="application/json", status_code=200)

    except Exception as e:
        logging.error(f"Error procesando la función: {e}")
        return func.HttpResponse("Error interno", status_code=500)