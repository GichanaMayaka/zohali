from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def allow_request_origins(app: FastAPI) -> FastAPI:
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["GET"],
        allow_headers=["*"]
    )

    return app
