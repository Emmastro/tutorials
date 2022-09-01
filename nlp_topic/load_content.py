import time
import os

import pandas as pd
import numpy as np

import grequests
import requests
from requests.adapters import HTTPAdapter, Retry

from bs4 import BeautifulSoup

storage_options = None
#if os.getenv("SERVICE_NAME", -1) == -1:

storage_options = {'token': 'private/data-tests-352711-35f4c48c05ab.json'}

def to_pickle(batch: int):

    articles_batch = pd.read_parquet(f"gs://okapi/article_titles/articles_{batch}.parquet", storage_options=storage_options)

    articles_batch.to_pickle(f'gs://okapi/article_titles/articles_{batch}.pickle', storage_options=storage_options)


if __name__ == '__main__':

    for batch in range(10):
        start = time.time()
        print(f"processing batch {batch}")
        to_pickle(batch)
        print(f"Done processing {batch} in {time.time()-start}")
