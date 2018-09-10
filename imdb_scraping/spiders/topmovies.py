import scrapy
import re
from imdb_scraping.items import Actor, Movie, MovieActor

class TopmoviesSpider(scrapy.Spider):
    name = 'topmovies'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/chart/top?ref_=nv_mv_250']

    def parse(self, response):
        """ This function parses the genres list.

            @url https://www.imdb.com/chart/top?ref_=nv_mv_250
            @returns items 0 0
            @returns requests 20 25
        """
        for link in response.xpath("//h3[contains(text(), 'Top Rated Movies by Genre')]/../ul/li/a"):
            genre = link.css('a::text').extract_first().strip()
            url = link.xpath('@href').extract_first().strip()
            self.log("Found genre {} at {}".format(genre, url))
            yield response.follow(url, self.parse_genre)

    def parse_genre(self, response):
        """ This function parses the movies list of a genre.

            @url https://www.imdb.com/search/title?genres=action&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=B54BBB9RK3QYTQNYM0TH&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_1
            @returns requests 50
        """
        for movie in response.css(".lister-item-header > a"):
            movie_name = movie.css('a::text').extract_first().strip()
            url = movie.xpath('@href').extract_first().strip()
            self.log("Found movie {}".format(movie_name))
            yield response.follow(url, self.parse_movie)
        next_page = response.css(".next-page").extract_first()
        if self.settings.getbool('GENRE_ALL_PAGES') and next_page is not None:
            yield response.follow(next_page, self.parse_genre)

    def parse_movie(self, response):
        """ This function parses a movie.

            @url https://www.imdb.com/title/tt1431045/?ref_=adv_li_tt
            @returns items 1
            @returns requests 1
            @scrapes movie_id title year duration genres image_urls
        """
        movie_id = re.search(r"title/(\w+)/", response.url).group(1)
        title = response.css("h1::text").extract_first().strip()
        year = response.css("#titleYear > a::text").extract_first().strip()
        duration = response.css("time::text").extract_first().strip()
        genres = response.css(
            ".title_wrapper > div[class=subtext] > a[href*=genre]::text").extract()
        poster = response.css(
            "div[class=poster] > a > img::attr(src)").extract_first()

        cast_page = response.css(
            "#titleCast > .see-more > a::attr(href)").extract_first()

        yield Movie(
            movie_id=movie_id,
            title=title,
            year=year,
            duration=duration,
            genres=genres,
            image_urls=[poster]
        )

        yield response.follow(cast_page, lambda resp: self.parse_cast(resp, movie_id))

    def parse_cast(self, response, movie_id=''):
        """ This function parses a movie cast page.

            @url https://www.imdb.com/title/tt1431045/fullcredits?ref_=tt_cl_sm#cast
            @returns items 20
            @returns requests 20
            @scrapes actor_id movie_id character
        """
        for actor in response.css(".cast_list > tr")[1:]:
            if len(actor.css("td")) < 2:
                continue
            actor_url = actor.css("td")[1].css("a::attr(href)").extract_first()
            actor_id = re.search(r"name/(\w+)/", actor_url).group(1)
            self.log("Found movie actor {} {}".format(movie_id, actor_id))
            yield response.follow(actor_url, lambda resp: self.parse_actor(resp, actor_id))

            character = actor.css("td.character > a::text").extract_first()
            if character is None:
                character = actor.css("td.character::text").extract_first()
            character = re.sub(r"\s+", " ", character).strip()
            yield MovieActor(
                actor_id=actor_id,
                character=character,
                movie_id=movie_id
            )

    def parse_actor(self, response, actor_id=''):
        """ This function parses a movie cast page.

            @url https://www.imdb.com/name/nm0005351/?ref_=ttfc_fc_cl_t1
            @returns items 1
            @returns requests 0
            @scrapes actor_id name image_urls
        """
        name = response.css("h1 > span::text").extract_first()
        self.log("Found actor {}".format(name))
        img_url = response.css("#name-poster::attr(src)").extract_first()
        image_urls = [img_url] if img_url is not None else []
        yield Actor(
            actor_id=actor_id,
            name=name,
            image_urls=image_urls
        )
