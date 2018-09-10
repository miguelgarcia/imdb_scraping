# IMDB Top movies by genre scraping

I made this project to try [Scrapy](https://scrapy.org/). The developed spider extracts the info from the top movies by genres listings on imdb.com to a Mongo
database.

The database is populated with three collections:

movie:

    {
        "_id" : ObjectId("5b95a75c252126484e38d032"),
        "movie_id" : "tt1431045",
        "title" : "A Movie",
        "year" : "2016",
        "duration" : "1h 48min",
        "genres" : [
            "Action",
            "Adventure",
            "Comedy"
        ],
        "images" : [
            "full/b859847a08e8dcb9ef96d4b15965d149caf2856f.jpg"
        ]
    }

actor:

    {
        "_id" : ObjectId("5b95a760252126484e38d05e"),
        "actor_id" : "nm1765324",
        "name" : "An Actor Name",
        "images" : [
            "full/fde484f2efb28cc8a51b765b0a26bcac435cecbb.jpg"
         ]
    }

movie_actor:

    {
        "_id" : ObjectId("5b95a75e252126484e38d037"),
        "actor_id" : "nm0417520",
        "character" : "A Character Name",
        "movie_id" : "tt0386064"
    }

Also, movies posters and actors pictures are stored in the `images` directory.

# Setup

Edit de `imdb_scraping/settings.py` to configure

    IMAGES_STORE = './images'
    MONGO_URI = 'mongodb://localhost:27017/'
    MONGO_DATABASE = 'movies'

    # If True, get all pages of each genre else only first page of each genre
    GENRE_ALL_PAGES = False

# Run

## Create and activate virtual env

    python3 -m venv venv
    . ./venv/bin/activate

## Install dependencies

    pip install -r requirements.txt

## Check spiders contracts

    scrapy check topmovies

## Scrap

    scrapy crawl topmovies