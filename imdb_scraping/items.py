import scrapy


class Actor(scrapy.Item):
    actor_id = scrapy.Field()
    name = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()

    def visit(self, visitor):
        visitor.visit_actor(self)

class Movie(scrapy.Item):
    movie_id = scrapy.Field()
    title = scrapy.Field()
    year = scrapy.Field()
    duration = scrapy.Field()
    genres = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()

    def visit(self, visitor):
        visitor.visit_movie(self)

class MovieActor(scrapy.Item):
    actor_id = scrapy.Field()
    character = scrapy.Field()
    movie_id = scrapy.Field()

    def visit(self, visitor):
        visitor.visit_movie_actor(self)
    