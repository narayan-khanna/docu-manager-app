from fastapi import FastAPI
from app.routers import ingest, qa, docs,metrics
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://docu-manager-fe:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest.router, prefix="/api/v1")
app.include_router(qa.router, prefix="/api/v1")
app.include_router(docs.router, prefix="/api/v1")
app.include_router(metrics.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "RAG Backend is running"}
