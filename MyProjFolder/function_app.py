import azure.functions as func
import logging
import json
from main import  cerca_note, aggiungi_note, modifica_note, cancella_note

app = func.FunctionApp()

@app.route(route="MyHttpTrigger", auth_level=func.AuthLevel.ANONYMOUS)
def MyHttpTrigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    action = req.params.get("action")
    if not action:
        guida = """Benvenuto nel gestore note. Ecco una guida per l'utilizzo:\nAzioni disponibili:
    1. Cerca Note
        - Descrizione: Cerca una nota utilizzando l'ID o parte del testo.
        - Parametri:
            - `action=cerca` 
            - `id=<ID della nota>` (opzionale)
            - `text=<Testo della nota>` (opzionale)
        - Esempio: `/MyHttpTrigger?action=cerca&id=1` , `/MyHttpTrigger?action=cerca&text=esempio`
    2. Aggiungi Nota
        - Descrizione: Aggiungi una nuova nota al sistema.
        - Parametri:
            - `action=aggiungi`
            - `text=<Testo della nuova nota>`
        - Esempio: `/MyHttpTrigger?action=aggiungi&text=Nuova%20nota`
    3. Modifica Nota
        - Descrizione: Modifica una nota esistente.
        - Parametri:
            - `action=modifica`
            - `id=<ID della nota>`
            - `text=<Nuovo testo della nota>`
        - Esempio: `/MyHttpTrigger?action=modifica&id=1&text=Nuova%20nota%20aggiornata`
    4. Elimina Nota
        - Descrizione: Elimina una nota esistente utilizzando l'ID.
        - Parametri:
            - `action=cancella`
            - `id=<ID della nota>`
        - Esempio: `/MyHttpTrigger?action=cancella&id=1`
    5. Elenco Completo
        - Descrizione: Recupera l'elenco completo delle note salvate.
        - Parametri:
            - `action=elenco`
        - Esempio: `/MyHttpTrigger?action=elenco`\nPer favore, assicurati di fornire i parametri corretti rispetto all'azione desiderata."""
        return func.HttpResponse(guida, mimetype="text/plain", status_code=400)

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
            logging.info(f"Parametro 'text' ricevuto: {note_text}")
            if not note_text:
                raise ValueError("Il testo della nota è obbligatorio.")
            result = aggiungi_note(note_text)
            return func.HttpResponse(json.dumps(result, ensure_ascii=False), mimetype="application/json", status_code=201)
        except ValueError as e:
            logging.error(f"Errore: {e}")
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
