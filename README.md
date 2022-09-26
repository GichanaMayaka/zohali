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
    - app/
        __init__.py
        auth.py
        config.py
        exceptions.py
        parser.py
        patterns.py
        transformer.py
        utils.py
        - images/
        - image_texts/

### Configuration
Default configurations as shown below. Adjust accordingly
    ENCODING:
    API_KEY:
    API_KEY_SECRET:
    BEARER_TOKEN:
    ACCESS_TOKEN:
    ACCESS_TOKEN_SECRET:
    SCREEN_NAME:
    TWEET_MODE:
    TWEETS_COUNT:
    EXCLUDE_REPLIES:
    INCLUDE_RETWEETS:
    TIMEOUT: