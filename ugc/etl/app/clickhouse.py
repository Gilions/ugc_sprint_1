from clickhouse_driver import Client
from migrations import MIGRATIONS
from settings import conf
from utility import backoff


class ClickHouseStreamClient:
    def __init__(self):
        self.migrations = MIGRATIONS
        self.client = self.get_client()

    @backoff()
    def get_client(self):
        return Client(host=conf.CH_HOST, port=conf.CH_PORT)

    def make_migrations(self):
        for row in MIGRATIONS:
            for sql in row.split(';'):
                if sql.strip():
                    self.make_request(sql=sql)

    def make_request(self, sql: str):
        self.client.execute(sql)

    def process(self):
        self.make_migrations()
