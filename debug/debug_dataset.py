# -*- coding: utf-8 -*-

from aws_console_url_search.dataset import downloader, dataset, preprocess_query
from rich import print as rprint

# docs = downloader()
# for doc in docs:
#     rprint(doc)

query = "ec2"

if __name__ == "__main__":
    final_query = preprocess_query(query)
    res = dataset.search(query=final_query)
    rprint(res)
