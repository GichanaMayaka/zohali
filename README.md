## Project Zohali (Saturn)
This is an API that consumes Kenya Power's Tweets to check for scheduled/planned maintenance in Kenya.
Information extracted includes the Region, County, Area, Specific places, time as well as date of the planned incidents.

Future developments include intergrating with a Twitter Bot.

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
        .dockerignore
        .gitignore
        -/api/
            __ini__.py
            auth.py
            config.py
            database.py
            models.py
            schemas.py
            tasks.py
            utils.py
        -/app/
            __init__.py
            auth.py
            config.py
            database.py
            exceptions.py
            parser.py
            patterns.py
            transformer.py
            utils.py
            -/images/
            -/image_texts/
        -/migrations

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
    TWEETS_COUNT: = 900
    EXCLUDE_REPLIES: = True
    INCLUDE_RETWEETS: = False
    TIMEOUT: = 120
    POSTGRES_HOSTNAME:
    POSTGRES_USER:
    POSTGRES_PASSWORD: 
    POSTGRES_PORT:
    POSTGRES_DATABASE_NAME: