# -*- coding: utf-8 -*-

import typing as T
import dataclasses
import zelfred.api as zf

from .dataset import ServiceDocument, dataset, preprocess_query
from .terminal import (
    terminal,
    format_shortcut,
    highlight_text,
    format_resource_type,
    format_key,
    format_value,
    format_key_value,
    remove_text_format,
    ShortcutEnum,
    SUBTITLE,
    SHORT_SUBTITLE,
)


# ------------------------------------------------------------------------------
# Item
# ------------------------------------------------------------------------------
@dataclasses.dataclass
class Item(zf.Item):
    pass


@dataclasses.dataclass
class InfoItem(zf.Item):
    pass


@dataclasses.dataclass
class ConsoleUrlItem(Item):
    @classmethod
    def from_doc(
        cls,
        doc: ServiceDocument,
        console_domain: str,
        aws_region: str,
    ):
        return cls(
            title=f"{doc.id} | {doc.name_ngram}",
            subtitle=f"{doc.description}",
            uid=doc.id,
            variables={
                "url": "https://{}{}".format(
                    console_domain, doc.url.format(region=aws_region)
                )
            },
        )

    def enter_handler(self, ui: "UI"):
        zf.open_url_or_print(self.variables["url"])

    def post_enter_handler(self, ui: "UI"):
        ui.wait_next_user_input()


# ------------------------------------------------------------------------------
# search_service_handler
# ------------------------------------------------------------------------------
def search_service_and_return_items(
    query: str,
    ui: T.Optional["UI"] = None,
    refresh_data: bool = False,
) -> T.List[T.Union["ConsoleUrlItem", "InfoItem"]]:
    query = preprocess_query(query)
    docs = dataset.search(
        query=query,
        limit=50,
        simple_response=True,
        verbose=False,
        refresh_data=refresh_data,
    )
    if len(docs):
        docs = [ServiceDocument.from_result(doc) for doc in docs]
        console_domain = ui.console_domain
        return [
            ConsoleUrlItem.from_doc(
                doc,
                console_domain=console_domain,
                aws_region=ui.aws_region,
            )
            for doc in docs
        ]
    else:
        return [
            InfoItem(
                title="No service found",
                subtitle="",
                uid="no-service-found",
            )
        ]


def search_service_handler(
    query: str,
    ui: T.Optional["UI"] = None,
    skip_ui: bool = False,
):
    if query.strip().endswith("!~"):
        if skip_ui is False:  # pragma: no cover
            ui.run_handler(items=[])
            ui.repaint()
            ui.line_editor.press_backspace(n=2)
        return search_service_and_return_items(
            ui=ui,
            query=query[:-2],
            refresh_data=True,
        )

    items = search_service_and_return_items(
        ui=ui,
        query=query,
        refresh_data=False,
    )
    return items


# ------------------------------------------------------------------------------
# main handler
# ------------------------------------------------------------------------------
def handler(
    query: str,
    ui: T.Optional["UI"] = None,
    skip_ui: bool = False,
) -> T.List[T.Union["ConsoleUrlItem"]]:
    return search_service_handler(query, ui, skip_ui)


@dataclasses.dataclass
class UI(zf.UI):
    def __init__(
        self,
        aws_region: str = "us-east-1",
        **kwargs,
    ):
        self.aws_region = aws_region
        super().__init__(
            handler=handler,
            terminal=terminal,
            **kwargs,
        )

    @property
    def console_domain(self) -> str:
        if self.aws_region in {"us-gov-east-1", "us-gov-west-1"}:
            return "console.amazonaws-us-gov.com"
        else:
            return "console.aws.amazon.com"
