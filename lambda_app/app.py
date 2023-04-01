# -*- coding: utf-8 -*-

from chalice import Chalice
from aws_console_url_search.lbd import hello

app = Chalice(app_name="aws_console_url_search")


@app.lambda_function(name="hello")
def handler_hello(event, context):
    return hello.high_level_api(event, context)
