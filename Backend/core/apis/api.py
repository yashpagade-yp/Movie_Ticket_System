from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.apis.routers.user_router import user_router
from core.database.database import connect_to_mongo, close_mongo_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to MongoDB
    await connect_to_mongo()
    yield
    # Shutdown: Close connection
    await close_mongo_connection()


app = FastAPI(title="Movie Ticket System API", lifespan=lifespan)

# CORS middleware - Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to Movie Ticket System API"}


# User Routes - Register, Login, Forgot Password, Reset Password
app.include_router(user_router, prefix="/users", tags=["Users"])
