# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import delete, match, upload, chat_history
from fastapi.staticfiles import StaticFiles
from routes import list_images


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/images", StaticFiles(directory="images"), name="images")
app.include_router(upload.router)
app.include_router(match.router)
app.include_router(list_images.router)
app.include_router(delete.router)
app.include_router(chat_history.router)
