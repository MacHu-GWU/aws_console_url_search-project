# -*- coding: utf-8 -*-

from aws_console_url_search.model import load_data
from rich import print as rprint

service_list = load_data()
rprint(service_list)
