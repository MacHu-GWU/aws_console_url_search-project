# -*- coding: utf-8 -*-

from aws_console_url_search.code.gen_code import (
    load_console_url_data,
    dump_console_url_data,
    normalize_console_url_data,
)

console_url_data = load_console_url_data()
console_url_data = normalize_console_url_data(console_url_data)
dump_console_url_data(console_url_data)
