notes = []

import uuid

def aggiungi_note(notes):
    nota = input("Scrivi la tua nota: ")
    if nota.strip():  # Ensure the note is not empty
        note_dict = {"id": str(uuid.uuid4()), "content": nota}
        notes.append(note_dict)  # Append the note as a dictionary
        print("Hai aggiunto una nota.")
    else:
        print("La nota non può essere vuota.")
def visualizza_note(notes):
    if len(notes) == 0:
        print("Non ci sono note salvate.")
        return
    print("\nLe tue note:")
    for i, note in enumerate(notes, 1):
        print(f"{i}. {note}")
    print()

def modifica_note(notes):
    if not notes:
        return
    try:
        index = int(input("Quale nota vuoi modificare? (inserisci il numero): ")) - 1
        if index >= 0 and index < len(notes):
            new_note = input("Scrivi la nuova nota: ")
            if new_note.strip():
                notes[index]['content'] = new_note
                print("Modifica aggiunta correttamente")
            else:
                print("La nota non può essere vuota")
        else:
            print("Numero non valido")
    except ValueError:
        print("Devi inserire un numero")

def cerca_note(notes):
    """Cerca tra le note"""
    if not notes:
        print("Non ci sono note salvate.")
        return

    search = input("Cerca una nota").lower()
    found = False
    print("\nRisultati della ricerca:")

    for i, note in enumerate(notes, 1):
        if search in note['content'].lower():  # Check within the note content
            print(f"{i}. {note['content']}")
            found = True

    if not found:
        print("Nessuna nota trovata")
    print()

def elimina_note(notes):
    visualizza_note(notes)
    if not notes:
        return

    try:
        index = int(input("Quale nota vuoi cancellare definitivamente? (inserisci il numero): ")) - 1
        if index >= 0 and index < len(notes):
            nota_da_cancellare = notes[index]
            conferma = input(f"Sei sicuro di voler cancellare definitivamente questa nota? '{nota_da_cancellare}' (s/n): ").lower()

            if conferma == 's':
                del notes[index]
                print(f"Nota cancellata")
            else:
                print("Cancellazione annullata")
        else:
            print("Numero non valido")
    except ValueError:
        print("Devi inserire un numero")
