# -*- coding: utf-8 -*-

from aws_console_url_search.ui_def import handler
from aws_console_url_search.ui_init import ui
from rich import print as rprint

if __name__ == "__main__":
    items = handler(
        query="!@",
        ui=ui,
    )
    rprint(items)
