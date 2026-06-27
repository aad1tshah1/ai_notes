from models.note import Note

"""
Responsibility:
Save and retrieve notes from Postgres.
"""

def save_note(db, transcript, notes):
    note = Note (
        transcript=transcript,
        summary=notes["summary"],
        key_points=notes["key_points"],
        action_items=notes["action_items"],
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def list_notes():
    pass

def get_note(note_id):
    pass

def delete_note(note_id):
    pass
