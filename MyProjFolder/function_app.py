import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()

@app.route(route="MyHttpTrigger", auth_level=func.AuthLevel.ANONYMOUS)
def MyHttpTrigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

import requests
from io import BytesIO

def scarica_pdf(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            if 'application/pdf' in response.headers.get('Content-Type', ''):
                contenuto_pdf_binario = BytesIO(response.content)
                return contenuto_pdf_binario
            else:
                print(f"Il contenuto scaricato da {url} non è un PDF.")
                return None
        else:
            print(f"Impossibile scaricare il PDF da {url}. Codice di stato: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Si è verificato un errore di rete: {e}")
        return None

    name = req.params.get('name')
    cognome = req.params.get('cognome')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        if cognome:
            return func.HttpResponse(f"Hello, {name} {cognome}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )