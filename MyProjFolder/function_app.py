import azure.functions as func
import json
import logging

app = func.FunctionApp()

@app.route(route="MyHttpTrigger", auth_level=func.AuthLevel.ANONYMOUS)
def MyHttpTrigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    def main():
        notes = []  # Lista per salvare le note

        while True:
            print("\n=== 📝 Blocco Note ===")
            print("1.  Aggiungi nota")
            print("2.  Vedi note")
            print("3.  Modifica nota")
            print("4.  Elimina note")
            print("5.  Cerca")
            print("6.  Esci")

            scelta = input("\nCosa vuoi fare? (1-6): ")

            if scelta == '1':
                aggiungi_note(notes)
            elif scelta == '2':
                visualizza_note(notes)
            elif scelta == '3':
                modifica_note(notes)
            elif scelta == '4':
                elimina_note(notes)
            elif scelta == '5':
                cerca_note(notes)
            elif scelta == '6':
                print("\nArrivederci")
                break
            else:
                print("Scelta non valida")

    if __name__ == "__main__":
        main()

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
