from fastapi import FastAPI
from .routers import auth, users, admin
from .database import Base, engine

app = FastAPI(title="Backend-HMS")

# Include routes
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {"message": "Backend-HMS is running successfully 🚀"}
