from pydantic import BaseModel, EmailStr
from typing import List, Optional, Any


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: int
    favorites: List['Author'] = []

    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    name: str


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    fans: List[UserBase] = []  # Must be User but gives Cyclic Error
    albums: List['AlbumBase'] = []
    musics: List['MusicBase'] = []

    class Config:
        from_attributes = True


class AlbumBase(BaseModel):
    name: str


class AlbumCreate(AlbumBase):
    author_id: int


class AlbumUpdate(AlbumBase):
    pass


class Album(AlbumBase):
    id: int
    author: AuthorBase
    musics: List['MusicCreate'] = []

    class Config:
        from_attributes = True


class MusicBase(BaseModel):
    name: str


class MusicCreate(MusicBase):
    album_id: int
    author_id: int


class MusicUpdate(MusicBase):
    pass


class Music(MusicBase):
    id: int
    album: AlbumBase
    author: AuthorBase

    class Config:
        from_attributes = True

