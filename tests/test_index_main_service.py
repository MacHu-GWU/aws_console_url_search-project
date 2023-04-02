# -*- coding: utf-8 -*-

import typing as T
import dataclasses
from rich import print as rprint
from aws_console_url_search.index.main_svc import (
    MainServiceIndex,
)
from aws_console_url_search.paths import dir_tests


class TestMainServiceIndex:
    index: MainServiceIndex

    @classmethod
    def setup_class(cls):
        from fixa.timer import DateTimeTimer

        cls.index = MainServiceIndex.new(
            dir_index=dir_tests.joinpath("tmp", "main_service_index")
        )

        # with DateTimeTimer():
        cls.index.build_index(rebuild=True)

    def test_search(self):
        test_cases = [
            ("ec2", "ec2"),
            ("elastic compute", "ec2"),
            ("oss", "aos"),
            ("opensearch", "aos"),
            ("open search", "aos"),
        ]
        for query_str, id in test_cases:
            assert self.index.search(query_str)[0].id == id


if __name__ == "__main__":
    from aws_console_url_search.tests import run_cov_test

    run_cov_test(__file__, "aws_console_url_search.index", preview=False)
