## Project Zohali (Saturn)

This is an API that consumes [Kenya Power's](https://twitter.com/KenyaPower_Care) Tweets to check for scheduled/planned maintenance in Kenya.
Information extracted includes the Region, County, Area, Specific places, time as well as date of the planned incidents.
This API, consequently, makes the information publicly searchable, and analysable.

### Getting Started

Quickly run the project using [docker](https://www.docker.com/) and
[docker-compose](https://docs.docker.com/compose/):

```bash
    $ docker-compose up -d
```

### Directory Structure:

    -/zohali/
        init.sh
        serve.py
        README.md
        docker-compose.yml
        Dockerfile
        requirements.txt
        alembic.ini
        nginx.conf
        .dockerignore
        .gitignore
        -/api/
            __ini__.py
            auth.py
            database.py
            models.py
            schemas.py
            tasks.py
            utils.py
        -/app/
            __init__.py
            authenticators.py
            patterns.py
            runner.py
            tweetListeners.py
            utils.py
            -/images/
            -/image_texts/
        -/confs/
            __init__.py
            configs.py
        -/migrations/
        -/data/
            db.sql
        -/postman collection/
            zohali.postman_collection.json

### Configuration

Default configurations as shown below. Adjust accordingly

    ENCODING: = "utf-8"
    API_KEY:
    API_KEY_SECRET:
    BEARER_TOKEN:
    ACCESS_TOKEN:
    ACCESS_TOKEN_SECRET:
    SCREEN_NAME: = "KenyaPower_Care"
    TWEET_MODE: = "extended"
    TWEETS_COUNT: = 1500
    EXCLUDE_REPLIES: = True
    INCLUDE_RETWEETS: = False
    TIMEOUT: = 120
    POSTGRES_HOSTNAME:
    POSTGRES_USER:
    POSTGRES_PASSWORD:
    POSTGRES_PORT: = 5432
    POSTGRES_DATABASE_NAME:

### Endpoints

| METHOD | ENDPOINT |                          DESCRIPTION |
| ------ | :------: | -----------------------------------: |
| GET    |  /all/   | Get the previous 100 tracked records |
| GET    |  /prev/  |   Get the previous 5 tracked records |
| GET    |  /next/  |       Get the next 5 tracked records |


#### Query Parameters

