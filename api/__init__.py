import asyncio

from fastapi import FastAPI, status

from .database import engine
from .middleware import allow_request_origins
from .models import Base
from .routes import all, stepwise
from .tasks import BackgroundListener

app = FastAPI()
app = allow_request_origins(app=app)

app.include_router(all.router)
app.include_router(stepwise.router)


@app.on_event("startup")
async def run_background_listener():
    """
        Runs background listener on startup
    """

    runner = BackgroundListener(save_to_database=False)
    Base.metadata.create_all(bind=engine)
    asyncio.create_task(runner.run_listener())


@app.get("/", status_code=status.HTTP_200_OK, tags=["Index"])
async def index():
    return {
        'message': "Welcome, to Zohali (https://github.com/GichanaMayaka/zohali)"
    }
