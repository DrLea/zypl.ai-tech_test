from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, crud, database


router = APIRouter()


@router.post("/", response_model=schemas.Album)
def create_album(album: schemas.AlbumCreate, db: Session = Depends(database.get_db)):
    return crud.create_album(db=db, album=album)


@router.get("/{album_id}", response_model=schemas.Album)
def read_album(album_id: int, db: Session = Depends(database.get_db)):
    db_album = crud.get_album(db, album_id=album_id)
    if db_album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    return db_album


@router.put("/{album_id}", response_model=schemas.Album)
def update_album(album_id: int, album_update: schemas.AlbumUpdate, db: Session = Depends(database.get_db)):
    db_album = crud.update_album(db, album_id=album_id, album_update=album_update)
    if db_album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    return db_album


@router.delete("/{album_id}", response_model=schemas.Album)
def delete_album(album_id: int, db: Session = Depends(database.get_db)):
    db_album = crud.delete_album(db, album_id=album_id)
    if db_album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    return db_album
