from sqlalchemy import Table, Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


author_fan_association = Table(
    'author_fan',
    Base.metadata,
    Column('author_id', Integer, ForeignKey('authors.id')),
    Column('fan_id', Integer, ForeignKey('users.id'))
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    favorites = relationship("Author", secondary=author_fan_association, back_populates="fans")


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    fans = relationship("User", secondary=author_fan_association, back_populates="favorites")
    albums = relationship("Album", back_populates="author")
    musics = relationship("Music", back_populates="author")


class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)

    author = relationship("Author", back_populates="albums")
    musics = relationship("Music", back_populates="album")


class Music(Base):
    __tablename__ = 'musics'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    album_id = Column(Integer, ForeignKey("albums.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)

    album = relationship("Album", back_populates="musics")
    author = relationship("Author", back_populates="musics")