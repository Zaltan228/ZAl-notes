from fastapi import APIRouter, HTTPException, status

from backend.database import db_handler as handler
from backend.models.notes import NoteSchema

router = APIRouter(
    tags=["notes"],
    prefix="/notes"
)

@router.post("/create", summary="Creates a note")
async def create_note(note: NoteSchema):
    await handler.insert_note(note)

    return note

@router.post("/delete/{id}", summary="Deletes the note by its id")
async def delete_note_by_id(id: int):
    await handler.delete_note_by_id(id)

    return {"message": "successfully deleted"}

@router.put("/update/{id}")
async def update_note_by_id(id: int, new_note: NoteSchema):
    existing_note = await handler.get_note_by_id(id)

    if not existing_note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note by id: {id} not found"
        )

    try:
        existing_note = NoteSchema(**existing_note)
        update_data = new_note.model_dump(exclude_unset=True)
        updated_note = existing_note.model_copy(update=update_data)
        
        await handler.update_note_by_id(id, updated_note)
        
        return updated_note
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error while filling the note: {str(e)}"
        )
    