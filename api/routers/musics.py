from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, BackgroundTasks
from sqlalchemy.orm import Session
from .. import schemas, crud, database, models
from ..utils import email

import csv


router = APIRouter()


@router.post("/", response_model=schemas.Music)
def create_music(music: schemas.MusicCreate,
                 db: Session = Depends(database.get_db),
                 background_tasks: BackgroundTasks = BackgroundTasks()):
    db_music = crud.create_music(db=db, music=music)
    author = db.query(models.Author).filter(models.Author.id == db_music.author_id).first()
    if author:
        followers = author.fans
        for follower in followers:
            background_tasks.add_task(email.send_email_notification, follower.email, author.name, db_music.name)
    return db_music


@router.get("/{music_id}", response_model=schemas.Music)
def read_music(music_id: int, db: Session = Depends(database.get_db)):
    db_music = crud.get_music(db, music_id=music_id)
    if db_music is None:
        raise HTTPException(status_code=404, detail="Music not found")
    return db_music


@router.put("/{music_id}", response_model=schemas.Music)
def update_music(music_id: int, music_update: schemas.MusicUpdate, db: Session = Depends(database.get_db)):
    db_music = crud.update_music(db, music_id=music_id, music_update=music_update)
    if db_music is None:
        raise HTTPException(status_code=404, detail="Music not found")
    return db_music


@router.delete("/{music_id}", response_model=schemas.Music)
def delete_music(music_id: int, db: Session = Depends(database.get_db)):
    db_music = crud.delete_music(db, music_id=music_id)
    if db_music is None:
        raise HTTPException(status_code=404, detail="Music not found")
    return db_music


@router.post("/populate_from_csv/")
async def populate_music_from_csv(file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    try:
        contents = await file.read()
        decoded_content = contents.decode('utf-8').splitlines()

        reader = csv.DictReader(decoded_content)
        musics = []
        for row in reader:
            value = row['name\talbum_id\tauthor_id']
            value = value.split('\t')
            music_data = schemas.MusicCreate(
                name=value[0],
                album_id=value[1],
                author_id=value[2]
            )
            music = models.Music(**music_data.dict())
            musics.append(music)

        db.add_all(musics)
        db.commit()
        return {"message": "Music data successfully populated from CSV"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to populate music data from CSV: {str(e)}")
