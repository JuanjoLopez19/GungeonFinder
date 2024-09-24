import logging

import elasticsearch.helpers as helpers
from elasticsearch import Elasticsearch

from . import gunsScrapper, itemsScrapper, shrinesScrapper, synergiesScrapper
from src.models.Guns import Guns
from src.models.items import Items
from src.models.Shrines import Shrines
from src.models.Synergies import Synergies


class Elastic:
    def __init__(self):
        self.client = Elasticsearch(
            "http://localhost:9200", http_auth=("elastic", "VvVZiNDR7s4nHajE7x90")
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

    def _setup_elastic_data(self):
        try:
            if self.test_connection():
                self.logger.info("Connection to ElasticSearch successful")
                if self.list_indexes() == {}:
                    self.logger.info("No indexes found")
                    self.create_index(
                        Guns.parse_index().get("name"), Guns.parse_index().get("body")
                    )
                    self.create_index(
                        Items.parse_index().get("name"), Items.parse_index().get("body")
                    )
                    self.create_index(
                        Synergies.parse_index().get("name"),
                        Synergies.parse_index().get("body"),
                    )
                    self.create_index(
                        Shrines.parse_index().get("name"),
                        Shrines.parse_index().get("body"),
                    )
                    self.logger.info("Indexes created")

                self.logger.info("Indexes found")
                if self.check_index("guns") == 0:
                    self.logger.debug("Guns index empty, adding data...")
                    gunsScrapper.get_data()
                    self.bulk_insert(gunsScrapper.bulk_insert())

                if self.check_index("items") == 0:
                    self.logger.debug("Items index empty, adding data...")
                    itemsScrapper.get_data()
                    self.bulk_insert(itemsScrapper.bulk_insert())

                if self.check_index("shrines") == 0:
                    self.logger.debug("Shrines index empty, adding data...")
                    shrinesScrapper.get_data()
                    self.bulk_insert(shrinesScrapper.bulk_insert())

                if self.check_index("synergies") == 0:
                    self.logger.debug("Synergies index empty, adding data...")
                    synergiesScrapper.get_data()
                    self.bulk_insert(synergiesScrapper.bulk_insert())

                self.logger.info("Data inserted")
                return True
            else:
                self.logger.error("Connection to ElasticSearch failed.")
                return False
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
            return False

    def check_index(self, index_name: str):
        return self.client.count(index=index_name).get("count")
