import azure.functions as func
import logging

app = func.FunctionApp()

@app.route(route="MyHttpTrigger", auth_level=func.AuthLevel.ANONYMOUS)
def MyHttpTrigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    azione = req.params.get('azione')  
    indice = req.params.get('indice da 1 a 6')  
    note_content = req.params.get('nota')  
    search_term = req.params.get('cerca')  

    if azione == 'aggiungi' and note_content:
        return func.HttpResponse(aggiungi_nota(note_content), status_code=200)
    elif azione == 'visualizza':
        return func.HttpResponse(visualizza_note(), status_code=200)
    elif azione == 'modifica' and indice and note_content:
        try:
            index = int(indice) - 1 
            return func.HttpResponse(modifica_nota(indice, note_content), status_code=200)
        except ValueError:
            return func.HttpResponse("Indice non valido", status_code=400)
    elif azione == 'elimina' and indice:
        try:
            indice = int(indice) - 1  
            return func.HttpResponse(elimina_nota(indice), status_code=200)
        except ValueError:
            return func.HttpResponse("Indice non valido", status_code=400)
    elif azione == 'cerca' and search_term:
        return func.HttpResponse(cerca_note(search_term), status_code=200)

    else:
        return func.HttpResponse(
            "Azioni disponibili: aggiungi, visualizza, modifica, elimina, cerca. Passa i parametri necessari.",
            status_code=400
        )

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
