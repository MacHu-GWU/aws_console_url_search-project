# -*- coding: utf-8 -*-

import typing as T
import dataclasses
from aws_console_url_search.model import (
    BaseModel,
    load_data,
)


@dataclasses.dataclass
class Model(BaseModel):
    id: str = dataclasses.field()
    name: T.Optional[str] = dataclasses.field(default=None)
    flag: bool = dataclasses.field(default=True)


class TestBaseModel:
    def test(self):
        data = {"id": "id-1", "flag": None, "undefined": 123}
        model = Model.from_dict(data)
        assert model.id == "id-1"
        assert model.name is None
        assert model.flag is True

        assert model.to_dict() == {"id": "id-1", "name": None, "flag": True}


def test_load_data():
    main_services = load_data()

    _ = main_services


if __name__ == "__main__":
    from aws_console_url_search.tests import run_cov_test

    run_cov_test(__file__, "aws_console_url_search.model", preview=False)
