# -*- coding: utf-8 -*-

"""
A wrapper around the whoosh index object.
"""

import typing as T
import dataclasses
from pathlib_mate import Path
from whoosh import fields, qparser, query, sorting

from ..model import BaseModel, MainService, load_data
from ..paths import dir_main_service_index
from ..cache import cache
from .base import SearchIndex


class MainServiceSchema(fields.SchemaClass):
    id = fields.NGRAM(
        minsize=2,
        maxsize=10,
        stored=True,
        sortable=True,
        field_boost=3.0,
    )
    id_kw = fields.KEYWORD(stored=False)
    name = fields.NGRAM(
        minsize=2,
        maxsize=10,
        stored=True,
    )
    short_name = fields.NGRAM(
        minsize=2,
        maxsize=10,
        stored=True,
        field_boost=3.0,
    )
    description = fields.STORED()
    url = fields.STORED()
    regional = fields.BOOLEAN(stored=True)
    weight = fields.NUMERIC(
        sortable=True,
        stored=True,
    )
    search_terms = fields.NGRAM(
        minsize=2,
        maxsize=10,
        stored=False,
        field_boost=2.0,
    )
    has_sub_svc = fields.BOOLEAN(stored=True)


main_service_schema = MainServiceSchema()


@dataclasses.dataclass
class MainServiceDocument(BaseModel):
    id: str = dataclasses.field()
    name: str = dataclasses.field()
    url: str = dataclasses.field()
    regional: bool = dataclasses.field()
    weight: int = dataclasses.field()
    has_sub_svc: bool = dataclasses.field()
    short_name: T.Optional[str] = dataclasses.field(default=None)
    description: T.Optional[str] = dataclasses.field(default=None)


@dataclasses.dataclass
class MainServiceIndex(SearchIndex):
    @classmethod
    def new(
        cls,
        dir_index: Path = dir_main_service_index,
    ) -> "MainServiceIndex":
        return MainServiceIndex(
            schema=main_service_schema,
            dir_index=dir_index,
        )

    def _build_index(
        self,
        main_services: T.Optional[T.List[MainService]] = None,
    ):
        """
        Build Whoosh Index, add document.
        """
        if main_services is None:
            main_services = load_data()

        idx = self.get_index()
        writer = idx.writer()
        # writer = index.writer(procs=os.cpu_count()) # multi thread mode

        for main_service in main_services:
            document = {
                "id": main_service.id,
                "id_kw": main_service.id,
                "name": main_service.name,
                "short_name": main_service.short_name,
                "description": main_service.description,
                "url": main_service.url,
                "search_terms": " ".join(main_service.search_terms),
                "weight": main_service.weight,
            }

            new_document = {k: v for k, v in document.items() if bool(v)}
            new_document["has_sub_svc"] = bool(main_service.sub_services)
            new_document["regional"] = main_service.regional
            writer.add_document(**new_document)
        writer.commit()

    def build_index(
        self,
        main_services: T.Optional[T.List[MainService]] = None,
        rebuild: bool = False,
    ):
        if rebuild:
            self.dir_index.remove_if_exists()
        self._build_index(
            main_services=main_services,
        )

    def get_by_id(self, id: str) -> T.Optional[MainServiceDocument]:
        q = query.Term("id_kw", id)
        idx = self.get_index()
        with idx.searcher() as searcher:
            doc_list = [hit.fields() for hit in searcher.search(q, limit=1)]
        try:
            return MainServiceDocument.from_dict(doc_list[0])
        except IndexError:
            return None

    @cache.memoize(expire=3)
    def top_k(self, k: int = 20) -> T.List[MainServiceDocument]:
        q = query.Or([query.Term("regional", True), query.Term("regional", False)])
        idx = self.get_index()
        multi_facet = sorting.MultiFacet()
        multi_facet.add_field("weight", reverse=True)
        multi_facet.add_field("id")
        doc_list = list()
        with idx.searcher() as searcher:
            for hit in searcher.search(q, sortedby=multi_facet, limit=k):
                doc_list.append(MainServiceDocument.from_dict(hit.fields()))
        return doc_list

    @cache.memoize(expire=3600)
    def search(
        self,
        query_str: str,
        limit: int = 20,
    ) -> T.List[MainServiceDocument]:
        q = qparser.MultifieldParser(
            [
                "id",
                "name",
                "short_name",
                "search_terms",
            ],
            schema=self.schema,
        ).parse(query_str)
        index = self.get_index()
        multi_facet = sorting.MultiFacet()
        multi_facet.add_field("weight", reverse=True)
        multi_facet.add_field("id")
        doc_list = list()
        with index.searcher() as searcher:
            for hit in searcher.search(q, sortedby=multi_facet, limit=limit):
                doc_list.append(MainServiceDocument.from_dict(hit.fields()))

        # if the "id" starts with the query str, prioritize it
        doc_list_1 = list()
        doc_list_2 = list()
        for doc in doc_list:
            if doc.id.startswith(query_str):
                doc_list_1.append(doc)
            else:
                doc_list_2.append(doc)
        doc_list_1.extend(doc_list_2)
        return doc_list_1
