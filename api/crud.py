from sqlalchemy.orm import Session
from . import models, schemas, auth


# User CRUD operations
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    user = get_user(db, user_id)
    if not user:
        return None
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if user:
        db.delete(user)
        db.commit()
        return user
    return None


def add_author_to_favorites(db: Session, user_id: int, author_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    author = db.query(models.Author).filter(models.Author.id == author_id).first()

    if user is None or author is None:
        return False

    if author in user.favorites:
        return True

    user.favorites.append(author)
    db.commit()
    return True


# Author CRUD operations
def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(name=author.name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def update_author(db: Session, author_id: int, author_update: schemas.AuthorUpdate):
    author = get_author(db, author_id)
    if not author:
        return None
    for key, value in author_update.dict(exclude_unset=True).items():
        setattr(author, key, value)
    db.commit()
    db.refresh(author)
    return author


def delete_author(db: Session, author_id: int):
    author = get_author(db, author_id)
    if author:
        db.delete(author)
        db.commit()
        return author
    return None


# Album CRUD operations
def get_album(db: Session, album_id: int):
    return db.query(models.Album).filter(models.Album.id == album_id).first()


def create_album(db: Session, album: schemas.AlbumCreate):
    db_album = models.Album(name=album.name, author_id=album.author_id)
    db.add(db_album)
    db.commit()
    db.refresh(db_album)
    return db_album


def update_album(db: Session, album_id: int, album_update: schemas.AlbumUpdate):
    album = get_album(db, album_id)
    if not album:
        return None
    for key, value in album_update.dict(exclude_unset=True).items():
        setattr(album, key, value)
    db.commit()
    db.refresh(album)
    return album


def delete_album(db: Session, album_id: int):
    album = get_album(db, album_id)
    if album:
        db.delete(album)
        db.commit()
        return album
    return None


# Music CRUD operations
def get_music(db: Session, music_id: int):
    return db.query(models.Music).filter(models.Music.id == music_id).first()


def create_music(db: Session, music: schemas.MusicCreate):
    db_music = models.Music(name=music.name, album_id=music.album_id, author_id=music.author_id)
    db.add(db_music)
    db.commit()
    db.refresh(db_music)
    return db_music


def update_music(db: Session, music_id: int, music_update: schemas.MusicUpdate):
    music = get_music(db, music_id)
    if not music:
        return None
    for key, value in music_update.dict(exclude_unset=True).items():
        setattr(music, key, value)
    db.commit()
    db.refresh(music)
    return music


def delete_music(db: Session, music_id: int):
    music = get_music(db, music_id)
    if music:
        db.delete(music)
        db.commit()
        return music
    return None
