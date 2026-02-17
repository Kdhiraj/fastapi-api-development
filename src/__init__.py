from fastapi import FastAPI
from src.books.routes import book_router
from src.auth.routes import auth_router
from .middleware import register_middleware
from .errors import register_error_handlers
from src.reviews.routes import review_router
from src.tags.routes import tags_router
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
    # lifespan=lifespan,
)


register_error_handlers(app)
register_middleware(app)

app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["reviews"])
app.include_router(tags_router, prefix=f"/api/{version}/tags", tags=["tags"])
