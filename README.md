# Music FastAPI Project

This is a FastAPI-based REST API service for managing music compositions, authors, and albums. The project includes features for user authentication, subscription notifications, and CSV file uploads.

## Features

1. **CRUD operations** for music compositions, authors, and albums.
2. **User authentication** using JWT tokens.
3. **Subscription notifications** via email for new tracks from followed authors.
4. **CSV file upload** to add multiple music compositions at once.
5. **Dockerized** for easy deployment.


## Launch
create .env file from .env_template(P.S You can find ready to use one from old commits)

docker compose up --build -d

go to localhost:8080/docs


## Populating from CSV
There is a template Music.csv 

Do not forget to check wheather Author and Album whose Id you pass in CSV already exist.

Steps:

1) Create Author

2) Create Album for that Author

3) Load Music from CSV with IDs of that Author and Album

4) Note: that notifications to subscribers are not sent via bulk create

## PS
I am working with FastAPI for 2 days. So there are still room for improvement, please leave PR and check for updates soon

## Refs
[Docs](https://fastapi.tiangolo.com/tutorial/)

[Git Template](https://github.com/tiangolo/fastapi)

