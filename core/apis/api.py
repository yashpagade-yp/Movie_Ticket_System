from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.apis.routers.user_router import user_router
from core.apis.routers.movie_router import movie_router
from core.apis.routers.theater_router import theater_router
from core.apis.routers.showtime_router import showtime_router
from core.apis.routers.booking_router import booking_router
from core.database.database import connect_to_mongo, close_mongo_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to MongoDB
    await connect_to_mongo()
    yield
    # Shutdown: Close connection
    await close_mongo_connection()


app = FastAPI(title="Movie Ticket System API", lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Welcome to Movie Ticket System API"}


app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(movie_router, prefix="/movies", tags=["Movies"])
app.include_router(theater_router, prefix="/theaters", tags=["Theaters"])
app.include_router(showtime_router, prefix="/showtimes", tags=["Showtimes"])
app.include_router(booking_router, prefix="/bookings", tags=["Bookings"])
