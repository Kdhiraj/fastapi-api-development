from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server is starting...")
    await init_db()
    yield
    print("Server is shutting down...")


version = "v1"
app = FastAPI(
    title="Book Management API",
    version=version,
    description="An API to manage a collection of books.",
    lifespan=lifespan,
)


app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
