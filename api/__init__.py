import asyncio

from fastapi import FastAPI, Path, status

from .database import engine
from .routes import all, stepwise
from .tasks import BackgroundListener
from .models import Base


app = FastAPI()

app.include_router(all.router)
app.include_router(stepwise.router)


@app.on_event("startup")
async def run_background_listener():
    """
        Runs background listener on startup
    """
    runner = BackgroundListener()
    Base.metadata.create_all(bind=engine)
    asyncio.create_task(runner.run_listener())


@app.get("/{name}", status_code=status.HTTP_200_OK, tags=["Index"])
async def index(
    name: str = Path(default=None, regex=r"[a-zA-Z]", min_length=1),
):
    return {
        'message': f"Welcome, {name.capitalize()}"
    }
