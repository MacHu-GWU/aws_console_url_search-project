# -*- coding: utf-8 -*-

"""
A wrapper around the whoosh index object.
"""

import typing as T
import dataclasses
from pathlib_mate import Path
from whoosh import fields
from whoosh.index import open_dir, create_in, FileIndex


@dataclasses.dataclass
class SearchIndex:
    """
    Abstract class for whoosh search index.

    ::

        def build_index():
            ...

        def search():
            ...
    """
    schema: fields.SchemaClass = dataclasses.field()
    dir_index: Path = dataclasses.field()

    def __post_init__(self):
        self.dir_index = Path(self.dir_index)

    def get_index(self) -> FileIndex:
        if self.dir_index.exists():
            idx = open_dir(self.dir_index.abspath)
        else:
            self.dir_index.mkdir(parents=True, exist_ok=True)
            idx = create_in(dirname=self.dir_index.abspath, schema=self.schema)
        return idx

