from elasticsearch import Elasticsearch

class ElasticSearch:
    def __init__(self, host, port, index, doc_type):
        self.host = host
        self.port = port
        self.index = index
        self.es_type = doc_type

        self.es = Elasticsearch()

    def index(self, data):
        es_id = "%s-%s-%s-%s-%s" % (data.dateRef, data.time, data.x, data.y, 
                                 data.id)
        r = self.es.index(index=self.index, doc_type=self.doc_type, id=es_id,
                          body=data)
        return r

    def get_count(self, doc_type=None):
        return self.es.count(index=self.index, doc_type=self.doc_type)
