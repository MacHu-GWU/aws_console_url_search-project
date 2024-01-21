# -*- coding: utf-8 -*-

from aws_console_url_search.dataset import (
    service_downloader,
    service_dataset,
    preprocess_query,
    region_downloader,
    region_dataset,
)
from rich import print as rprint

# rprint(service_downloader()[:10])
# rprint(region_downloader()[:10])

# query = "oss"
query = ""

if __name__ == "__main__":
    final_query = preprocess_query(query)
    # res = service_dataset.search(query=final_query, refresh_data=True)
    res = region_dataset.search(query=final_query, refresh_data=True)
    rprint(res)
