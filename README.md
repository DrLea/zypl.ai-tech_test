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


## PS
I am working with FastAPI for 2 days. So there are still room for improvement, please leave PR and check for updates soon

## Refs
[Docs](https://fastapi.tiangolo.com/tutorial/)

[Git Template](https://github.com/tiangolo/fastapi)

