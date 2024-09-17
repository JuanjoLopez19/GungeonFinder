from elasticsearch import Elasticsearch
import elasticsearch.helpers as helpers
import logging


class Elastic:
    def __init__(self):
        self.client = Elasticsearch(
            "http://localhost:9200", http_auth=("elastic", "root")
        )
        self.logger = logging.getLogger(__name__)
        self.setup_logger()

    def test_connection(self):
        return self.client.ping()

    def setup_logger(self):
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def create_index(self, index_name: str, properties: dict[str, dict[str, str]]):
        config = {
            "settings": {"number_of_shards": 1, "number_of_replicas": 1},
            "mappings": {"properties": properties},
        }
        res = self.client.indices.create(index=index_name, body=config, ignore=400)

        if "error" in res:
            self.logger.info(f"Index {index_name} already exists")
        else:
            self.logger.info(f"Index {index_name} created")

    def list_indexes(self):
        return self.client.indices.get_alias()

    def bulk_insert(self, data: list[dict]):
        helpers.bulk(self.client, data)

    def search(self, query: str = None):
        """
        Search method
        """

        res = self.client.search(
            body={
                "query": {
                    "multi_match": {
                        "type": "bool_prefix",
                        "fields": ["name", "description", "notes"],
                        "query": query,
                    }
                }
            },
            size=20,
        )
        return [hit["_source"] for hit in res["hits"]["hits"]]
