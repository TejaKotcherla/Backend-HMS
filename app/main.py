from fastapi import FastAPI
import app.init_admins as init_admins 
from .routers import auth, users, admin
from .database import Base, engine

app = FastAPI(title="Backend-HMS")

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
