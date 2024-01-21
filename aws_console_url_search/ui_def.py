# -*- coding: utf-8 -*-

import typing as T
import dataclasses
import zelfred.api as zf

from .dataset import ServiceDocument, service_dataset, preprocess_query, region_dataset
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
    def post_enter_handler(self, ui: "UI"):
        ui.wait_next_user_input()

    def post_ctrl_a_handler(self, ui: "UI"):
        ui.wait_next_user_input()

    def post_ctrl_w_handler(self, ui: "UI"):
        ui.wait_next_user_input()

    def post_ctrl_u_handler(self, ui: "UI"):
        ui.wait_next_user_input()

    def post_ctrl_p_handler(self, ui: "UI"):
        ui.wait_next_user_input()


@dataclasses.dataclass
class InfoItem(Item):
    pass


# ------------------------------------------------------------------------------
# search_service_handler
# ------------------------------------------------------------------------------
@dataclasses.dataclass
class ConsoleUrlItem(Item):
    @classmethod
    def from_doc(
        cls,
        doc: ServiceDocument,
        console_domain: str,
        aws_region: str,
    ):
        service_id = doc.id.split("-", 1)[0]
        if doc.emoji:
            emoji = f"{doc.emoji} "
        else:
            emoji = ""
        if doc.menu_name:
            title = "🌠 {}{} | {}".format(
                emoji,
                format_resource_type(service_id),
                doc.menu_name,
            )
        else:
            title = "🌟 {}{} ({})".format(
                emoji,
                format_resource_type(service_id),
                doc.srv_name,
            )
        return cls(
            title=title,
            subtitle=f"{doc.desc}",
            uid=doc.id,
            variables={
                "url": "https://{}{}".format(
                    console_domain, doc.url.format(region=aws_region)
                )
            },
        )

    def enter_handler(self, ui: "UI"):
        zf.open_url_or_print(self.variables["url"])

    def ctrl_a_handler(self, ui: "UI"):
        self.ctrl_u_handler(ui)

    def ctrl_u_handler(self, ui: "UI"):
        zf.copy_text(self.variables["url"])


def search_service_and_return_items(
    query: str,
    ui: T.Optional["UI"] = None,
    refresh_data: bool = False,
) -> T.List[T.Union["ConsoleUrlItem", "InfoItem"]]:
    query = preprocess_query(query)
    docs = service_dataset.search(
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
    if skip_ui is False:  # pragma: no cover
        ui.render.prompt = f"[Query (region = {ui.aws_region})]"
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
# search_region_handler
# ------------------------------------------------------------------------------
@dataclasses.dataclass
class RegionItem(Item):
    @classmethod
    def from_region(cls, line_input: str, region: str, description: str):
        return cls(
            title="{} | {}".format(
                highlight_text(region),
                description,
            ),
            subtitle=f"Hit {ShortcutEnum.ENTER} set region and return to search",
            uid=region,
            autocomplete=line_input + "!@" + region,
            variables={"region": region, "line_input": line_input},
        )

    def enter_handler(self, ui: "UI"):
        "no region"
        region = self.variables["region"]
        if region == "no-region":
            ui.aws_region = None
        else:
            ui.aws_region = region

    def post_enter_handler(self, ui: "UI"):  # pragma: no cover
        """
        When exiting the switch aws region session, recover the original query input.
        """
        ui.line_editor.clear_line()
        ui.line_editor.enter_text(self.variables["line_input"])

    def ctrl_a_handler(self, ui: "UI"):
        zf.copy_or_print(self.variables["region"])

    def post_ctrl_a_handler(self, ui: "UI"):
        self.post_enter_handler(ui)

    def ctrl_u_handler(self, ui: "UI"):
        self.ctrl_a_handler(ui)

    def post_ctrl_u_handler(self, ui: "UI"):
        self.post_enter_handler(ui)


def search_region_and_return_items(
    line_input: str,
    aws_region_query: str,
    ui: T.Optional["UI"] = None,
    refresh_data: bool = True,
) -> T.List[T.Union["RegionItem", "InfoItem"]]:
    query = preprocess_query(aws_region_query)
    docs = region_dataset.search(
        query=query,
        limit=50,
        simple_response=True,
        verbose=False,
        refresh_data=refresh_data,
    )
    if len(docs):
        return [
            RegionItem.from_region(
                line_input=line_input,
                region=doc["region"],
                description=doc["desc"],
            )
            for doc in docs
        ]
    else:
        return [
            InfoItem(
                title="No region found",
                subtitle=f"Hit {ShortcutEnum.TAB} to return to re-enter a region query",
                autocomplete=line_input + "!@",
                uid="no-region-found",
            )
        ]


def search_region_handler(
    line_input: str,
    aws_region_query: str,
    ui: T.Optional["UI"] = None,
    skip_ui: bool = False,
):
    if skip_ui is False:  # pragma: no cover
        ui.render.prompt = f"(AWS Region Query)"
    return search_region_and_return_items(
        ui=ui,
        line_input=line_input,
        aws_region_query=aws_region_query,
    )


# ------------------------------------------------------------------------------
# main handler
# ------------------------------------------------------------------------------
def handler(
    query: str,
    ui: T.Optional["UI"] = None,
    skip_ui: bool = False,
) -> T.List[T.Union["ConsoleUrlItem", "RegionItem", "InfoItem"]]:
    if len(query.split("!@", 1)) > 1:
        line_input, aws_region_query = query.split("!@", 1)
        return search_region_handler(
            ui=ui,
            line_input=line_input,
            aws_region_query=aws_region_query,
            skip_ui=skip_ui,
        )

    return search_service_handler(query, ui, skip_ui)


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
