from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import engine, Base
from app.routers import auth_router, detection_router, audit_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="PhantomWeave API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(detection_router.router)
app.include_router(audit_router.router)


@app.get("/")
def root():
    return {"status": "PhantomWeave backend running"}