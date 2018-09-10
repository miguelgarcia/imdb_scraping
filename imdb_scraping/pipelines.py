# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
import logging

def _item_to_dict(item):
    data = dict(item)
    if 'image_urls' in data:
        del data['image_urls']
        data['images'] = [i['path'] for i in data['images']]
    return data

class MongoPipeline(object):
    """
    This pipeline item persists scraped items to three mongo collections, based
    on the item type:
     - movie
     - actor
     - movie_actor
    """

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        item.visit(self)
        return item

    def visit_movie(self, item):
        data = _item_to_dict(item)
        # insert only once
        db_movie = self.db['movie'].find_one({ 'movie_id': data['movie_id'] })
        if db_movie is None:
            db_movie_id = self.db['movie'].insert_one(data)
    
    def visit_actor(self, item):
        data = _item_to_dict(item)
        db_actor = self.db['actor'].find_one({ 'actor_id': data['actor_id'] })
        if db_actor is None:
            db_actor_id = self.db['actor'].insert_one(data)

    def visit_movie_actor(self, item):
        data = _item_to_dict(item)
        db_movie_actor = self.db['movie_actor'].find_one({
            'movie_id': data['movie_id'],
            'actor_id': data['actor_id'],
        })
        if db_movie_actor is None:
            self.db['movie_actor'].insert_one(data)
    