from elasticsearch import Elasticsearch, helpers
from datetime import datetime

TWEET = 'twitter_tweet'
USER = 'twitter_user'
INTERACTION = 'twitter_interaction'
CRAWLED = 'twitter_crawled'


class Elastic:
    def __init__(self, host="142.93.170.234", port=9200, user="elastic", password="changeme"):
        self.es = Elasticsearch(hosts=[{'host': host, 'port': port}], http_auth=(user, password))

    def is_crawled(self, username):
        res = self.es.count(index=CRAWLED, body={"query": {"bool": {"must": {"match": {"username": str(username)}}}}})["count"]
        return res > 0

    def store_crawled(self, crawled):
        self.store_crawleds([crawled])

    def store_crawleds(self, crawleds):
        self.create_index_crawled()
        print("Store ", len(crawleds), " crawled(s)")
        print(helpers.bulk(self.es, self.doc_from_dict(crawleds, CRAWLED)))

    def store_user(self, user):
        self.store_users([user])

    def store_users(self, users):
        self.create_index_user()
        print("Store ", len(users), " user(s)")
        print(helpers.bulk(self.es, self.doc_from_dict(users, USER)))

    def store_tweets(self, tweets):
        self.create_index_tweet()
        print("Store ", len(tweets), " tweet(s)")
        print(helpers.bulk(self.es, self.doc_from_dict(tweets, TWEET)))

    def store_interactions(self, interactions):
        if interactions is None:
            return
        self.create_index_interaction()
        print("Store ", len(interactions), " interaction(s)")
        print(helpers.bulk(self.es, self.doc_from_dict(interactions, INTERACTION)))

    @staticmethod
    def filter_keys(document, headers):
        return {key: document[key] for key in headers}

    @staticmethod
    def doc_from_dict(docs, index):
        for doc in docs:
            try:
                yield {
                    "_index": index,
                    "_type": "_doc",
                    "_id": f"{doc.id}",
                    "_source": vars(doc),
                }
            except StopIteration:
                return

    def create_index_user(self):
        user_body = {
            "mappings": {
                "properties": {
                    "id": {"type": "keyword"},
                    "name": {"type": "keyword"},
                    "username": {"type": "keyword"},
                    "bio": {"type": "text"},
                    "location": {"type": "keyword"},
                    "url": {"type": "text"},
                    "join_datetime": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss"},
                    "tweets": {"type": "integer"},
                    "following": {"type": "integer"},
                    "followers": {"type": "integer"},
                    "likes": {"type": "integer"},
                    "media": {"type": "integer"},
                    "private": {"type": "integer"},
                    "verified": {"type": "integer"},
                    "avatar": {"type": "text"},
                    "background_image": {"type": "text"},
                    "session": {"type": "keyword"},
                    "geo_user": {"type": "geo_point"},
                }
            },
            "settings": {
                "number_of_shards": 1
            }
        }
        self.es.indices.create(index=USER, body=user_body, ignore=400)

    def create_index_tweet(self):
        tweets_body = {
            "mappings": {
                "properties": {
                    "id": {"type": "long"},
                    "conversation_id": {"type": "long"},
                    "created_at": {"type": "long"},
                    "date": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss"},
                    "timezone": {"type": "keyword"},
                    "place": {"type": "keyword"},
                    "location": {"type": "keyword"},
                    "tweet": {"type": "text"},
                    "hashtags": {"type": "keyword", "normalizer": "hashtag_normalizer"},
                    "cashtags": {"type": "keyword", "normalizer": "hashtag_normalizer"},
                    "user_id_str": {"type": "keyword"},
                    "username": {"type": "keyword", "normalizer": "hashtag_normalizer"},
                    "name": {"type": "text"},
                    "profile_image_url": {"type": "text"},
                    "day": {"type": "integer"},
                    "hour": {"type": "integer"},
                    "link": {"type": "text"},
                    "retweet": {"type": "text"},
                    "essid": {"type": "keyword"},
                    "nlikes": {"type": "integer"},
                    "nreplies": {"type": "integer"},
                    "nretweets": {"type": "integer"},
                    "quote_url": {"type": "text"},
                    "video": {"type": "integer"},
                    "search": {"type": "text"},
                    "near": {"type": "text"},
                    "geo_near": {"type": "geo_point"},
                    "geo_tweet": {"type": "geo_point"},
                    "photos": {"type": "text"},
                    "user_rt_id": {"type": "keyword"},
                    "mentions": {"type": "keyword", "normalizer": "hashtag_normalizer"},
                    "source": {"type": "keyword"},
                    "user_rt": {"type": "keyword"},
                    "retweet_id": {"type": "keyword"},
                    "reply_to": {
                        "type": "nested",
                        "properties": {
                            "user_id": {"type": "keyword"},
                            "username": {"type": "keyword"}
                        }
                    },
                    "retweet_date": {"type": "keyword"},
                    "urls": {"type": "keyword"},
                    "translate": {"type": "text"},
                    "trans_src": {"type": "keyword"},
                    "trans_dest": {"type": "keyword"},
                }
            },
            "settings": {
                "number_of_shards": 1,
                "analysis": {
                    "normalizer": {
                        "hashtag_normalizer": {
                            "type": "custom",
                            "char_filter": [],
                            "filter": ["lowercase", "asciifolding"]
                        }
                    }
                }
            }
        }
        self.es.indices.create(index="twitter_tweet", body=tweets_body, ignore=400)

    def create_index_interaction(self):
        interaction_body = {
            "mappings": {
                "properties": {
                    "twittos_a": {"type": "keyword"},
                    "interaction": {"type": "keyword"},
                    "twittos_b": {"type": "keyword"},
                    "source": {"type": "keyword"}
                }
            },
            "settings": {
                "number_of_shards": 1
            }
        }
        self.es.indices.create(index=INTERACTION, body=interaction_body, ignore=400)

    def create_index_crawled(self):
        interaction_body = {
            "mappings": {
                "properties": {
                    "id": {"type": "keyword"},
                    "username": {"type": "keyword"},
                    "crawled_time": {"type": "date"},
                }
            },
            "settings": {
                "number_of_shards": 1
            }
        }
        self.es.indices.create(index=CRAWLED, body=interaction_body, ignore=400)

