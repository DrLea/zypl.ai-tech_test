from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import event
from datetime import timedelta

from .routers import users, authors, albums, musics
from . import schemas, database, auth, crud, models
from .utils import email

app = FastAPI()

database.Base.metadata.create_all(bind=database.engine)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(authors.router, prefix="/authors", tags=["authors"])
app.include_router(albums.router, prefix="/albums", tags=["albums"])
app.include_router(musics.router, prefix="/musics", tags=["musics"])


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(database.get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(auth.get_current_user)):
    return current_user


@app.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return crud.create_user(db=db, user=user)


# def send_email_notification(follower_email, author_name, music_name):
#     email.send_email(
#         recipient_email=follower_email,
#         subject=f"New music from {author_name}",
#         body=f"Dear user,\n\nNew music '{music_name}' from {author_name} is now available!"
#     )


# def notify_followers_of_new_music(mapper, connection, target):
#     db = database.SessionLocal()
#     author = db.query(models.Author).filter(models.Author.id == target.author_id).first()
#     background_tasks = BackgroundTasks()
#     if author:
#         followers = author.fans
#         for follower in followers:
#             background_tasks.add_task(send_email_notification, follower.email, author.name, target.name)
#
#
# event.listen(models.Music, 'after_insert', notify_followers_of_new_music)
