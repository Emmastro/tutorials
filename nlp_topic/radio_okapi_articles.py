import time

import pandas as pd
import numpy as np

import grequests
import requests
from requests.adapters import HTTPAdapter, Retry

from bs4 import BeautifulSoup


def process_article_data(batch: int):

    articles_batch = pd.read_parquet(f"gs://okapi/article_titles/articles_{batch}.parquet")

    website = "https://www.radiookapi.net"

    for chuck, articles in enumerate(np.array_split(articles_batch, 10)):
        if batch==0 and chuck==0: 
            continue

        articles = articles.reset_index()
        print(f"Starting batch {batch} chunk {chuck}")
        data = {
            'all_data': [],
            'title': [],
            'link': [],
            'date': [],
            'content': []
        }

        articles['urls'] = website + articles['link']

        session = requests.Session()
        retries = Retry(total=10, backoff_factor=2, status_forcelist=[500, 502, 503, 504],
                        raise_on_redirect=True,
                        raise_on_status=True)

        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))

        start = time.time()
        rs = (grequests.get(u, session=session) for u in articles['urls'])
        pages = grequests.map(rs)

        print(f"HTTP requests done in {time.time() - start}")

        for i, page in enumerate(pages):

            soup = BeautifulSoup(page.content, "html.parser")
            title = soup.find('h1', class_="page-header").get_text()

            date = soup.find_all('div', class_='pane-content')
            date = date[0].text.strip()
        
            content = soup.find_all('div', class_='field')
            content = content[0].text.strip()

            data['all_data'].append(soup.get_text())
            data['title'].append(title)
            data['link'].append(articles['urls'][i])
            data['date'].append(date)
            data['content'].append(content)

        articles_df = pd.DataFrame(data)

        articles_df.to_pickle(f'gs://okapi/content/articles_content_{batch}_{chuck}.pickle')


if __name__ == '__main__':

    for batch in range(10):
        start = time.time()
        print(f"processing batch {batch}")
        process_article_data(batch)
        print(f"Done processing {batch} in {time.time()-start}")
