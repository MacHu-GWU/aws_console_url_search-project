# -*- coding: utf-8 -*-

import typing as T
import json
import dataclasses

import sayt.api as sayt

from .paths import (
    dir_index,
    dir_cache,
    path_data_json,
)


fields = [
    sayt.IdField(name="id", stored=True),
    sayt.StoredField(name="service_name"),
    sayt.StoredField(name="sub_service_name"),
    sayt.StoredField(name="description"),
    sayt.StoredField(name="url"),
    sayt.StoredField(name="globally"),
    sayt.TextField(name="name_text", stored=True),
    sayt.NgramWordsField(name="name_ngram", stored=True, minsize=2, maxsize=6),
    sayt.NumericField(name="weight", stored=True, sortable=True, ascending=False),
]


@dataclasses.dataclass
class ServiceDocument:
    # fmt: off
    id: str = dataclasses.field()
    service_name: str = dataclasses.field()
    sub_service_name: T.Optional[str] = dataclasses.field()
    description: str = dataclasses.field()
    url: str = dataclasses.field()
    globally: bool = dataclasses.field()
    name_text: str = dataclasses.field()
    name_ngram: str = dataclasses.field()
    weight: int = dataclasses.field()
    # fmt: on

    @classmethod
    def new(
        cls,
        service_id: str,
        service_data: dict,
        sub_service_id: T.Optional[str] = None,
        sub_service_data: T.Optional[dict] = None,
    ):
        service_name = service_data.get("name", service_id)
        service_weight = service_data.get("weight", 1) * 10000
        globally = service_data.get("globally", False)
        if sub_service_id is None:
            id = service_id
            sub_service_name = None
            description = service_data.get("description", "No description")
            url = service_data["url"]
            name_ngram = service_name
            name_text = name_ngram
            sub_service_weight = 9999
        else:
            id = sub_service_id
            sub_service_name = sub_service_data.get("name", sub_service_id)
            description = sub_service_data.get("description", "No description")
            url = sub_service_data["url"]
            name_ngram = f"{service_name} {sub_service_name}"
            name_text = name_ngram
            sub_service_weight = sub_service_data.get("weight", 1)
        weight = service_weight + sub_service_weight
        return cls(
            id=id,
            service_name=service_name,
            sub_service_name=sub_service_name,
            description=description,
            url=url,
            globally=globally,
            name_text=name_text,
            name_ngram=name_ngram,
            weight=weight,
        )

    @classmethod
    def from_result(cls, doc: sayt.T_DOCUMENT):
        doc.setdefault("sub_service_name", None)
        return cls(**doc)


def downloader() -> T.List[sayt.T_DOCUMENT]:
    console_url_data = json.loads(path_data_json.read_text())
    docs = list()
    for service_id, service_data in console_url_data.items():
        doc = ServiceDocument.new(service_id, service_data)
        docs.append(doc)
        for sub_service_id, sub_service_data in service_data.get(
            "sub_services", {}
        ).items():
            sub_doc = ServiceDocument.new(
                service_id, service_data, sub_service_id, sub_service_data
            )
            docs.append(sub_doc)
    return [dataclasses.asdict(doc) for doc in docs]


index_name = "services"
dataset = sayt.DataSet(
    dir_index=dir_index,
    index_name=index_name,
    fields=fields,
    dir_cache=dir_cache,
    cache_key=index_name,
    cache_tag=index_name,
    cache_expire=24 * 60 * 60,
    downloader=downloader,
)


def preprocess_query(query: T.Optional[str]) -> str:  # pragma: no cover
    """
    Preprocess query, automatically add fuzzy search term if applicable.
    """
    delimiter = ".-_@+"
    if query:
        for char in delimiter:
            query = query.replace(char, " ")
        words = list()
        for word in query.split():
            if word.strip():
                word = word.strip()
                if len(word) == 1:
                    if word == "*":
                        words.append(word)
                else:
                    try:
                        if word[-2] != "~" and not word.endswith("!~"):
                            word = f"{word}~1/2"
                    except IndexError:
                        word = f"{word}~1/2"
                    words.append(word)
        if words:
            return " ".join(words)
        else:
            return "*"
    else:
        return "*"
