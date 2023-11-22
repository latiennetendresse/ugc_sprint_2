from clickhouse_driver import Client, errors as ch_errors

from src_etl.models.kafka_message import KafkaMessage
from src_etl.etl_settings import ClickHouseSettings
from src_etl.backoff import backoff


class ClickHouseWriter:
    def __init__(self, click_config: ClickHouseSettings):
        self.click_config = click_config
        self.client = None

    @backoff(error=(ch_errors.NetworkError, EOFError), start_sleep_time=2)
    def connect(self):
        self.client = Client(host=self.click_config.clickhouse_host)
        self.client.execute('SHOW DATABASES')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.client:
            self.client.close()

    def write_data(self, messages: list[KafkaMessage]):
        if not self.client:
            self.connect()
        if self.client:
            self.client.execute(
                'INSERT INTO default.movie_views (user_id, film_id, viewed_frame) VALUES',
                (
                    (
                        message.user_id,
                        message.film_id,
                        message.viewed_frame,
                    )
                    for message in messages
                ),
            )
