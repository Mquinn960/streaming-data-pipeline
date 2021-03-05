import time
from datetime import datetime

from faust import App

from matching.term_cache_builder import TermCacheBuilder
from matching.matcher import Matcher
from data.database_record_writer import DatabaseRecordWriter

term_cache = {}
term_location = 'test_data/terms.csv'

matcher = None
writer = None

app = App(
    'app_main',
    broker='kafka://kafka:9091'
)

topic = app.topic(
    'input-csv',
    value_type=bytes,
    partitions=1,
)

@app.agent(topic)
async def read_topic(streams):
    async for payload in streams:
        match_records = matcher.match(payload, full_search=False)
        print("Message Received:", payload)
        if match_records['term_matches']:
            print("Matched Record:", match_records)
            writer.write_record(match_records)
        else:
            print("No Match Found.")
        print("Message Processed.")

def init_term_cache():

    global term_cache

    term_cache_builder = TermCacheBuilder()
    term_cache = term_cache_builder.build_term_cache(term_location)

def init_services():

    global matcher
    global writer

    matcher = Matcher(term_cache)
    writer = DatabaseRecordWriter()

if __name__ == '__main__':
    init_term_cache()
    init_services()
    app.main()
