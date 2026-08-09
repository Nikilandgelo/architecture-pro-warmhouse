from fastapi import FastAPI

app = FastAPI(
    version="1.0",
    contact={
        "name": "Nikita Selivanov",
        "email": "niki_landgelo@outlook.com"
    },
)
