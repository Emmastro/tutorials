import time
import pandas as pd

import grequests
import requests
from requests.adapters import HTTPAdapter, Retry

from bs4 import BeautifulSoup

GOOGLE_APPLICATION_CREDENTIALS = 'private/data-tests-352711-35f4c48c05ab.json'


def process_data(batch: int):

    print(f"processing batch {batch}")

    base_url = "https://www.radiookapi.net/actualite?page="

    data = {
        'title': [],
        'link': [],
    }

    page_content = {
        'page_url': [],
        'n_articles': [],
        'content': [],
    }

    PAGE_PER_BATCH = 1000
    start, end = batch*PAGE_PER_BATCH, PAGE_PER_BATCH*(batch+1)

    urls = [base_url + str(i) for i in range(start, end)]
    session = requests.Session()
    retries = Retry(total=10, backoff_factor=1,
                    status_forcelist=[500, 502, 503, 504],
                    raise_on_redirect=True,
                    raise_on_status=True)

    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))

    start = time.time()
    response = (grequests.get(u, session=session) for u in urls)
    pages = grequests.map(response)
    print(f"HTTP requests done in {time.time() - start}")

    for i, page in enumerate(pages):

        soup = BeautifulSoup(page.content, "html.parser")
        content = soup.find_all('h2', class_="field-content")

        page_content['page_url'].append(urls[i])
        page_content['n_articles'].append(len(content))
        page_content['content'].append(soup.get_text())

        if content == []:
            continue

        for l in content:

            href = list(l.children)[0]
            data['title'].append(href.getText())
            data['link'].append(href.get('href', ''))
    
    articles_df = pd.DataFrame(data)
    page_df = pd.DataFrame(page_content)

  
    storage_options = {'token': GOOGLE_APPLICATION_CREDENTIALS}

    articles_df.to_parquet(
        f'gs://okapi/article_titles/articles_{batch}.parquet', storage_options=storage_options)
    page_df.to_parquet(
        f'gs://okapi/page_content/page_{batch}.parquet', storage_options=storage_options)



if __name__ == '__main__':

    for batch in range(10):
        start = time.time()
        print(f"processing batch {batch}")
        process_data(batch)
        print(f"Done processing {batch} in {time.time()-start}")
