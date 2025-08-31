import aiosqlite

from backend.models.notes import NoteSchema

DB_PATH = "backend/database/db.db"

async def get_note_by_id(note_id: int):
    async with aiosqlite.connect(DB_PATH) as connect:
        connect.row_factory = aiosqlite.Row

        cursor = await connect.cursor()

        await cursor.execute("""
            SELECT * FROM notes
            WHERE id == ?
        """, (note_id,))

        row = await cursor.fetchone()

        return dict(row) if row else None

async def insert_note(note: NoteSchema):
    async with aiosqlite.connect(DB_PATH) as connect:
        await connect.execute("""
            CREATE TABLE IF NOT EXISTS notes(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                description TEXT)
        """)

        await connect.execute("""
            INSERT INTO notes(title, description) VALUES(?, ?)
        """, (note.title, note.description))

        await connect.commit()

async def delete_note_by_id(note_id: int):
    async with aiosqlite.connect(DB_PATH) as connect:
        await connect.execute("""
            DELETE FROM notes
            WHERE id == ?
        """, (note_id,))

        await connect.commit()

async def update_note_by_id(note_id: int, new_note: NoteSchema):
    async with aiosqlite.connect(DB_PATH) as connect:
        await connect.execute("""
            UPDATE notes
            SET title == ?, description == ?
            WHERE id == ?
        """, (new_note.title, new_note.description, note_id))

        await connect.commit()
