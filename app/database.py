from sqlalchemy import create_engine

from config import configs

engine = create_engine(
    f'postgresql+psycopg2://{configs.POSTGRES_USER}:{configs.POSTGRES_PASSWORD}@{configs.POSTGRES_HOSTNAME}/{configs.POSTGRES_DATABASE_NAME}',
    echo=True,
    encoding="utf-8"
)
