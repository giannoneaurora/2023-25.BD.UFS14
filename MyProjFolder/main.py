import pandas as pd
import os

data = {
    "ID": [1, 2, 3],
    "Nota": ["Questa è la prima nota", "Seconda nota di esempio", "Terza nota importante"]
}
notes_df = pd.DataFrame(data)

path = "note.csv"

if os.path.exists(path):
    notes_df = pd.read_csv(path)

def save_notes_to_file(notes_df, path):
    notes_df.to_csv(path, index=False)

def get_all_notes():
    return notes_df.to_dict(orient="records")

def cerca_note(id_param=None, text_param=None):
    filtered_notes = notes_df
    if id_param:
        try:
            filtered_notes = filtered_notes[filtered_notes["ID"] == int(id_param)]
        except ValueError:
            return {"error": "Il parametro ID deve essere un numero."}
    if text_param:
        filtered_notes = filtered_notes[filtered_notes["Nota"].str.contains(text_param, case=False, na=False)]
    if filtered_notes.empty:
        return {"error": "Nessuna nota trovata."}
    return filtered_notes.to_dict(orient="records")

def aggiungi_note(note_text):
    global notes_df
    new_id = notes_df["ID"].max() + 1 if not notes_df.empty else 1
    new_note = {"ID": new_id, "Nota": note_text}
    notes_df = pd.concat([notes_df, pd.DataFrame([new_note])], ignore_index=True)
    save_notes_to_file(notes_df, path)  # Salva la modifica
    return {"ID": int(new_note["ID"]), "Nota": new_note["Nota"]}

def modifica_note(note_id, new_text):
    global notes_df
    if note_id not in notes_df["ID"].values:
        return {"error": "Nota non trovata."}
    notes_df.loc[notes_df["ID"] == note_id, "Nota"] = new_text
    save_notes_to_file(notes_df, path)  # Salva la modifica
    return {"ID": int(note_id), "Nota": new_text}

def cancella_note(note_id):
    global notes_df
    if note_id not in notes_df["ID"].values:
        return {"error": "Nota non trovata."}
    notes_df = notes_df[notes_df["ID"] != note_id]
    save_notes_to_file(notes_df, path)  # Salva la modifica
    return {"message": f"Nota con ID {note_id} eliminata."}