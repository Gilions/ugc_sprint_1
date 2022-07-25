from clickhouse import ClickHouseStreamClient


if __name__ == '__main__':
    migrate = ClickHouseStreamClient()
    migrate.process()
