from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import app.init_admins as init_admins
from .routers import auth, users, admin
from .database import Base, engine

app = FastAPI(title="Backend-HMS")

# ------------------------------------
# 🚀 Add CORS Middleware (REQUIRED FOR FLUTTER WEB)
# ------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.1.7:8000"],      # or set your domain here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await init_admins.init_admins() 
    
# Include routes
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {"message": "Backend-HMS is running successfully 🚀"}
