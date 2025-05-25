from fastapi import FastAPI
from app.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://docu-manager-fe:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router, prefix="/auth")



