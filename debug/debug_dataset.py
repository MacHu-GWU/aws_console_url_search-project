# -*- coding: utf-8 -*-

from aws_console_url_search.dataset import downloader, dataset, preprocess_query
from rich import print as rprint

# docs = downloader()
# for doc in docs[:10]:
#     rprint(doc)

query = "oss"

if __name__ == "__main__":
    final_query = preprocess_query(query)
    res = dataset.search(query=final_query, refresh_data=True)
    rprint(res)
