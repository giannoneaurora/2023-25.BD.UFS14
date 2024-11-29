import azure.functions as func
import logging
import json
from main import  cerca_note, aggiungi_note, modifica_note, cancella_note, get_all_notes

app = func.FunctionApp()

@app.route(route="MyHttpTrigger", auth_level=func.AuthLevel.ANONYMOUS)
def MyHttpTrigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
     # Azione da eseguire (search, add, update, delete)
    action = req.params.get("action")
    if not action:
        return func.HttpResponse("Azione non specificata. \nUsa 'action=aggiungi', 'action=cerca', 'action=modifica', 'action=cancella', 'action=elenco'", status_code=400)

    # Azione: Cerca Note
    if action == "cerca":
        id_param = req.params.get("id")
        text_param = req.params.get("text")
        result = cerca_note(id_param=id_param, text_param=text_param)
        return func.HttpResponse(json.dumps(result, ensure_ascii=False), mimetype="application/json")

    # Azione: Aggiungi Nota
    if action == "aggiungi":
        try:
            note_text = req.params.get("text")
            if not note_text:
                raise ValueError("Il testo della nota è obbligatorio.")
            result = aggiungi_note(note_text)
            return func.HttpResponse(json.dumps(result, ensure_ascii=False), mimetype="application/json", status_code=201)
        except ValueError as e:
            return func.HttpResponse(str(e), status_code=400)

    # Azione: Modifica Nota
    if action == "modifica":
        try:
            note_id = int(req.params.get("id"))
            new_text = req.params.get("text")
            if not new_text:
                raise ValueError("Il nuovo testo della nota è obbligatorio.")
            result = modifica_note(note_id, new_text)
            return func.HttpResponse(json.dumps(result, ensure_ascii=False), mimetype="application/json")
        except (ValueError, TypeError):
            return func.HttpResponse("ID o testo non validi.", status_code=400)

    # Azione: Elimina Nota
    if action == "cancella":
        try:
            note_id = int(req.params.get("id"))
            result = cancella_note(note_id)
            return func.HttpResponse(json.dumps(result, ensure_ascii=False), mimetype="application/json")
        except (ValueError, TypeError):
            return func.HttpResponse("ID non valido.", status_code=400)

    # Azione: Elenco Completo
    if action == "elenco":
        result = get_all_notes()
        return func.HttpResponse(json.dumps(result, ensure_ascii=False), mimetype="application/json")

    # Azione non riconosciuta
    return func.HttpResponse("Azione non riconosciuta.", status_code=400)

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
