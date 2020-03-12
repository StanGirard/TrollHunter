from elasticsearch import Elasticsearch, helpers


class Elastic:
    def __init__(self, host="142.93.170.234", port=9200, user="elastic", password="changeme"):
        self.es = Elasticsearch(hosts=[{'host': host, 'port': port}], http_auth=(user, password))

    def store_user(self, user):
        self.store_users([user])

    def store_users(self, users):
        print("Store ", len(users), " user(s)")
        print(helpers.bulk(self.es, self.doc_from_dict(users, "twitter_user")))

    def store_tweets(self, tweets):
        print("Store ", len(tweets), " tweet(s)")
        print(helpers.bulk(self.es, self.doc_from_dict(tweets, "twitter_tweet")))

    def store_interactions(self, interactions):
        if interactions is None:
            return
        print("Store ", len(interactions), " interaction(s)")
        print(helpers.bulk(self.es, self.doc_from_dict(interactions, "twitter_interaction")))

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
