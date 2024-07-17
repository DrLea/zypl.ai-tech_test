from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, crud, database, auth, models


router = APIRouter()


@router.post("/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(database.get_db)):
    return crud.create_author(db=db, author=author)


@router.get("/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(database.get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@router.put("/{author_id}", response_model=schemas.Author)
def update_author(author_id: int, author_update: schemas.AuthorUpdate, db: Session = Depends(database.get_db)):
    db_author = crud.update_author(db, author_id=author_id, author_update=author_update)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@router.delete("/{author_id}", response_model=schemas.Author)
def delete_author(author_id: int, db: Session = Depends(database.get_db)):
    db_author = crud.delete_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return


@router.post("/authors/{author_id}/favorite", response_model=schemas.Author)
async def add_author_to_favorites(author_id: int, db: Session = Depends(database.get_db),
                                  current_user: models.User = Depends(auth.get_current_user)):
    if not crud.add_author_to_favorites(db, current_user.id, author_id):
        raise HTTPException(status_code=400, detail="Author not found or already in favorites")

    return db.query(models.Author).filter(models.Author.id == author_id).first()
